# Event Model

Use this reference for GA4 event analysis and event recommendations.

## Event Roles

| Role | Meaning |
|------|---------|
| `conversions` | Business-critical outcomes the user wants to optimize from Organic Search. |
| `importantInteractions` | Meaningful middle-of-funnel behavior that helps judge landing page quality. |
| `ignore` | Noise or automatic events that should not drive conversion-quality conclusions. |

## Event Health Labels

| Label | Use When |
|-------|----------|
| `observed` | The event appears in GA4 data. |
| `configured and observed` | The event is configured as a conversion/key event or listed in config and appears in the data window. |
| `configured but not observed` | The event is configured, but current data does not contain it. |
| `candidate conversion event` | Naming or behavior suggests the event may represent a conversion, but it is not configured. |
| `important interaction` | The event helps evaluate page quality even if it is not a final conversion. |
| `ignored/noise event` | The event is routine, automatic, or explicitly ignored. |
| `unexpected key event` | GA4 marks the event as a key event, but it is not in config or the business-type recommendation list. |
| `measurement gap` | Data is missing or incomplete enough that no reliable conclusion can be drawn. |

## Business-Type Recommendations

| `businessType` | Recommended events |
|----------------|--------------------|
| `saas` | `sign_up`, `trial_start`, `demo_request`, `pricing_view`, `pricing_cta_click`, `subscription_start` |
| `ecommerce` | `view_item`, `add_to_cart`, `begin_checkout`, `purchase` |
| `publisher` | `article_read`, `newsletter_signup`, `scroll_depth`, `internal_link_click` |
| `local_business` | `contact_click`, `phone_click`, `directions_click`, `booking_submit` |
| `marketplace` | `search_performed`, `listing_view`, `lead_submit`, `seller_signup` |
| `agency` | `case_study_view`, `service_page_view`, `contact_submit`, `demo_request` |

When `businessType` is missing, infer conservatively from site content, URLs, GA4 event names, and the user's description. If confidence is low, list likely business types and ask the user to confirm.

## Analysis Rules

1. Compare configured conversions with observed Organic Search events.
2. Compare configured important interactions with observed Organic Search events.
3. Identify configured events that do not appear in the selected date window.
4. Identify Organic Search landing pages with sessions but weak conversion or interaction signals.
5. Identify likely conversion-like events not configured as conversions.
6. Identify noise events that are dominating counts without explaining page quality.
7. Identify unexpected key events and explain why they may distort SEO quality analysis.

## Recommendation Rules

For each recommendation, state:

- Evidence source: GA4 report/export, config, or event inventory.
- Current status: observed, configured, missing, or uncertain.
- Suggested action: configure as key event, track as important interaction, ignore, rename, or audit implementation.
- Expected SEO analytics impact: better landing page quality read, cleaner conversion rate, clearer content intent, or better prioritization.
- Confidence level: high, medium, or low.

Do not claim that a recommended event already exists unless it appears in the data or config.
