import pandas as pd
import datetime as dt
import yagmail
import os

# ----------------------
# Set working directory
# ----------------------
os.chdir("file/path")

# ----------------------
# 1. Load data
# ----------------------
df = pd.read_csv("claims_master.csv")
df["admission_date"] = pd.to_datetime(df["admission_date"])

today = dt.date.today()
week_start = today - dt.timedelta(days=7)

# ==========================================
# 2. BASIC DATA QUALITY CHECKS
# ==========================================
dq_issues = {}

# Missing values (column-wise)
missing_counts = df.isnull().sum()
total_missing = int(missing_counts.sum())
dq_issues["Missing Values"] = total_missing  # summary-friendly

# Invalid (negative) claim costs
invalid_costs = df[df["claim_cost"] < 0]
dq_issues["Negative Cost Records"] = len(invalid_costs)

# Future dates
future_dates = df[df["admission_date"].dt.date > today]
dq_issues["Future Date Records"] = len(future_dates)


# ==========================================
# 3. FILTER DATA WINDOWS
# ==========================================
current_week = df[df["admission_date"].dt.date >= week_start]

last_week_start = week_start - dt.timedelta(days=7)
last_week_end = week_start - dt.timedelta(days=1)
previous_week = df[
    (df["admission_date"].dt.date >= last_week_start) &
    (df["admission_date"].dt.date <= last_week_end)
]

mtd = df[df["admission_date"].dt.month == today.month]
ytd = df[df["admission_date"].dt.year == today.year]


def format_currency(x):
    return "${:,.2f}".format(x)


# ==========================================
# 4. ANOMALY DETECTION (Outliers)
# Using simple z-score on cost
# ==========================================
df["cost_zscore"] = (df["claim_cost"] - df["claim_cost"].mean()) / df["claim_cost"].std()
anomalies = df[abs(df["cost_zscore"]) > 3]
anomaly_count = len(anomalies)


# ==========================================
# 5. Top Contributors (Pareto)
# ==========================================
df_sorted = df.sort_values(by="claim_cost", ascending=False)
top_10_percent_count = int(len(df) * 0.10)
top_contributors = df_sorted.head(top_10_percent_count)

top_contribution_value = top_contributors["claim_cost"].sum()
total_cost_overall = df["claim_cost"].sum()

top_contribution_pct = round((top_contribution_value / total_cost_overall) * 100, 2)


# ==========================================
# 6. SUMMARY STATISTICS
# ==========================================
summary = {
    "Total Claims (This Week)": int(len(current_week)),
    "Total Claims (Last Week)": int(len(previous_week)),
    "WoW Growth %": (
        f"{round(((len(current_week) - len(previous_week)) / len(previous_week)) * 100, 2)}%"
        if len(previous_week) > 0 else "NA"
    ),

    # Cost Metrics
    "Total Cost (This Week)": format_currency(current_week["claim_cost"].sum()),
    "Total Cost (Last Week)": format_currency(previous_week["claim_cost"].sum()),
    "Total Cost (MTD)": format_currency(mtd["claim_cost"].sum()),
    "Total Cost (YTD)": format_currency(ytd["claim_cost"].sum()),
    "Avg Cost per Claim (This Week)": format_currency(current_week["claim_cost"].mean()),
    "Avg Cost per Claim (YTD)": format_currency(ytd["claim_cost"].mean()),

    # Data Quality KPIs
    "Missing Data Issues": dq_issues["Missing Values"],
    "Negative Cost Records": dq_issues["Negative Cost Records"],
    "Future Date Records": dq_issues["Future Date Records"],

    # Anomaly Summary
    "Anomalous Claims Count": anomaly_count,

    # Pareto Contribution
    "Top 10% Claims Contribution ($)": format_currency(top_contribution_value),
    "Top 10% Contribution %": f"{top_contribution_pct}%"
}

summary_df = pd.DataFrame(summary.items(), columns=["Metric", "Value"])
print(summary_df)


# ==========================================
# 7. Save output files
# ==========================================
os.makedirs("output", exist_ok=True)

current_week.to_excel("output/weekly_claims.xlsx", index=False)
summary_df.to_excel("output/summary.xlsx", index=False)
anomalies.to_excel("output/anomalies.xlsx", index=False)
top_contributors.to_excel("output/top_contributors.xlsx", index=False)
missing_counts.to_excel("output/missing_data_detail.xlsx")  # detailed DQ file

# ==========================================
# 8. Business Email Automation
# ==========================================

summary_text = f"""
Hi Team,

Please find a brief summary of this week's claims performance. All detailed reports have been included as attachments.

Key Metrics
----------------
This Week's Claims     : {summary['Total Claims (This Week)']}
Last Week's Claims     : {summary['Total Claims (Last Week)']}
WoW Growth             : {summary['WoW Growth %']}
Total Weekly Cost      : {summary['Total Cost (This Week)']}
Average Cost per Claim : {summary['Avg Cost per Claim (This Week)']}

Let me know if you need further detail or a breakdown by specific segments.

Regards,
Andrea
Analytics consultant
"""

yag = yagmail.SMTP("email@id.com", "app passcode") #Enter email id and passcode

yag.send(
    to="stakeholder_email@id.com", #Stakeholder email id
    subject=f"Weekly Claims Summary – {today.strftime('%b %d, %Y')}",
    contents=[summary_text],
    attachments=[
        "output/summary.xlsx",
        "output/top_contributors.xlsx"
    ]
)

print("Email sent successfully!")
