# Localization Rules

Use this reference when choosing report language or interpreting target search language.

## Language Selection

Choose report language in this order:

1. `language` in the selected profile.
2. The user's explicit language request.
3. The conversation language.
4. English when the language is still unclear.

Public `seo-analytics` must not treat Chinese as a fixed default. Chinese is fully supported when selected by config or user context.

## Separate Report Language From Search Language

| Field | Controls |
|-------|----------|
| `language` | Report headings, summaries, explanations, risks, and action text. |
| `market.searchLanguage` | Search intent interpretation, query-language assumptions, content recommendation language. |
| `market.country` | SERP geography, country filters, local search context, and prioritization. |

When `language` and `market.searchLanguage` differ, write the report in `language` but evaluate queries and page intent in the target search language.

## Preserve Source-Defined Labels

Do not translate:

- GSC, Bing Webmaster Tools, and GA4 field names
- Metric names
- Event names
- Channel group names
- URL paths
- Query text
- API names
- Commands
- File paths

You may explain their meaning in the selected report language.

## Stable Section Names

English report sections:

1. Executive Summary
2. Data Scope and Limitations
3. Google Search Console Opportunities
4. Bing Webmaster Tools Opportunities
5. Cross-Search-Engine Findings
6. GA4 Organic Search Quality Signals
7. Event Analysis
8. Event Recommendation
9. Prioritized SEO Actions
10. Questions to Confirm

Simplified Chinese report sections:

1. 核心结论
2. 数据范围与限制
3. Google Search Console 机会
4. Bing Webmaster Tools 机会
5. 跨搜索引擎发现
6. GA4 Organic Search 质量信号
7. 事件分析
8. 事件推荐
9. 优先级 SEO Actions
10. 待确认问题

For other languages, translate section text naturally while keeping source names such as `Google Search Console`, `Bing Webmaster Tools`, `GA4`, `Organic Search`, and `SEO Actions` stable unless the user asks otherwise.

## Event Naming

Recommended event names should remain engineering-friendly English `snake_case`, such as `sign_up`, `purchase`, and `newsletter_signup`. Localize the event explanation and implementation recommendation, not the event identifier.
