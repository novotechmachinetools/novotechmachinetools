import { execFileSync } from "node:child_process";
import { createSign } from "node:crypto";
import { existsSync } from "node:fs";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const DEFAULT_CONFIG_FILES = [
  "seo-analytics.config.yaml",
  "seo-analytics.config.yml",
  "seo-analytics.config.json"
];

const DEFAULT_LOCAL_FILES = [
  "seo-analytics.local.yaml",
  "seo-analytics.local.yml",
  "seo-analytics.local.json"
];

export function parseArgs(argv) {
  const args = {
    dryRun: false,
    help: false,
    config: null,
    profile: null,
    startDate: null,
    endDate: null,
    snapshotDate: null,
    outRoot: null,
    rowLimit: 25000
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--help" || arg === "-h") {
      args.help = true;
    } else if (arg === "--dry-run") {
      args.dryRun = true;
    } else if (arg === "--config") {
      args.config = requireValue(argv, ++i, arg);
    } else if (arg === "--profile") {
      args.profile = requireValue(argv, ++i, arg);
    } else if (arg === "--start-date") {
      args.startDate = requireDate(requireValue(argv, ++i, arg), arg);
    } else if (arg === "--end-date") {
      args.endDate = requireDate(requireValue(argv, ++i, arg), arg);
    } else if (arg === "--snapshot-date") {
      args.snapshotDate = requireDate(requireValue(argv, ++i, arg), arg);
    } else if (arg === "--out-root") {
      args.outRoot = requireValue(argv, ++i, arg);
    } else if (arg === "--row-limit") {
      args.rowLimit = Number.parseInt(requireValue(argv, ++i, arg), 10);
      if (!Number.isInteger(args.rowLimit) || args.rowLimit < 1) {
        throw new Error("--row-limit must be a positive integer");
      }
    } else {
      throw new Error(`Unknown argument: ${arg}`);
    }
  }

  return args;
}

export function printHelp({ command, sourceLabel, description, examples = [] }) {
  console.log(`${command}

${description}

Usage:
  node ${command} [--dry-run] [--config <path>] [--profile <name>] [--start-date YYYY-MM-DD] [--end-date YYYY-MM-DD] [--snapshot-date YYYY-MM-DD] [--out-root <dir>]

Options:
  --help, -h                 Print this help message.
  --dry-run                  Validate config and print the planned ${sourceLabel} request without credentials or network calls.
  --config <path>            Use a specific seo-analytics config file.
  --profile <name>           Select a profile from config.profiles.
  --start-date <date>        Start date in YYYY-MM-DD format.
  --end-date <date>          End date in YYYY-MM-DD format.
  --snapshot-date <date>     Output snapshot label date in YYYY-MM-DD format.
  --out-root <dir>           Override output root. Defaults to profile.output.rawDataDir or docs/seo/raw-data.
  --row-limit <number>       Source row limit where supported. Defaults to 25000.

Examples:
${examples.map((example) => `  ${example}`).join("\n")}
`);
}

export async function createRunContext({ args, sourceKey, sourceLabel, requiredField }) {
  const cwd = process.cwd();
  const configInfo = await loadConfig({ explicitConfig: args.config, cwd });
  const profileInfo = selectProfile(configInfo.config, args.profile);
  const profile = profileInfo.profile;
  const source = profile.sources?.[sourceKey] ?? {};
  const auth = source.auth ? configInfo.config.auth?.[source.auth] : null;
  const window = resolveDateWindow(args);
  const outRoot = path.resolve(cwd, args.outRoot ?? profile.output?.rawDataDir ?? "docs/seo/raw-data");
  const targetDir = path.join(outRoot, sourceKey, profileInfo.name ?? "default", window.snapshotDate);
  const warnings = [];

  if (!configInfo.configPath) {
    warnings.push("No seo-analytics config file found. Using empty config and requiring explicit source metadata from exports.");
  }

  if (source.enabled === false) {
    warnings.push(`${sourceLabel} is disabled for this profile.`);
  }

  if (!source[requiredField]) {
    warnings.push(`${sourceLabel} source is missing sources.${sourceKey}.${requiredField}.`);
  }

  if (source.auth && !auth) {
    warnings.push(`${sourceLabel} auth reference '${source.auth}' was not found in top-level auth.`);
  }

  return {
    cwd,
    args,
    config: configInfo.config,
    configPath: configInfo.configPath,
    localConfigPath: configInfo.localConfigPath,
    profileName: profileInfo.name,
    profile,
    source,
    authRef: source.auth ?? null,
    auth,
    window,
    output: {
      outRoot,
      targetDir
    },
    warnings
  };
}

