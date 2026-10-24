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

const COMMAND = "skills/seo-analytics/scripts/fetch-ga4.mjs";
const SCOPE = "https://www.googleapis.com/auth/analytics.readonly";

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    printHelp({
      command: COMMAND,
      sourceLabel: "GA4",
      description: "Fetch GA4 Organic Search landing page and event data for a seo-analytics profile, or print a safe dry-run plan.",
      examples: [
        `node ${COMMAND} --dry-run --profile example`,
        `node ${COMMAND} --config seo-analytics.config.yaml --profile example --start-date 2026-05-01 --end-date 2026-05-31`
      ]
    });
    return;
  }

  const context = await createRunContext({
    args,
    sourceKey: "ga4",
    sourceLabel: "GA4",
    requiredField: "propertyId"
  });

  const propertyId = context.source.propertyId;
  const endpoint = propertyId
    ? `https://analyticsdata.googleapis.com/v1beta/properties/${propertyId}:runReport`
    : null;
  const requests = buildRequests(context);
  const plan = publicPlan(context, {
    source: {
      key: "ga4",
      label: "GA4",
      propertyId: propertyId ?? null
    },
    request: {
      method: "POST",
      endpoint,
      reports: requests
    }
  });

  if (args.dryRun) {
    console.log(JSON.stringify(plan, null, 2));
    return;
  }

  if (!propertyId) {
    throw new Error("sources.ga4.propertyId is required for a live GA4 fetch.");
  }

  const token = await googleAccessToken(context.auth, SCOPE);
  const response = {};
  for (const request of requests) {
    response[request.name] = await fetchJson(endpoint, {
      method: "POST",
      headers: {
        authorization: `Bearer ${token}`,
        "content-type": "application/json"
      },
      body: JSON.stringify(request.body)
    });
  }

  const stem = `ga4-organic-search-${safeSlug(context.profileName)}-${dateStampRange(context.window)}`;
  const rawPath = path.join(context.output.targetDir, `${stem}.json`);
  const csvPath = path.join(context.output.targetDir, `${stem}.events.csv`);
  await writeJsonFile(rawPath, {
    meta: plan,
    response
  });
  await writeCsvFile(csvPath, normalizeEventRows(response.events), [
    "source",
    "searchEngine",
    "eventName",
    "sessionDefaultChannelGroup",
    "eventCount",
    "totalUsers"
  ]);

  console.log(JSON.stringify({ ok: true, rawPath, csvPath, reports: Object.keys(response) }, null, 2));
}

function buildRequests(context) {
  const dateRanges = [{ startDate: context.window.startDate, endDate: context.window.endDate }];
  const organicFilter = {
    filter: {
      fieldName: "sessionDefaultChannelGroup",
      stringFilter: {
        matchType: "EXACT",
        value: "Organic Search"
      }
    }
  };
  const limit = String(Math.min(context.args.rowLimit, 250000));

  return [
    {
      name: "organicLandingPages",
      body: {
        dateRanges,
        dimensions: [
          { name: "landingPagePlusQueryString" },
          { name: "sessionDefaultChannelGroup" }
        ],
        metrics: [
          { name: "sessions" },
          { name: "engagedSessions" },
          { name: "eventCount" }
        ],
        dimensionFilter: organicFilter,
        limit
      }
    },
    {
      name: "events",
      body: {
        dateRanges,
        dimensions: [
          { name: "eventName" },
          { name: "sessionDefaultChannelGroup" }
        ],
        metrics: [
          { name: "eventCount" },
          { name: "totalUsers" }
        ],
        dimensionFilter: organicFilter,
        limit
      }
    }
  ];
}

function normalizeEventRows(report) {
  return (report?.rows ?? []).map((row) => ({
    source: "ga4",
    searchEngine: "",
    eventName: row.dimensionValues?.[0]?.value ?? "",
    sessionDefaultChannelGroup: row.dimensionValues?.[1]?.value ?? "",
    eventCount: row.metricValues?.[0]?.value ?? "",
    totalUsers: row.metricValues?.[1]?.value ?? ""
  }));
}

main().catch((error) => {
  console.error(`Error: ${error.message}`);
  process.exit(1);
});
