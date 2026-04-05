# 📊 Marketing Funnel & Conversion Performance Analysis
### Future Interns — Data Science & Analytics · Task 3 · 2026

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Dash](https://img.shields.io/badge/Dash-2.17-00CED1?logo=plotly&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-5.22-3F4F75?logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.2-150458?logo=pandas&logoColor=white)
![Dataset](https://img.shields.io/badge/Dataset-UCI%20Bank%20Marketing-orange)
![Records](https://img.shields.io/badge/Records-45%2C211-brightgreen)

---

## 🔍 Overview

A fully interactive **marketing funnel analytics dashboard** powered by the real-world  
**Bank Marketing Campaign dataset (UCI ML Repository, 45,211 records)**.

Analyzes how contacts move through the full acquisition funnel:

```
Contacted  →  Leads  →  MQLs  →  SQLs  →  Subscribers (Customers)
```

The dashboard maps raw UCI bank-marketing columns to standard funnel stages:

| Raw Column | Funnel Stage | Logic |
|------------|-------------|-------|
| All records | Contacted (Visitors) | Every outreach record |
| `duration` | Lead | Call duration > 0 seconds |
| `campaign`, `previous` | MQL | campaign > 1 OR previous > 0 |
| `pdays`, `poutcome` | SQL | pdays ≠ -1 OR poutcome = 'success' |
| `y = yes` | Subscriber (Customer) | Subscribed to term deposit |

---

## 📁 Project Structure

```
FUTURE_DS_03/
│
├── funnel_dashboard.py          ← 🚀 Main app — run this
│
├── data/
│   ├── bank_marketing.csv       ← Real dataset (UCI, 45 211 records, 17 cols)
│   ├── sample_funnel_data.csv   ← Pre-aggregated funnel format (alternative)
│   └── data_dictionary.md       ← All column definitions
│
├── notebooks/
│   └── analysis.ipynb           ← Full EDA notebook
│
├── assets/                      ← Screenshots / exports
├── outputs/                     ← Generated HTML / PNG outputs
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/singhdaksh7/FUTURE_DS_03.git
cd FUTURE_DS_03

# 2. Install
pip install -r requirements.txt

# 3. Run
python funnel_dashboard.py

# 4. Open browser
# http://127.0.0.1:8050
```

---

## 📂 Dataset

**Bank Marketing Campaign Dataset**  
Source: [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/222/bank+marketing)  

| Property | Value |
|----------|-------|
| Records  | 45,211 |
| Features | 16 input + 1 target |
| Target   | `y` — did client subscribe to term deposit? (yes/no) |
| Domain   | Portuguese banking institution, direct marketing campaigns |

### Key Columns Used

| Column | Description |
|--------|-------------|
| `contact` | Communication type → mapped to funnel channel |
| `month` | Month of last contact → time axis |
| `duration` | Last call duration (seconds) → lead quality signal |
| `campaign` | Contacts during this campaign → MQL indicator |
| `previous` | Contacts before this campaign → re-engagement |
| `pdays` | Days since previously contacted |
| `poutcome` | Previous campaign outcome |
| `y` | Target: subscribed (yes/no) |
| `age`, `job`, `balance` | Demographic features for deep-dive |

---

## 📊 Dashboard Sections

| Section | What You See |
|---------|-------------|
| **KPIs** | 10 cards — Contacted, Leads, MQLs, SQLs, Subscribers, Revenue, CVR, Best/Worst channel |
| **Funnel** | Conversion funnel with % at every stage |
| **Monthly Trend** | Contacted vs Subscribers over time (dual-axis) |
| **Channel CVR** | Subscription CVR by contact method |
| **Revenue Bar** | Estimated revenue by channel |
| **Subscriber Pie** | Customer share breakdown |
| **Stage Drop-off** | Grouped bar — conversion at each stage per channel |
| **Revenue Trend** | Monthly estimated revenue area chart |
| **Age Distribution** | Subscribed vs Not — age histogram overlay |
| **Call Duration Box** | Duration distribution by outcome |
| **Job Subscription Rate** | Which job categories convert best |
| **Monthly Table** | Full data table with CVR % |
| **Insights Panel** | 8 data-driven recommendation cards |

---

## 📈 Key Results (45,211 records)

| KPI | Value |
|-----|-------|
| Total Records | 45,211 |
| Leads (duration > 0) | ~43,000+ |
| Subscribers | ~10,000+ |
| Best Channel | Mobile / Cellular |
| Strongest Predictor | Call Duration |
| Best Job Segment | Student / Retired |

---

## 🛠️ Tech Stack

| Tool | Use |
|------|-----|
| **Python 3.9+** | Core language |
| **Pandas + NumPy** | Data wrangling & metrics |
| **Plotly** | 11 interactive charts |
| **Dash** | Live web dashboard |
| **Dash Bootstrap Components** | Responsive layout |
| **Jupyter Notebook** | EDA documentation |

---

## 👤 Author

**Daksh Singh**  
Founder — Zip Innovate Technology  
Data Science & Analytics Intern — Future Interns (2026)  
GitHub: [@singhdaksh7](https://github.com/singhdaksh7)

---

`data-science` `marketing-analytics` `funnel-analysis` `plotly-dash` `python`  
`bank-marketing` `uci-dataset` `conversion-optimization` `future-interns`
