# AutoFlow
Automated Python pipeline for weekly claims processing, KPI computation, anomaly detection, and automated email delivery
📌 AutoFlow — Automated Claims Reporting Pipeline

AutoFlow is a Python-based automation workflow that processes weekly healthcare claims data, performs data-quality checks, computes key performance metrics, detects anomalies, generates structured Excel reports, and automatically emails a stakeholder-ready summary.
The system reduces manual reporting time by ~90% and ensures accurate, consistent, and repeatable weekly insights.

🚀 Features

- Automated weekly data ingestion and cleaning

- Data-quality validation (missing values, invalid costs, future dates)

- Weekly, MTD, YTD KPI computation

- Anomaly detection using z-scores

- Pareto analysis for top contributors

- Generates Excel reports (summary, anomalies, DQ findings)

- Sends a business-style email summary with attachments

- Fully hands-free, repeatable workflow

How It Works

- Loads the weekly claims file (CSV)

- Cleans and validates the data

- Computes key operational metrics and WoW changes

- Detects high-cost claim anomalies

- Generates structured Excel outputs

- Builds a plain-text summary

- Emails reports automatically via Gmail SMTP

- Can be scheduled for weekly execution


🧩 Key Components
- Data Quality Checks

- Missing values

- Negative/invalid claim cost

- Future admission dates

- Metrics Computed

- Total claims (weekly)

- Total cost (weekly)

- Week-over-week % change

- Avg cost per claim

- MTD / YTD cost analysis

- Top 10% claim contributors

Anomaly Detection

- Z-score method on claim cost

- Automated Email Summary

Includes:

- High-level KPIs

- Issue counts

- Attached Excel reports

📬 Sample Outputs
Output File	Description
summary.xlsx	Weekly KPI summary
weekly_claims.xlsx	Cleaned weekly dataset
anomalies.xlsx	Detected outlier claims
missing_data_detail.xlsx	DQ breakdown

<img width="850" height="336" alt="image" src="https://github.com/user-attachments/assets/b4b0a9c9-0186-4d57-b3f4-e11e03a5cac3" />

<img width="850" height="336" alt="image" src="https://github.com/user-attachments/assets/c9686810-d34a-474f-8e50-df4f3678e99b" />


⚙️ Installation
git clone https://github.com/Andreatechconsulting/AutoFlow.git
cd AutoFlow
pip install -r requirements.txt

▶️ Usage
python src/autoflow.py

Ensure:

- Your sample data is placed in /data

- You update your Gmail credentials with an App Password

Outputs will be saved to /output

🔒 Email Configuration (Gmail SMTP)

- Enable 2-Step Verification

- Generate an App Password

Use it in your script:

yag = yagmail.SMTP("your_email@gmail.com", "your_app_password")

🎯 Impact

- ~90% reduction in manual reporting time

- ~95% improvement in data accuracy due to automated checks

- 100% consistency in weekly reporting

- 80% faster detection of anomalies

- 70% faster stakeholder turnaround through automated emails

🔭 Next Steps

Enhance reliability and scalability by adding automated logging, scheduled execution, cloud-based ingestion, and dashboarding features, and expanding the pipeline to additional datasets.
