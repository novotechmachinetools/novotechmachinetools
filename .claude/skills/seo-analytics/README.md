# seo-analytics

Analyze SEO performance from Google Search Console, Bing Webmaster Tools, and GA4 data.

`seo-analytics` is an Agent Skill for traditional SEO data analysis. It reads existing CSV/JSON exports by default, optionally fetches data when safe credentials are configured, and produces evidence-backed recommendations for search acquisition, landing page quality, and event measurement.

It does not perform GEO analytics, AI visibility scoring, LLM citation analysis, or private product API integration.

---

## What Gets Analyzed

| Source | Focus |
|--------|-------|
| Google Search Console | Queries, pages, clicks, impressions, CTR, average position, low-CTR opportunities, rank improvement opportunities |
| Bing Webmaster Tools | Query stats, page stats, rank and traffic stats, crawl/indexing clues, Google vs Bing differences |
| GA4 | Organic Search sessions, engagement, landing page quality, event inventory, key events, conversion paths |
| Event model | Configured conversions, important interactions, ignored events, missing measurement, recommended business events |

## Typical Inputs

- GSC Search Analytics CSV/JSON exports
- Bing Webmaster Tools CSV/JSON exports
- GA4 Data API JSON exports
- GA4 UI CSV exports
- `seo-analytics.config.yaml`, `seo-analytics.config.yml`, or `seo-analytics.config.json`
- Optional private `seo-analytics.local.*` override files

## Configuration

Use `seo-analytics.config.yaml` for shared project configuration and `seo-analytics.local.yaml` for private local overrides. Local override files can contain credential path references or environment-variable-specific auth settings, but must not contain raw secrets.

```yaml
version: 1
defaultProfile: example

profiles:
  example:
    site: https://example.com
    businessType: saas
    language: en
    market:
      country: US
      searchLanguage: en
    sources:
      gsc:
        enabled: true
        property: sc-domain:example.com
        auth: google-adc
      bingWebmaster:
        enabled: true
        siteUrl: https://example.com
        auth: bing-webmaster-api
      ga4:
        enabled: true
        propertyId: "123456789"
        auth: ga4-service-account
    events:
      conversions:
        - sign_up
        - trial_start
      importantInteractions:
        - pricing_view
        - pricing_cta_click
      ignore:
        - page_view
        - session_start
    output:
      rawDataDir: docs/seo/raw-data
      reportsDir: docs/seo/reports

auth:
  google-adc:
    type: google-application-default
  ga4-service-account:
    type: google-service-account
    credentialsPathEnv: GA4_CREDENTIALS_PATH
  bing-webmaster-api:
    type: bing-api-key
    apiKeyEnv: BING_WEBMASTER_API_KEY
  bing-webmaster-oauth:
    type: bing-oauth
    accessTokenEnv: BING_WEBMASTER_ACCESS_TOKEN
```

Add private local overrides to `.gitignore`:

```gitignore
seo-analytics.local.yaml
seo-analytics.local.yml
seo-analytics.local.json
```

## Optional Fetch Scripts

The skill works with existing exports without credentials. Fetch scripts are optional helpers for projects that already have safe local credentials.

```bash
node skills/seo-analytics/scripts/fetch-gsc.mjs --help
node skills/seo-analytics/scripts/fetch-gsc.mjs --dry-run --profile example

node skills/seo-analytics/scripts/fetch-bing-webmaster.mjs --help
node skills/seo-analytics/scripts/fetch-bing-webmaster.mjs --dry-run --profile example

node skills/seo-analytics/scripts/fetch-ga4.mjs --help
node skills/seo-analytics/scripts/fetch-ga4.mjs --dry-run --profile example
```

All three scripts share the `scripts/lib/cli-utils.mjs` helper (config discovery and merging, auth resolution, output writing).

Supported shared options:

| Option | Purpose |
|--------|---------|
| `--help` | Print usage |
| `--dry-run` | Validate config and print the planned request without credentials or network calls |
| `--config <path>` | Use an explicit config file |
| `--profile <name>` | Select a profile from `profiles` |
| `--start-date <YYYY-MM-DD>` | Start of data window |
| `--end-date <YYYY-MM-DD>` | End of data window |
| `--snapshot-date <YYYY-MM-DD>` | Date label for output paths |
| `--out-root <dir>` | Override raw data output root |
| `--row-limit <number>` | Source row limit where supported (default 25000) |

Bing Webmaster Tools live fetches support `bing-api-key` and `bing-oauth`.
For `bing-oauth`, provide a short-lived access token through `accessTokenEnv`
or `tokenEnv`; the script sends it as an `Authorization: Bearer` header and
does not perform OAuth authorization-code or refresh-token exchange.

## Report Output

Reports should include:

- Executive summary
- Data scope and limitations
- Google Search Console opportunities
- Bing Webmaster Tools opportunities
- Cross-search-engine differences
- GA4 Organic Search quality signals
- Event Analysis
- Event Recommendation
- Prioritized SEO Actions
- Questions to confirm

The report language is controlled by `language`. If missing, use the user's explicit language request or conversation language. If still unclear, default to English. `market.searchLanguage` describes the target search-language context and is not the same as report language.

## Related Skills

| Skill | Relationship |
|-------|--------------|
| [geo-audit](../geo-audit/) | Audits whether a site can be understood, cited, and recommended by AI systems |
| [geo-monitor](../geo-monitor/) | Tracks GEO audit score changes over time |
| [geo-compare](../geo-compare/) | Compares GEO audit scores against competitors |