export function publicPlan(context, extra = {}) {
  return {
    mode: context.args.dryRun ? "dry-run" : "fetch",
    configPath: context.configPath,
    localConfigPath: context.localConfigPath,
    profile: context.profileName,
    site: context.profile.site ?? null,
    businessType: context.profile.businessType ?? null,
    language: context.profile.language ?? null,
    market: context.profile.market ?? null,
    auth: summarizeAuth(context.authRef, context.auth),
    dateWindow: {
      startDate: context.window.startDate,
      endDate: context.window.endDate,
      snapshotDate: context.window.snapshotDate
    },
    output: context.output,
    warnings: context.warnings,
    ...extra
  };
}

export async function writeJsonFile(filePath, value) {
  await mkdir(path.dirname(filePath), { recursive: true });
  await writeFile(filePath, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

export async function writeCsvFile(filePath, rows, headers) {
  await mkdir(path.dirname(filePath), { recursive: true });
  const lines = [headers.join(",")];
  for (const row of rows) {
    lines.push(headers.map((header) => csvCell(row[header])).join(","));
  }
  await writeFile(filePath, `${lines.join("\n")}\n`, "utf8");
}

export async function fetchJson(url, options = {}) {
  const response = await fetch(url, options);
  const text = await response.text();
  let body;
  try {
    body = text ? JSON.parse(text) : {};
  } catch {
    body = { raw: text };
  }

  if (!response.ok) {
    const message = body?.error?.message ?? body?.Message ?? body?.message ?? response.statusText;
    throw new Error(`Request failed (${response.status}) for ${redactUrl(url)}: ${message}`);
  }

  return body;
}

export async function googleAccessToken(auth, scope) {
  if (!auth) {
    throw new Error("Missing Google auth reference. Add an auth block or use --dry-run.");
  }

  if (auth.type === "google-access-token" || auth.type === "google-oauth-access-token") {
    return envSecret(auth.accessTokenEnv ?? auth.tokenEnv, "Google access token env var");
  }

  if (auth.type === "google-application-default") {
    const envName = auth.accessTokenEnv ?? "GOOGLE_OAUTH_ACCESS_TOKEN";
    if (process.env[envName]) {
      return process.env[envName];
    }
    if (process.env.GOOGLE_ACCESS_TOKEN) {
      return process.env.GOOGLE_ACCESS_TOKEN;
    }
    try {
      return execFileSync("gcloud", ["auth", "application-default", "print-access-token"], {
        encoding: "utf8",
        stdio: ["ignore", "pipe", "ignore"]
      }).trim();
    } catch {
      throw new Error("Unable to resolve Google Application Default credentials. Set GOOGLE_OAUTH_ACCESS_TOKEN/GOOGLE_ACCESS_TOKEN or configure google-service-account credentials.");
    }
  }

  if (auth.type === "google-service-account") {
    return serviceAccountToken(auth, scope);
  }

  throw new Error(`Unsupported Google auth type '${auth.type}'.`);
}

export function bingWebmasterAuth(auth) {
  if (!auth) {
    throw new Error("Missing Bing Webmaster Tools auth reference. Add auth.<name>.apiKeyEnv/accessTokenEnv or use --dry-run.");
  }
  if (auth.type === "bing-api-key") {
    return {
      type: "bing-api-key",
      apiKey: envSecret(auth.apiKeyEnv, "Bing Webmaster API key env var")
    };
  }
  if (auth.type === "bing-oauth") {
    return {
      type: "bing-oauth",
      accessToken: envSecret(auth.accessTokenEnv ?? auth.tokenEnv, "Bing Webmaster OAuth access token env var")
    };
  }
  throw new Error(`Unsupported Bing Webmaster Tools auth type '${auth.type}'. Supported live fetch auth types are bing-api-key and bing-oauth.`);
}

export function bingApiKey(auth) {
  const resolved = bingWebmasterAuth(auth);
  if (resolved.type !== "bing-api-key") {
    throw new Error(`Unsupported Bing Webmaster Tools auth type '${auth.type}'. Use bingWebmasterAuth for OAuth-capable requests.`);
  }
  return resolved.apiKey;
}

export function dateStampRange(window) {
  return `${window.startDate}_${window.endDate}`;
}

export function safeSlug(value) {
  return String(value ?? "default")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80) || "default";
}

function requireValue(argv, index, flag) {
  const value = argv[index];
  if (!value || value.startsWith("--")) {
    throw new Error(`${flag} requires a value`);
  }
  return value;
}

function requireDate(value, flag) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) {
    throw new Error(`${flag} must be YYYY-MM-DD`);
  }
  return value;
}

