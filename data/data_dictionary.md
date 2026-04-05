# Data Dictionary — Marketing Funnel Dataset

## File: `sample_funnel_data.csv`

This dataset represents a simulated 6-month marketing funnel
across 6 acquisition channels (Jan–Jun 2025).

---

## Columns

| Column      | Type    | Description                                                  | Example         |
|-------------|---------|--------------------------------------------------------------|-----------------|
| `month`     | string  | Reporting month (any readable date string)                   | `Jan 2025`      |
| `channel`   | string  | Marketing acquisition channel                                | `Paid Search`   |
| `visitors`  | integer | Total unique website visitors from that channel in the month | `3800`          |
| `leads`     | integer | Visitors who submitted a form / expressed interest           | `420`           |
| `mqls`      | integer | Marketing Qualified Leads — leads scored by marketing        | `210`           |
| `sqls`      | integer | Sales Qualified Leads — leads accepted by sales team         | `130`           |
| `customers` | integer | SQLs who converted to paying customers                       | `42`            |
| `revenue`   | float   | Total revenue (₹) generated from that channel + month       | `18900`         |

---

## Channels in sample data

| Channel          | Description                              |
|------------------|------------------------------------------|
| Organic Search   | SEO / unpaid Google traffic              |
| Paid Search      | Google Ads / PPC campaigns               |
| Social Media     | Instagram, LinkedIn, Twitter ads         |
| Email            | Newsletter and drip campaign leads       |
| Referral         | Partner websites / backlink traffic      |
| Direct           | Users who typed the URL directly         |

---

## Funnel Stages

```
Visitors → Leads → MQLs → SQLs → Customers
```

| Transition         | Metric Name       | Formula                        |
|--------------------|-------------------|--------------------------------|
| Visitors → Leads   | Visit-to-Lead CVR | leads / visitors × 100         |
| Leads → MQLs       | Lead-to-MQL Rate  | mqls / leads × 100             |
| MQLs → SQLs        | MQL-to-SQL Rate   | sqls / mqls × 100              |
| SQLs → Customers   | SQL-to-Close Rate | customers / sqls × 100         |
| Visitors → Customers | Overall CVR     | customers / visitors × 100     |

---

## Notes

- `mqls` and `sqls` columns are **optional** in your upload.
  The dashboard will auto-calculate them if missing:
  - `mqls = leads × 0.48`
  - `sqls = mqls × 0.52`
- Revenue is in **Indian Rupees (₹)** in the sample data.
  You can use any currency — the dashboard displays raw values.
- Minimum required columns: `month, channel, visitors, leads, customers, revenue`
