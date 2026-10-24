#!/usr/bin/env node
import path from "node:path";
import {
  bingWebmasterAuth,
  createRunContext,
  dateStampRange,
  fetchJson,
  parseArgs,
  printHelp,
  publicPlan,
  safeSlug,
  writeCsvFile,
  writeJsonFile
} from "./lib/cli-utils.mjs";

const COMMAND = "skills/seo-analytics/scripts/fetch-bing-webmaster.mjs";
const BASE_URL = "https://ssl.bing.com/webmaster/api.svc/json";

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    printHelp({
      command: COMMAND,
      sourceLabel: "Bing Webmaster Tools",
      description: "Fetch Bing Webmaster Tools query, page, rank/traffic, and crawl issue data for a seo-analytics profile, or print a safe dry-run plan.",
      examples: [
        `node ${COMMAND} --dry-run --profile example`,
        `node ${COMMAND} --config seo-analytics.config.yaml --profile example --start-date 2026-05-01 --end-date 2026-05-31`
      ]
    });
    return;
  }

  const context = await createRunContext({
    args,
    sourceKey: "bingWebmaster",
    sourceLabel: "Bing Webmaster Tools",
    requiredField: "siteUrl"
  });

  const siteUrl = context.source.siteUrl;
  const methodNames = context.source.methods ?? [
    "GetQueryStats",
    "GetPageStats",
    "GetRankAndTrafficStats",
    "GetCrawlIssues"
  ];
  const plannedEndpoints = methodNames.map((method) => {
    const url = new URL(`${BASE_URL}/${method}`);
    if (siteUrl) url.searchParams.set("siteUrl", siteUrl);
    if (context.auth?.type !== "bing-oauth") {
      url.searchParams.set("apikey", "<redacted>");
    }
    return url.toString();
  });
  const plannedHeaders = context.auth?.type === "bing-oauth"
    ? { authorization: "Bearer <redacted>" }
    : {};

  const plan = publicPlan(context, {
    source: {
      key: "bingWebmaster",
      label: "Bing Webmaster Tools",
      siteUrl: siteUrl ?? null,
      note: "Bing query/page stats can be weekly; do not interpret them as precise daily trends."
    },
    request: {
      method: "GET",
      endpoints: plannedEndpoints,
      headers: plannedHeaders
    }
  });

  if (args.dryRun) {
    console.log(JSON.stringify(plan, null, 2));
    return;
  }

  if (!siteUrl) {
    throw new Error("sources.bingWebmaster.siteUrl is required for a live Bing Webmaster Tools fetch.");
  }

  const auth = bingWebmasterAuth(context.auth);
  const responses = {};
  for (const method of methodNames) {
    const url = new URL(`${BASE_URL}/${method}`);
    url.searchParams.set("siteUrl", siteUrl);
    const options = {};
    if (auth.type === "bing-api-key") {
      url.searchParams.set("apikey", auth.apiKey);
    } else {
      options.headers = {
        authorization: `Bearer ${auth.accessToken}`
      };
    }
    responses[method] = await fetchJson(url.toString(), options);
  }

  const stem = `bing-webmaster-${safeSlug(context.profileName)}-${dateStampRange(context.window)}`;
  const rawPath = path.join(context.output.targetDir, `${stem}.json`);
  const csvPath = path.join(context.output.targetDir, `${stem}.normalized.csv`);
  await writeJsonFile(rawPath, {
    meta: plan,
    response: responses
  });
  await writeCsvFile(csvPath, normalizeResponses(responses), [
    "source",
    "searchEngine",
    "date",
    "page",
    "query",
    "clicks",
    "impressions",
    "ctr",
    "averagePosition",
    "rawPositionMetric",
    "method"
  ]);

  console.log(JSON.stringify({ ok: true, rawPath, csvPath, methods: Object.keys(responses) }, null, 2));
}

function normalizeResponses(responses) {
  const rows = [];
  for (const [method, body] of Object.entries(responses)) {
    for (const row of body.d ?? []) {
      const clicks = numberOrBlank(row.Clicks);
      const impressions = numberOrBlank(row.Impressions);
      const avgPosition = row.AvgClickPosition ?? row.AvgImpressionPosition ?? "";
      rows.push({
        source: "bingWebmaster",
        searchEngine: "bing",
        date: normalizeBingDate(row.Date),
        page: method === "GetPageStats" ? row.Query ?? row.Url ?? "" : row.Url ?? "",
        query: method === "GetQueryStats" ? row.Query ?? "" : "",
        clicks,
        impressions,
        ctr: clicks !== "" && impressions ? clicks / impressions : "",
        averagePosition: avgPosition,
        rawPositionMetric: row.AvgClickPosition !== undefined ? "AvgClickPosition" : row.AvgImpressionPosition !== undefined ? "AvgImpressionPosition" : "",
        method
      });
    }
  }
  return rows;
}

function numberOrBlank(value) {
  return value === undefined || value === null ? "" : Number(value);
}

function normalizeBingDate(value) {
  if (!value) return "";
  const match = String(value).match(/\/Date\((\d+)/);
  if (match) {
    return new Date(Number(match[1])).toISOString().slice(0, 10);
  }
  return String(value).slice(0, 10);
}

main().catch((error) => {
  console.error(`Error: ${error.message}`);
  process.exit(1);
});