function resolveDateWindow(args) {
  const today = new Date();
  const defaultEnd = new Date(Date.UTC(today.getUTCFullYear(), today.getUTCMonth(), today.getUTCDate() - 3));
  const defaultStart = new Date(defaultEnd);
  defaultStart.setUTCDate(defaultStart.getUTCDate() - 29);
  const snapshot = new Date(Date.UTC(today.getUTCFullYear(), today.getUTCMonth(), today.getUTCDate()));

  const startDate = args.startDate ?? formatDate(defaultStart);
  const endDate = args.endDate ?? formatDate(defaultEnd);
  const snapshotDate = args.snapshotDate ?? formatDate(snapshot);

  if (startDate > endDate) {
    throw new Error("--start-date must be on or before --end-date");
  }

  return { startDate, endDate, snapshotDate };
}

function formatDate(date) {
  return date.toISOString().slice(0, 10);
}

async function loadConfig({ explicitConfig, cwd }) {
  const configPath = explicitConfig ? path.resolve(cwd, explicitConfig) : findFirst(cwd, DEFAULT_CONFIG_FILES);
  const baseDir = configPath ? path.dirname(configPath) : cwd;
  const localConfigPath = findFirst(baseDir, DEFAULT_LOCAL_FILES);
  let config = {};

  if (configPath) {
    config = await readConfigFile(configPath);
  }
  if (localConfigPath) {
    config = deepMerge(config, await readConfigFile(localConfigPath));
  }

  return { config, configPath, localConfigPath };
}

function findFirst(dir, names) {
  for (const name of names) {
    const candidate = path.join(dir, name);
    if (existsSync(candidate)) {
      return candidate;
    }
  }
  return null;
}

async function readConfigFile(filePath) {
  const text = await readFile(filePath, "utf8");
  if (filePath.endsWith(".json")) {
    return JSON.parse(text);
  }
  return parseSimpleYaml(text);
}

function selectProfile(config, requestedProfile) {
  const profiles = config.profiles ?? {};
  const name = requestedProfile ?? config.defaultProfile ?? Object.keys(profiles)[0] ?? null;
  if (!name) {
    return { name: null, profile: config.site || config.sources ? config : {} };
  }
  if (!profiles[name]) {
    throw new Error(`Profile '${name}' was not found in config.profiles`);
  }
  return { name, profile: profiles[name] };
}

function parseSimpleYaml(text) {
  const parsedLines = [];
  const rawLines = text.replace(/\t/g, "  ").split(/\r?\n/);

  for (let index = 0; index < rawLines.length; index += 1) {
    const raw = rawLines[index];
    const trimmed = raw.trim();
    if (!trimmed || trimmed.startsWith("#")) {
      continue;
    }
    const content = stripInlineComment(raw.slice(raw.match(/^ */)[0].length)).trimEnd();
    if (!content) {
      continue;
    }
    parsedLines.push({
      indent: raw.match(/^ */)[0].length,
      content,
      line: index + 1
    });
  }

  const root = {};
  const stack = [{ indent: -1, value: root }];

  for (let i = 0; i < parsedLines.length; i += 1) {
    const line = parsedLines[i];
    while (line.indent <= stack[stack.length - 1].indent) {
      stack.pop();
    }
    const parent = stack[stack.length - 1].value;

    if (line.content.startsWith("- ")) {
      if (!Array.isArray(parent)) {
        throw new Error(`Unsupported YAML list placement at line ${line.line}`);
      }
      parent.push(parseScalar(line.content.slice(2).trim()));
      continue;
    }

    const match = line.content.match(/^([^:]+):(.*)$/);
    if (!match) {
      throw new Error(`Unsupported YAML syntax at line ${line.line}`);
    }

    const key = unquote(match[1].trim());
    const rest = match[2].trim();
    let value;

    if (rest === "") {
      const next = parsedLines[i + 1];
      value = next && next.indent > line.indent && next.content.startsWith("- ") ? [] : {};
    } else {
      value = parseScalar(rest);
    }

    parent[key] = value;
    if (value && typeof value === "object") {
      stack.push({ indent: line.indent, value });
    }
  }

  return root;
}

