#!/usr/bin/env node
import path from "node:path";
import {
  createRunContext,
  dateStampRange,
  fetchJson,
  googleAccessToken,
  parseArgs,
  printHelp,
  publicPlan,
  safeSlug,
  writeCsvFile,
  writeJsonFile
} from "./lib/cli-utils.mjs";

const COMMAND = "skills/seo-analytics/scripts/fetch-gsc.mjs";
const SCOPE = "https://www.googleapis.com/auth/webmasters.readonly";

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    printHelp({
      command: COMMAND,
      sourceLabel: "Google Search Console",
      description: "Fetch Google Search Console Search Analytics data for a seo-analytics profile, or print a safe dry-run plan.",
      examples: [
        `node ${COMMAND} --dry-run --profile example`,
        `node ${COMMAND} --config seo-analytics.config.yaml --profile example --start-date 2026-05-01 --end-date 2026-05-31`
      ]
    });
    return;
  }

  const context = await createRunContext({
    args,
    sourceKey: "gsc",
    sourceLabel: "Google Search Console",
    requiredField: "property"
  });

  const property = context.source.property;
  const dimensions = context.source.dimensions ?? ["date", "query", "page"];
  const requestBody = {
    startDate: context.window.startDate,
    endDate: context.window.endDate,
    dimensions,
    type: context.source.type ?? "web",
    rowLimit: Math.min(args.rowLimit, 25000),
    startRow: 0
  };
  const endpoint = property
    ? `https://www.googleapis.com/webmasters/v3/sites/${encodeURIComponent(property)}/searchAnalytics/query`
    : null;

  const plan = publicPlan(context, {
    source: {
      key: "gsc",
      label: "Google Search Console",
      property: property ?? null
    },
    request: {
      method: "POST",
      endpoint,
      body: requestBody
    }
  });

  if (args.dryRun) {
    console.log(JSON.stringify(plan, null, 2));
    return;
  }

  if (!property) {
    throw new Error("sources.gsc.property is required for a live GSC fetch.");
  }

  const token = await googleAccessToken(context.auth, SCOPE);
  const response = await fetchJson(endpoint, {
    method: "POST",
    headers: {
      authorization: `Bearer ${token}`,
      "content-type": "application/json"
    },
    body: JSON.stringify(requestBody)
  });

  const stem = `gsc-search-analytics-${safeSlug(context.profileName)}-${dateStampRange(context.window)}`;
  const rawPath = path.join(context.output.targetDir, `${stem}.json`);
  const csvPath = path.join(context.output.targetDir, `${stem}.normalized.csv`);
  await writeJsonFile(rawPath, {
    meta: plan,
    response
  });
  await writeCsvFile(csvPath, normalizeRows(response.rows ?? [], dimensions), [
    "source",
    "searchEngine",
    "date",
    "page",
    "query",
    "clicks",
    "impressions",
    "ctr",
    "averagePosition",
    "rawPositionMetric"
  ]);

  console.log(JSON.stringify({ ok: true, rawPath, csvPath, rows: response.rows?.length ?? 0 }, null, 2));
}

function normalizeRows(rows, dimensions) {
  return rows.map((row) => {
    const values = Object.fromEntries(dimensions.map((dimension, index) => [dimension, row.keys?.[index] ?? ""]));
    return {
      source: "gsc",
      searchEngine: "google",
      date: values.date ?? "",
      page: values.page ?? "",
      query: values.query ?? "",
      clicks: row.clicks ?? "",
      impressions: row.impressions ?? "",
      ctr: row.ctr ?? "",
      averagePosition: row.position ?? "",
      rawPositionMetric: "position"
    };
  });
}

main().catch((error) => {
  console.error(`Error: ${error.message}`);
  process.exit(1);
});
