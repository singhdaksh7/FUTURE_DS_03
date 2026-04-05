"""
╔══════════════════════════════════════════════════════════════════════════╗
║  Marketing Funnel & Conversion Performance Dashboard                    ║
║  Future Interns – Data Science & Analytics · Task 3 · 2026             ║
║  Author  : Daksh Singh · Zip Innovate Technology                        ║
║  Dataset : Bank Marketing Campaign · UCI ML Repository · 45,211 records ║
║                                                                          ║
║  RUN:                                                                    ║
║    pip install -r requirements.txt                                       ║
║    python funnel_dashboard.py                                            ║
║    Open → http://127.0.0.1:8050                                         ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

# ─── LOAD DATASET ─────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data", "bank_marketing.csv")

raw = pd.read_csv(CSV_PATH)
raw.columns = [c.strip().lower() for c in raw.columns]

print(f"✅ Dataset loaded: {len(raw):,} records × {len(raw.columns)} columns")

# ─── FUNNEL MAPPING ───────────────────────────────────────────────────────────
#
#  bank-marketing column  →  funnel stage
#  ─────────────────────────────────────────────────────────────
#  All records            →  Contacted  (Visitors)
#  duration > 0           →  Lead       (engaged in conversation)
#  campaign>1 | prev>0    →  MQL        (multi-touch / known contact)
#  pdays≠-1 | poutcome=success → SQL   (previously successful / tracked)
#  y = "yes"              →  Subscriber (Customer / converted)

MONTH_ORDER = ["jan","feb","mar","apr","may","jun",
               "jul","aug","sep","oct","nov","dec"]
MONTH_LABEL = {m: m.capitalize() for m in MONTH_ORDER}

CHANNEL_MAP = {
    "cellular":  "Mobile / Cellular",
    "telephone": "Landline / Telephone",
    "unknown":   "Unknown / Direct",
}

raw["channel"]     = raw["contact"].map(CHANNEL_MAP).fillna("Other")
raw["month_key"]   = raw["month"].str.lower()
raw["is_visitor"]  = 1
raw["is_lead"]     = (raw["duration"] > 0).astype(int)
raw["is_mql"]      = ((raw["campaign"] > 1) | (raw["previous"] > 0)).astype(int)
raw["is_sql"]      = ((raw["pdays"] != -1) | (raw["poutcome"] == "success")).astype(int)
raw["is_customer"] = (raw["y"] == "yes").astype(int)

# Revenue proxy: subscribed × ₹12,000 scaled by balance quartile
# Revenue proxy: subscribed x 12,000 scaled by balance tier
bal_q = pd.cut(raw["balance"].clip(lower=0), bins=[-1, 0, 1000, 5000, 999999],
               labels=[0.6, 0.8, 1.0, 1.3]).astype(float).fillna(0.6)
raw["revenue"] = raw["is_customer"] * 12_000 * bal_q

# ─── AGGREGATE TABLES ─────────────────────────────────────────────────────────

# Monthly funnel
monthly = (raw.groupby("month_key", sort=False)
              .agg(visitors  = ("is_visitor",  "sum"),
                   leads     = ("is_lead",     "sum"),
                   mqls      = ("is_mql",      "sum"),
                   sqls      = ("is_sql",      "sum"),
                   customers = ("is_customer", "sum"),
                   revenue   = ("revenue",     "sum"))
              .reset_index())
monthly["_ord"]  = monthly["month_key"].apply(
    lambda m: MONTH_ORDER.index(m) if m in MONTH_ORDER else 99)
monthly = monthly.sort_values("_ord").reset_index(drop=True)
monthly["month"] = monthly["month_key"].map(MONTH_LABEL).fillna(
    monthly["month_key"].str.capitalize())
monthly.drop(columns=["month_key", "_ord"], inplace=True)
monthly["cvr"] = (monthly["customers"] / monthly["visitors"].replace(0, np.nan) * 100).round(3)

# Channel funnel
by_channel = (raw.groupby("channel")
                 .agg(visitors  = ("is_visitor",  "sum"),
                      leads     = ("is_lead",     "sum"),
                      mqls      = ("is_mql",      "sum"),
                      sqls      = ("is_sql",      "sum"),
                      customers = ("is_customer", "sum"),
                      revenue   = ("revenue",     "sum"))
                 .reset_index())
by_channel["cvr"] = (by_channel["customers"] / by_channel["visitors"].replace(0, np.nan) * 100).round(3)

# ─── KPI NUMBERS ──────────────────────────────────────────────────────────────
TV  = int(raw["is_visitor"].sum())
TL  = int(raw["is_lead"].sum())
TQ  = int(raw["is_mql"].sum())
TS  = int(raw["is_sql"].sum())
TC  = int(raw["is_customer"].sum())
TR  = raw["revenue"].sum()
CVR = round(TC / TV * 100, 3)
V2L = round(TL / TV * 100, 1)

BEST  = by_channel.loc[by_channel["cvr"].idxmax()]
WORST = by_channel.loc[by_channel["cvr"].idxmin()]

AVG_DUR_YES = int(raw[raw["y"] == "yes"]["duration"].mean())
AVG_DUR_NO  = int(raw[raw["y"] == "no"]["duration"].mean())
BEST_JOB    = raw.groupby("job")["is_customer"].mean().idxmax()

print(f"   Overall CVR  : {CVR}%")
print(f"   Best channel : {BEST['channel']} ({BEST['cvr']:.2f}%)")
print(f"   Best job     : {BEST_JOB}")

# ─── DESIGN TOKENS ────────────────────────────────────────────────────────────
BG, CARD, GRID = "#05080f", "#0b1120", "#141d2f"
BORDER         = "#1e2d47"
C1, C2, C3, C4, C5 = "#00e5ff", "#7c3aed", "#f59e0b", "#10b981", "#f43f5e"
MUTED, WHITE   = "#8b9ab5", "#e8edf5"

CH_COLORS = {
    "Mobile / Cellular":    C1,
    "Landline / Telephone": C2,
    "Unknown / Direct":     C3,
    "Other":                "#8b5cf6",
}

PBASE = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=WHITE, family="'DM Sans',sans-serif", size=12),
    margin=dict(l=14, r=14, t=36, b=14),
)
AX = dict(gridcolor=GRID, tickfont=dict(color=MUTED),
          linecolor=BORDER, zerolinecolor=BORDER)
CFG = {"displaylogo": False, "modeBarButtonsToRemove": ["select2d", "lasso2d"]}


def cc(name): return CH_COLORS.get(name, "#8b5cf6")


# ─── CHARTS ───────────────────────────────────────────────────────────────────

def make_funnel():
    fig = go.Figure(go.Funnel(
        y=["Contacted", "Leads", "MQLs", "SQLs", "Subscribers"],
        x=[TV, TL, TQ, TS, TC],
        texttemplate="%{value:,.0f}<br>(%{percentInitial:.1%})",
        textposition="inside",
        textfont=dict(size=13, color=WHITE, family="'DM Mono',monospace"),
        marker=dict(color=[C1, "#38b2f9", C2, "#a855f7", C3], line=dict(width=0)),
        connector=dict(line=dict(color=GRID, width=2)),
    ))
    layout = {**PBASE}
    layout["margin"] = dict(l=120, r=30, t=44, b=14)
    layout["height"]  = 420
    layout["title"]   = dict(text="Conversion Funnel — All 45,211 Records",
                              x=.02, font=dict(size=13, color=MUTED))
    fig.update_layout(**layout)
    return fig


def make_trend():
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(
        x=monthly["month"], y=monthly["visitors"], name="Contacted",
        line=dict(color=C1, width=2.5),
        fill="tozeroy", fillcolor="rgba(0,229,255,.06)"), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=monthly["month"], y=monthly["customers"], name="Subscribers",
        line=dict(color=C3, width=2.5),
        mode="lines+markers", marker=dict(size=7)), secondary_y=True)
    layout = {**PBASE}
    layout["margin"] = dict(l=14, r=60, t=70, b=14)
    layout["height"]  = 420
    layout["legend"]  = dict(
        bgcolor="rgba(11,17,32,0.85)",
        bordercolor=BORDER, borderwidth=1,
        orientation="h", y=1.08, x=0,
        font=dict(size=11, color=WHITE),
    )
    layout["title"] = dict(text="Monthly Contacted vs Subscribers",
                           x=.02, font=dict(size=13, color=MUTED), y=0.97)
    fig.update_layout(**layout)
    fig.update_xaxes(**AX, tickangle=-30)
    fig.update_yaxes(**AX, secondary_y=False, title_text="Contacted",
                     title_font=dict(color=C1, size=11))
    fig.update_yaxes(**AX, secondary_y=True, title_text="Subscribers",
                     showgrid=False, title_font=dict(color=C3, size=11))
    return fig


def make_channel_cvr():
    t = by_channel.sort_values("cvr", ascending=False)
    fig = go.Figure(go.Bar(
        x=t["channel"], y=t["cvr"],
        marker_color=[cc(c) for c in t["channel"]],
        text=[f"{v:.2f}%" for v in t["cvr"]],
        textposition="outside", textfont=dict(color=WHITE),
    ))
    fig.update_layout(**PBASE, height=310,
                      title=dict(text="Subscription CVR by Channel",
                                 x=.02, font=dict(size=13, color=MUTED)))
    fig.update_xaxes(**AX)
    fig.update_yaxes(**AX, title_text="CVR %")
    return fig


def make_channel_rev():
    t = by_channel.sort_values("revenue")
    fig = go.Figure(go.Bar(
        y=t["channel"], x=t["revenue"], orientation="h",
        marker_color=[cc(c) for c in t["channel"]],
        text=[f"₹{v:,.0f}" for v in t["revenue"]],
        textposition="outside", textfont=dict(color=WHITE),
    ))
    fig.update_layout(**PBASE, height=280,
                      title=dict(text="Est. Revenue by Channel",
                                 x=.02, font=dict(size=13, color=MUTED)))
    fig.update_xaxes(**AX)
    fig.update_yaxes(**AX)
    return fig


def make_pie():
    fig = go.Figure(go.Pie(
        labels=by_channel["channel"], values=by_channel["customers"], hole=.52,
        marker=dict(colors=[cc(c) for c in by_channel["channel"]],
                    line=dict(color=CARD, width=2)),
        textfont=dict(color=WHITE, size=11),
    ))
    fig.update_layout(**PBASE, height=280,
                      legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=MUTED)),
                      title=dict(text="Subscriber Share by Channel",
                                 x=.02, font=dict(size=13, color=MUTED)))
    return fig


def make_stages():
    stage_labels = ["Contacted→Lead", "Lead→MQL", "MQL→SQL", "SQL→Sub"]
    fig = go.Figure()
    for ch in by_channel["channel"]:
        s = raw[raw["channel"] == ch]
        rates = [
            s["is_lead"].sum()     / max(s["is_visitor"].sum(), 1),
            s["is_mql"].sum()      / max(s["is_lead"].sum(),    1),
            s["is_sql"].sum()      / max(s["is_mql"].sum(),     1),
            s["is_customer"].sum() / max(s["is_sql"].sum(),     1),
        ]
        fig.add_trace(go.Bar(
            name=ch, x=stage_labels,
            y=[round(r * 100, 1) for r in rates],
            marker_color=cc(ch),
        ))
    fig.update_layout(**PBASE, barmode="group", height=340,
                      legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=-0.28, x=0),
                      title=dict(text="Stage-by-Stage Drop-off by Channel",
                                 x=.02, font=dict(size=13, color=MUTED)))
    fig.update_xaxes(**AX)
    fig.update_yaxes(**AX, title_text="Rate %")
    return fig


def make_rev_trend():
    fig = go.Figure(go.Scatter(
        x=monthly["month"], y=monthly["revenue"],
        fill="tozeroy", fillcolor="rgba(124,58,237,.12)",
        line=dict(color=C2, width=2.5),
        mode="lines+markers", marker=dict(color=C2, size=7, line=dict(color=CARD, width=2)),
    ))
    fig.update_layout(**PBASE, height=280,
                      title=dict(text="Monthly Estimated Revenue (₹)",
                                 x=.02, font=dict(size=13, color=MUTED)))
    fig.update_xaxes(**AX)
    fig.update_yaxes(**AX)
    return fig


def make_age_dist():
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=raw[raw["y"]=="no"]["age"],  name="Not Subscribed",
                               marker_color="rgba(244,63,94,.55)", nbinsx=30))
    fig.add_trace(go.Histogram(x=raw[raw["y"]=="yes"]["age"], name="Subscribed",
                               marker_color="rgba(0,229,255,.75)", nbinsx=30))
    fig.update_layout(**PBASE, barmode="overlay", height=300,
                      legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=1.15),
                      title=dict(text="Age Distribution by Outcome",
                                 x=.02, font=dict(size=13, color=MUTED)))
    fig.update_xaxes(**AX, title_text="Age")
    fig.update_yaxes(**AX, title_text="Count")
    return fig


def make_duration_box():
    fig = go.Figure()
    for label, name, color in [("yes","Subscribed",C1), ("no","Not Subscribed",C5)]:
        fig.add_trace(go.Box(
            y=raw[raw["y"]==label]["duration"].clip(upper=2000),
            name=name, marker_color=color, line_color=color,
            fillcolor='rgba(0,229,255,0.1)' if color == C1 else 'rgba(244,63,94,0.1)',
        ))
    fig.update_layout(**PBASE, height=300,
                      legend=dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=1.15),
                      title=dict(text="Call Duration vs Outcome",
                                 x=.02, font=dict(size=13, color=MUTED)))
    fig.update_xaxes(**AX)
    fig.update_yaxes(**AX, title_text="Duration (sec)")
    return fig


def make_job_bar():
    g = (raw.groupby("job")["is_customer"]
            .mean().mul(100).reset_index()
            .rename(columns={"is_customer":"sub_rate"})
            .sort_values("sub_rate", ascending=True))
    fig = go.Figure(go.Bar(
        y=g["job"], x=g["sub_rate"], orientation="h",
        marker_color=C4,
        text=[f"{v:.1f}%" for v in g["sub_rate"]],
        textposition="outside", textfont=dict(color=WHITE),
    ))
    fig.update_layout(**PBASE, height=350,
                      title=dict(text="Subscription Rate by Job (%)",
                                 x=.02, font=dict(size=13, color=MUTED)))
    fig.update_xaxes(**AX, title_text="%")
    fig.update_yaxes(**AX)
    return fig


def make_monthly_cvr():
    fig = go.Figure(go.Bar(
        x=monthly["month"], y=monthly["cvr"],
        marker_color=[C1 if v >= monthly["cvr"].mean() else C5 for v in monthly["cvr"]],
        text=[f"{v:.2f}%" for v in monthly["cvr"]],
        textposition="outside", textfont=dict(color=WHITE),
    ))
    fig.update_layout(**PBASE, height=290,
                      title=dict(text="Monthly CVR % (above/below average)",
                                 x=.02, font=dict(size=13, color=MUTED)))
    fig.update_xaxes(**AX)
    fig.update_yaxes(**AX, title_text="CVR %")
    return fig


# ─── LAYOUT HELPERS ───────────────────────────────────────────────────────────
CARD_S = {"background": CARD, "border": f"1px solid {BORDER}",
          "borderRadius": "14px", "padding": "20px"}
KPI_S  = {"background": CARD, "border": f"1px solid {BORDER}",
          "borderRadius": "14px", "padding": "16px 18px",
          "position": "relative", "minHeight": "108px"}


def badge(text, color):
    r, g, b = int(color[1:3],16), int(color[3:5],16), int(color[5:7],16)
    return html.Span(text, style={
        "padding":"4px 12px","borderRadius":"20px","fontSize":".72rem",
        "fontWeight":"600","letterSpacing":".5px","textTransform":"uppercase",
        "background":f"rgba({r},{g},{b},.13)","color":color,
        "border":f"1px solid rgba({r},{g},{b},.28)",
    })


def kpi_card(label, value, sub, accent=C1):
    # Pick font size based on value length so nothing overflows
    vlen = len(str(value))
    vsize = "1.5rem" if vlen <= 8 else ("1.15rem" if vlen <= 14 else "0.95rem")
    return html.Div([
        html.Div(style={"position":"absolute","top":"0","left":"0","right":"0","height":"2px",
                        "background":f"linear-gradient(90deg,{accent},transparent)",
                        "borderRadius":"14px 14px 0 0"}),
        html.Div(label, style={"fontSize":".65rem","color":MUTED,"textTransform":"uppercase",
                               "letterSpacing":".7px","marginBottom":"6px",
                               "whiteSpace":"nowrap","overflow":"hidden","textOverflow":"ellipsis"}),
        html.Div(value, style={"fontSize":vsize,"fontWeight":"800","color":WHITE,
                               "lineHeight":"1.1","fontFamily":"'Syne',sans-serif",
                               "wordBreak":"break-word"}),
        html.Div(sub,   style={"fontSize":".68rem","color":MUTED,"marginTop":"5px",
                               "lineHeight":"1.3"}),
    ], style=KPI_S)


def sec(txt):
    return html.Div([
        html.Span(txt, style={"fontFamily":"'Syne',sans-serif","fontSize":".78rem",
                              "fontWeight":"700","textTransform":"uppercase",
                              "letterSpacing":"2px","color":MUTED}),
        html.Div(style={"flex":"1","height":"1px","background":BORDER}),
    ], style={"display":"flex","alignItems":"center","gap":"14px","margin":"30px 0 14px"})


def ins_card(color, icon, title, body):
    r, g, b = int(color[1:3],16), int(color[3:5],16), int(color[5:7],16)
    return html.Div([
        html.Div(icon, style={"width":"38px","height":"38px","borderRadius":"10px",
                              "fontSize":"1.1rem","flexShrink":"0",
                              "display":"flex","alignItems":"center","justifyContent":"center",
                              "background":f"rgba({r},{g},{b},.12)"}),
        html.Div([
            html.Div(title, style={"fontFamily":"'Syne',sans-serif","fontWeight":"700",
                                   "fontSize":".84rem","marginBottom":"5px"}),
            html.Div(body,  style={"fontSize":".76rem","color":MUTED,"lineHeight":"1.55"}),
        ]),
    ], style={"display":"flex","gap":"12px","alignItems":"flex-start",
              "background":CARD,"border":f"1px solid {BORDER}",
              "borderRadius":"14px","padding":"16px 18px"})


# ─── BUILD MONTHLY TABLE ──────────────────────────────────────────────────────
tbl_df = monthly[["month","visitors","leads","customers","revenue","cvr"]].copy()
tbl_df.columns = ["Month","Contacted","Leads","Subscribers","Est. Revenue (₹)","CVR %"]
tbl_df["Est. Revenue (₹)"] = tbl_df["Est. Revenue (₹)"].apply(lambda x: f"₹{x:,.0f}")

# ─── APP LAYOUT ───────────────────────────────────────────────────────────────
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800"
        "&family=DM+Sans:wght@300;400;500"
        "&family=DM+Mono:wght@400;500&display=swap",
    ],
    title="Funnel Dashboard · Future Interns Task 3",
)

app.layout = html.Div(
    style={"backgroundColor": BG, "minHeight": "100vh",
           "fontFamily": "'DM Sans',sans-serif", "color": WHITE},
    children=[

        # ── HEADER ────────────────────────────────────────────────────────────
        html.Div(style={
            "background": f"linear-gradient(135deg,{CARD} 0%,#0d1628 100%)",
            "borderBottom": f"1px solid {BORDER}",
            "padding": "22px 40px",
            "display": "flex", "alignItems": "center",
            "justifyContent": "space-between", "flexWrap": "wrap", "gap": "14px",
        }, children=[
            html.Div([
                html.Div("📊", style={
                    "width":"44px","height":"44px","borderRadius":"10px","fontSize":"22px",
                    "background":f"linear-gradient(135deg,{C1},{C2})",
                    "display":"flex","alignItems":"center","justifyContent":"center",
                }),
                html.Div([
                    html.H1("Marketing Funnel & Conversion Dashboard", style={
                        "fontFamily":"'Syne',sans-serif","fontSize":"1.15rem",
                        "fontWeight":"800","margin":"0","letterSpacing":"-.3px",
                    }),
                    html.P(
                        "Future Interns · Data Science & Analytics · Task 3 · 2026  |  "
                        "Bank Marketing Campaign Dataset · UCI ML Repository · 45,211 records",
                        style={"fontSize":".72rem","color":MUTED,"margin":"2px 0 0"}),
                ]),
            ], style={"display":"flex","alignItems":"center","gap":"14px"}),
            html.Div([
                badge("Task 3", C1),
                badge("45,211 Records", C2),
                badge("UCI ML Repo", C3),
                badge("Bank Marketing", C4),
            ], style={"display":"flex","gap":"8px","flexWrap":"wrap"}),
        ]),

        # ── BODY ──────────────────────────────────────────────────────────────
        html.Div(style={"padding":"26px 36px","maxWidth":"1600px","margin":"0 auto"},
                 children=[

            # KPIs
            sec("📊  Key Performance Indicators"),
            # KPI row 1 — funnel numbers
            html.Div(style={
                "display":"grid",
                "gridTemplateColumns":"repeat(5,1fr)",
                "gap":"12px",
                "marginBottom":"12px",
            }, children=[
                kpi_card("Total Contacted",   f"{TV:,}",     "All outreach records",   C1),
                kpi_card("Total Leads",       f"{TL:,}",     "Duration > 0 sec",       C2),
                kpi_card("MQLs",              f"{TQ:,}",     "Multi-touch / previous", C3),
                kpi_card("SQLs",              f"{TS:,}",     "Prev. contacted/success",C4),
                kpi_card("Subscribers",       f"{TC:,}",     "Converted (y = yes)",    C1),
            ]),
            # KPI row 2 — performance metrics
            html.Div(style={
                "display":"grid",
                "gridTemplateColumns":"repeat(5,1fr)",
                "gap":"12px",
            }, children=[
                kpi_card("Est. Revenue",      f"₹{TR:,.0f}", "Term deposit proxy",     C2),
                kpi_card("Overall CVR",       f"{CVR}%",     "Contact → Subscriber",   C3),
                kpi_card("Contact→Lead",      f"{V2L}%",     "Top-of-funnel rate",     C4),
                kpi_card("Best Channel",      BEST["channel"],  f"CVR {BEST['cvr']:.2f}%",  C4),
                kpi_card("Worst Channel",     WORST["channel"], f"CVR {WORST['cvr']:.2f}%", C5),
            ]),

            # Funnel + Trend
            sec("🔻  Conversion Funnel & Monthly Trends"),
            dbc.Row([
                dbc.Col(html.Div(style={**CARD_S, "padding":"16px 16px 8px"}, children=[
                    dcc.Graph(figure=make_funnel(), config=CFG)]), md=5),
                dbc.Col(html.Div(style={**CARD_S, "padding":"16px 16px 8px"}, children=[
                    dcc.Graph(figure=make_trend(),  config=CFG)]), md=7),
            ], className="g-3 mb-3"),

            # Channel performance
            sec("📣  Channel Performance"),
            dbc.Row([
                dbc.Col(html.Div(style=CARD_S, children=[
                    dcc.Graph(figure=make_channel_cvr(), config=CFG)]), md=5),
                dbc.Col(html.Div(style=CARD_S, children=[
                    dcc.Graph(figure=make_channel_rev(), config=CFG)]), md=4),
                dbc.Col(html.Div(style=CARD_S, children=[
                    dcc.Graph(figure=make_pie(),         config=CFG)]), md=3),
            ], className="g-3 mb-3"),

            # Drop-off + Revenue
            sec("📉  Stage Drop-off & Revenue Trend"),
            dbc.Row([
                dbc.Col(html.Div(style=CARD_S, children=[
                    dcc.Graph(figure=make_stages(),    config=CFG)]), md=8),
                dbc.Col(html.Div(style=CARD_S, children=[
                    dcc.Graph(figure=make_rev_trend(), config=CFG)]), md=4),
            ], className="g-3 mb-3"),

            # Deep-dive
            sec("🔬  Deep-Dive Analysis"),
            dbc.Row([
                dbc.Col(html.Div(style=CARD_S, children=[
                    dcc.Graph(figure=make_age_dist(),     config=CFG)]), md=4),
                dbc.Col(html.Div(style=CARD_S, children=[
                    dcc.Graph(figure=make_duration_box(), config=CFG)]), md=4),
                dbc.Col(html.Div(style=CARD_S, children=[
                    dcc.Graph(figure=make_monthly_cvr(),  config=CFG)]), md=4),
            ], className="g-3 mb-3"),

            dbc.Row([
                dbc.Col(html.Div(style=CARD_S, children=[
                    dcc.Graph(figure=make_job_bar(), config=CFG)]), md=12),
            ], className="g-3 mb-3"),

            # Monthly table
            sec("📋  Monthly Funnel Table"),
            html.Div(style={**CARD_S, "overflowX":"auto"}, children=[
                dash_table.DataTable(
                    data=tbl_df.to_dict("records"),
                    columns=[{"name": c, "id": c} for c in tbl_df.columns],
                    style_table={"overflowX":"auto"},
                    style_header={
                        "backgroundColor": GRID, "color": MUTED, "fontWeight": "700",
                        "fontSize": "11px", "textTransform": "uppercase",
                        "letterSpacing": "0.8px", "border": f"1px solid {BORDER}",
                    },
                    style_cell={
                        "backgroundColor": CARD, "color": WHITE,
                        "border": f"1px solid {BORDER}", "fontSize": "13px",
                        "padding": "11px 14px", "fontFamily": "'DM Mono',monospace",
                    },
                    style_data_conditional=[
                        {"if":{"row_index":"odd"}, "backgroundColor":"#0d1525"}
                    ],
                    page_size=15,
                )
            ]),

            # Insights
            sec("💡  Insights & Recommendations"),
            html.Div(style={
                "display":"grid",
                "gridTemplateColumns":"repeat(auto-fit,minmax(268px,1fr))",
                "gap":"12px",
            }, children=[
                ins_card(C5, "🚨", "Biggest Drop-off: Contact → Lead",
                    f"Only {V2L:.1f}% of contacts result in a lead (call duration > 0). "
                    f"Training agents to extend conversations past {AVG_DUR_YES}s "
                    "can dramatically improve this rate."),
                ins_card(C1, "🏆", f"Best Channel: {BEST['channel']}",
                    f"{BEST['channel']} achieves {BEST['cvr']:.2f}% CVR — the highest. "
                    "Shift outreach budget toward this channel for maximum ROI."),
                ins_card(C5, "📉", f"Underperforming: {WORST['channel']}",
                    f"{WORST['channel']} converts at only {WORST['cvr']:.2f}%. "
                    "Audit call scripts and qualification criteria for this channel."),
                ins_card(C3, "⏱️", "Call Duration = Strongest Predictor",
                    f"Subscribers average {AVG_DUR_YES}s per call vs "
                    f"{AVG_DUR_NO}s for non-subscribers "
                    f"({round((AVG_DUR_YES/max(AVG_DUR_NO,1)-1)*100)}% longer). "
                    "Invest in call quality training."),
                ins_card(C4, "👷", f"Top Job Segment: {BEST_JOB.capitalize()}",
                    f'"{BEST_JOB}" shows the highest subscription rate in the dataset. '
                    "Prioritize this segment when building outreach lists."),
                ins_card(C2, "📅", "May Campaign Dominates Volume",
                    "~31% of contacts happen in May. Pre-load campaign materials and "
                    "agent capacity 4–6 weeks early to avoid conversion loss from overload."),
                ins_card(C1, "🔁", "Re-contact Strategy Works",
                    "Records with previous > 0 show higher MQL and SQL conversion. "
                    "Build structured multi-touch sequences for lapsed contacts."),
                ins_card(C4, "💡", "Cellular Beats Telephone",
                    "Mobile / Cellular contacts consistently outperform landline in CVR. "
                    "Invest in mobile number data enrichment for your contact lists."),
            ]),

            # Footer
            html.Div(style={
                "textAlign":"center","padding":"28px 0 12px",
                "color":MUTED,"fontSize":".75rem",
                "borderTop":f"1px solid {BORDER}","marginTop":"30px",
            }, children=[
                html.Span("Built by "),
                html.Strong("Daksh Singh", style={"color":C1}),
                html.Span(" · Zip Innovate Technology · Future Interns Task 3 · 2026  |  "
                          "Dataset: Bank Marketing Campaign · UCI ML Repository · 45,211 records"),
            ]),
        ]),
    ]
)

# ─── RUN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║  Marketing Funnel Dashboard — Future Interns Task 3          ║
║  Dataset : Bank Marketing Campaign (UCI · 45,211 records)    ║
║  Open    : http://127.0.0.1:8050                             ║
║  Stop    : Ctrl+C                                            ║
╚══════════════════════════════════════════════════════════════╝
    """)
    app.run(debug=True, host="127.0.0.1", port=8050)