function stripInlineComment(value) {
  let inSingle = false;
  let inDouble = false;
  for (let i = 0; i < value.length; i += 1) {
    const char = value[i];
    if (char === "'" && !inDouble) inSingle = !inSingle;
    if (char === '"' && !inSingle) inDouble = !inDouble;
    if (char === "#" && !inSingle && !inDouble && (i === 0 || /\s/.test(value[i - 1]))) {
      return value.slice(0, i);
    }
  }
  return value;
}

function parseScalar(value) {
  if (value === "true") return true;
  if (value === "false") return false;
  if (value === "null") return null;
  if (/^-?\d+(\.\d+)?$/.test(value)) return Number(value);
  if (value.startsWith("[") && value.endsWith("]")) {
    const inner = value.slice(1, -1).trim();
    if (!inner) return [];
    return inner.split(",").map((item) => parseScalar(item.trim()));
  }
  return unquote(value);
}

function unquote(value) {
  if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
    return value.slice(1, -1);
  }
  return value;
}

function deepMerge(base, overlay) {
  if (!isPlainObject(base) || !isPlainObject(overlay)) {
    return overlay ?? base;
  }
  const output = { ...base };
  for (const [key, value] of Object.entries(overlay)) {
    output[key] = key in output ? deepMerge(output[key], value) : value;
  }
  return output;
}

function isPlainObject(value) {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

function summarizeAuth(authRef, auth) {
  if (!authRef && !auth) return null;
  if (!auth) return { ref: authRef, found: false };
  const summary = { ref: authRef, type: auth.type };
  for (const key of ["apiKeyEnv", "accessTokenEnv", "tokenEnv", "credentialsPathEnv"]) {
    if (auth[key]) summary[key] = auth[key];
  }
  if (auth.credentialsPath) summary.credentialsPath = "<local path>";
  return summary;
}

function envSecret(envName, label) {
  if (!envName) {
    throw new Error(`${label} is not configured.`);
  }
  const value = process.env[envName];
  if (!value) {
    throw new Error(`${label} '${envName}' is not set.`);
  }
  return value;
}

async function serviceAccountToken(auth, scope) {
  const credentialsPath = auth.credentialsPath ?? (auth.credentialsPathEnv ? process.env[auth.credentialsPathEnv] : null);
  if (!credentialsPath) {
    throw new Error("google-service-account requires credentialsPath in a private local config or credentialsPathEnv pointing to a local file.");
  }

  const credentials = JSON.parse(await readFile(credentialsPath, "utf8"));
  const now = Math.floor(Date.now() / 1000);
  const assertion = signJwt(
    { alg: "RS256", typ: "JWT" },
    {
      iss: credentials.client_email,
      scope,
      aud: credentials.token_uri ?? "https://oauth2.googleapis.com/token",
      exp: now + 3600,
      iat: now
    },
    credentials.private_key
  );

  const body = new URLSearchParams({
    grant_type: "urn:ietf:params:oauth:grant-type:jwt-bearer",
    assertion
  });

  const response = await fetch(credentials.token_uri ?? "https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "content-type": "application/x-www-form-urlencoded" },
    body
  });
  const token = await response.json();
  if (!response.ok) {
    throw new Error(`Google service account token exchange failed: ${token.error_description ?? token.error ?? response.statusText}`);
  }
  return token.access_token;
}

function signJwt(header, payload, privateKey) {
  const encodedHeader = base64Url(JSON.stringify(header));
  const encodedPayload = base64Url(JSON.stringify(payload));
  const signer = createSign("RSA-SHA256");
  signer.update(`${encodedHeader}.${encodedPayload}`);
  signer.end();
  return `${encodedHeader}.${encodedPayload}.${signer.sign(privateKey, "base64url")}`;
}

function base64Url(value) {
  return Buffer.from(value).toString("base64url");
}

function csvCell(value) {
  if (value === null || value === undefined) return "";
  const text = String(value);
  if (/[",\n\r]/.test(text)) {
    return `"${text.replace(/"/g, '""')}"`;
  }
  return text;
}

function redactUrl(url) {
  try {
    const parsed = new URL(url);
    for (const key of ["apikey", "access_token", "key"]) {
      if (parsed.searchParams.has(key)) {
        parsed.searchParams.set(key, "<redacted>");
      }
    }
    return parsed.toString();
  } catch {
    return "<redacted-url>";
  }
}
