# SEO Analytics Report Outline

Use this outline when producing a report from GSC, Bing Webmaster Tools, GA4, and event data.

## 1. Executive Summary

State the main SEO opportunities in priority order. Separate acquisition issues, landing page quality issues, and measurement issues.

## 2. Data Scope and Limitations

Include:

- Site/profile
- Date window
- Data sources and file paths
- Filters used, such as Organic Search
- Missing fields or incomplete exports
- Bing data granularity caveats when query/page data is weekly or source-limited
- Whether the report used exports, live fetches, or mixed sources

## 3. Google Search Console Opportunities

Analyze when data is available:

- Clicks, impressions, CTR, and average position
- High-impression low-CTR query/page pairs
- Position 3-10 CTR opportunities
- Position 10-30 content, internal link, and intent-match opportunities
- Query/page mismatch
- Device or country differences

## 4. Bing Webmaster Tools Opportunities

Analyze when data is available:

- Query stats
- Page stats
- Rank and traffic stats
- Crawl and indexing clues
- Field limitations and update granularity
- Opportunities that differ from Google data

Do not treat Bing weekly query/page stats as exact daily trends.

## 5. Cross-Search-Engine Findings

Compare Google and Bing:

- Queries that perform well in one engine but not the other
- Pages with engine-specific CTR or ranking gaps
- Pages with Bing crawl/indexing clues but Google performance potential
- Cases where field or granularity differences prevent direct comparison

## 6. GA4 Organic Search Quality Signals

Analyze:

- Organic Search sessions
- Engagement signals
- Landing page quality
- Event rate or key event rate when available
- High-session pages with weak interactions or conversions
- Pages with strong search acquisition but weak post-click behavior

## 7. Event Analysis

Use `event-model.md` labels:

- Configured conversions observed or missing
- Important interactions observed or missing
- Ignored/noise events
- Unexpected key events
- Measurement gaps

## 8. Event Recommendation

Recommend events based on `businessType`, current event inventory, and Organic Search behavior. Mark each recommendation as observed, missing, candidate, or uncertain.

## 9. Prioritized SEO Actions

Use this table:

| Priority | Evidence | Affected page/query | Action | Expected metric impact | More data needed? |
|----------|----------|---------------------|--------|------------------------|-------------------|
| High | GSC query/page | `/pricing` + "pricing query" | Rewrite title/meta and align H1 with query intent | Higher CTR | No |

Each high-priority action must be executable. Avoid generic advice without a page, query, source, or expected metric.

## 10. Questions to Confirm

Ask only questions that change the recommendation:

- Business type when inference is weak
- Whether a conversion event is truly business-critical
- Whether a property/site URL maps to the right site
- Whether missing events are implementation gaps or expected behavior

## Machine-Readable Summary

When useful, append a compact block:

```yaml
SEO_ANALYTICS_META:
  profile: example
  site: https://example.com
  startDate: 2026-05-01
  endDate: 2026-05-31
  sources:
    gsc: true
    bingWebmaster: true
    ga4: true
  language: en
  market:
    country: US
    searchLanguage: en
```
