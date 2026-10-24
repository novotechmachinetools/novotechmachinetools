# seo-analytics Configuration

Use this reference when loading project configuration, choosing profiles, resolving source settings, or explaining private local overrides.

## Discovery Order

Load configuration in this order:

1. Explicit `--config` path or a path named by the user.
2. `seo-analytics.config.yaml`
3. `seo-analytics.config.yml`
4. `seo-analytics.config.json`
5. No config: infer conservatively from exports and ask for missing required fields.

After loading the public config, merge a local override from the same directory when present:

1. `seo-analytics.local.yaml`
2. `seo-analytics.local.yml`
3. `seo-analytics.local.json`

Runtime override precedence is:

1. CLI arguments
2. Environment variables
3. Local config
4. Public config

## Required Shape

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
        - demo_request
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

JSON config is equivalent:

```json
{
  "version": 1,
  "defaultProfile": "example",
  "profiles": {
    "example": {
      "site": "https://example.com",
      "businessType": "saas",
      "language": "en",
      "market": {
        "country": "US",
        "searchLanguage": "en"
      }
    }
  }
}
```

## Field Semantics

| Field | Meaning |
|-------|---------|
| `profiles` | Multi-site entry point. Each profile defines one site, source set, event model, and output location. |
| `defaultProfile` | Profile used when `--profile` is not provided. |
| `site` | Canonical site URL for human-readable reporting. Usually not a secret, but can be business-sensitive. |
| `businessType` | Event recommendation profile. Supported first-version values: `saas`, `ecommerce`, `publisher`, `local_business`, `marketplace`, `agency`. |
| `language` | Report language, using BCP 47 tags where possible. If absent and user intent is unclear, default to English. |
| `market.country` | Target country or region for search interpretation. |
| `market.searchLanguage` | Target query/content language for SEO interpretation. Not the same as report language. |
| `sources.gsc.property` | GSC URL-prefix property or domain property, such as `https://www.example.com/` or `sc-domain:example.com`. |
| `sources.bingWebmaster.siteUrl` | Verified Bing Webmaster Tools site URL. |
| `sources.ga4.propertyId` | GA4 numeric property ID. |
| `auth` | Named auth references. Store env var names or local credential path references only. |

## Auth References

Public config must not contain raw secrets. Store references only:

| Type | Required references | Notes |
|------|---------------------|-------|
| `google-application-default` | Optional `accessTokenEnv` | Scripts can use `GOOGLE_OAUTH_ACCESS_TOKEN`, `GOOGLE_ACCESS_TOKEN`, or local application default credentials where available. |
| `google-access-token` or `google-oauth-access-token` | `accessTokenEnv` or `tokenEnv` | Use only short-lived local tokens. Never print them. |
| `google-service-account` | `credentialsPathEnv` or `credentialsPath` in a private local config | The pointed JSON file is private and must not be committed. |
| `bing-api-key` | `apiKeyEnv` | The Bing Webmaster API key is user-level and can access all verified sites for that user. |
| `bing-oauth` | `accessTokenEnv` or `tokenEnv` | Use a short-lived Bing Webmaster OAuth access token. The fetch script sends it as an `Authorization: Bearer` header and does not manage refresh tokens. |

## Local Override Rules

`seo-analytics.local.*` is for private machine-specific overrides such as credential file paths, alternate output roots, or personal profile choices. Recommend adding these files to `.gitignore`:

```gitignore
seo-analytics.local.yaml
seo-analytics.local.yml
seo-analytics.local.json
```

Do not commit:

- API keys
- OAuth client secrets
- access tokens or refresh tokens
- service account JSON
- `.env` contents
- private raw export files

## No-Config Mode

When no config exists, proceed only with safe assumptions:

- Infer source from file names and columns.
- Infer site and date window from exports only if obvious.
- Use the user's requested output language or conversation language; otherwise default to English.
- Ask the user for source property IDs or event model details only when needed to avoid a misleading report.
