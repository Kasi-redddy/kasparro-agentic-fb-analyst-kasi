import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime

REQUIRED_COLUMNS = [
    "campaign_name", "adset_name", "date", "spend", "impressions", "clicks", "ctr",
    "purchases", "revenue", "roas", "creative_type", "creative_message",
    "audience_type", "platform", "country"
]

def normalize_columns(df):
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]
    return df

def check_columns(df):
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    return missing

def planner_agent(user_query):
    return [
        "Summarize ROAS trends and detect drop periods.",
        "Identify likely drivers for ROAS changes (audience fatigue, creative type, etc.).",
        "Find campaigns with low CTR and generate message recommendations."
    ]

def data_agent(df):
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    summary = {
        "n_rows": len(df),
        "columns": list(df.columns),
        "date_range": [str(df['date'].min()) if 'date' in df.columns else "N/A",
                       str(df['date'].max()) if 'date' in df.columns else "N/A"],
        "min_roas": float(df['roas'].min()) if 'roas' in df.columns else "N/A",
        "max_roas": float(df['roas'].max()) if 'roas' in df.columns else "N/A",
        "avg_roas": float(df['roas'].mean()) if 'roas' in df.columns else "N/A"
    }
    return summary

def insight_agent(df):
    insights = []
    if ('date' in df.columns) and ('roas' in df.columns) and ('ctr' in df.columns):
        roas_by_date = df.groupby('date')['roas'].mean()
        roas_deltas = roas_by_date.diff()
        drop_dates = roas_deltas[roas_deltas < -0.5].index
        for d in drop_dates:
            insights.append({
                "hypothesis": f"ROAS drop detected on {d.strftime('%Y-%m-%d')}",
                "confidence": "medium",
                "evidence": f"ROAS delta: {roas_deltas[d]:.2f} on {d.strftime('%Y-%m-%d')}"
            })
        low_ctr = df[df["ctr"] < 0.015]
        for _, row in low_ctr.iterrows():
            insights.append({
                "hypothesis": f"Underperformance likely in creative for campaign {row['campaign_name']} on {row['date'].strftime('%Y-%m-%d')}",
                "confidence": "medium" if row['ctr'] < 0.012 else "low",
                "evidence": f"Creative '{row['creative_message']}' has low CTR {row['ctr']:.3f}, creative type: {row['creative_type']}"
            })
    return insights

def evaluator_agent(insights, df):
    for h in insights:
        if "ROAS drop" in h["hypothesis"]:
            date_str = h["hypothesis"].split("on")[-1].strip()
            drop_date = pd.to_datetime(date_str)
            pre = df[df["date"] < drop_date].tail(7)
            after = df[df["date"] == drop_date]
            if len(pre) > 0 and len(after) > 0 and after["roas"].mean() < pre["roas"].mean() * 0.8:
                h["validated"] = True
                h["validation_confidence"] = "high"
            else:
                h["validated"] = False
                h["validation_confidence"] = "low"
        else:
            h["validated"] = h.get("confidence", "low") == "medium"
            h["validation_confidence"] = h.get("confidence", "low")
    return insights

def creative_generator_agent(df):
    output = []
    mean_ctr = df["ctr"].mean() if "ctr" in df.columns else 0.02
    if set(['ctr', 'creative_message', 'campaign_name', 'date', 'creative_type', 'audience_type']).issubset(df.columns):
        low_ctr = df[df["ctr"] < 0.015].drop_duplicates(subset=["creative_message"])
        for _, row in low_ctr.iterrows():
            relevant = df[
                (df["ctr"] > mean_ctr * 1.2) &
                (df["creative_type"] == row["creative_type"]) &
                (df["audience_type"] == row["audience_type"])
            ]
            top_msgs = relevant["creative_message"].value_counts().index[:2].tolist()
            suggestions = []
            for msg in top_msgs:
                suggestions.append(f"Reference similar successful creative: '{msg}'")
            if not suggestions:
                suggestions.append("Add urgency: e.g. 'Limited Time Offer!'")
            if row["ctr"] < mean_ctr:
                suggestions.append("Highlight offer/discount more explicitly.")
            suggestions = suggestions[:3]
            output.append({
                "campaign": row["campaign_name"],
                "date": row["date"].strftime('%Y-%m-%d') if isinstance(row["date"], pd.Timestamp) else str(row["date"]),
                "old_message": row["creative_message"],
                "suggestions": suggestions
            })
    return output

def create_report(summary, hypotheses, creatives):
    report = "# ROAS Analysis Report\n\n"
    report += "## Data Summary\n"
    report += json.dumps(summary, indent=2) + "\n\n"
    report += "## Insights & Hypotheses\n"
    for h in hypotheses:
        report += f"- {h['hypothesis']} | Confidence: {h['confidence']} | Validated: {h.get('validated', False)} | Evidence: {h['evidence']}\n"
    report += "\n## Creative Suggestions\n"
    for c in creatives:
        report += f"- Campaign: {c['campaign']} (Date: {c['date']})\n  Old Message: '{c['old_message']}'\n  Suggestions:\n"
        for s in c["suggestions"]:
            report += f"    - {s}\n"
    return report

st.title("Kasparro Agentic Facebook Ads Performance Analyst")

uploaded_file = st.file_uploader("Upload your Facebook Ads dataset (CSV)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df = normalize_columns(df)
    missing = check_columns(df)

    if missing:
        st.error(f"Missing columns: {missing}")
        st.write("Detected columns:", list(df.columns))
    else:
        st.success("File loaded successfully! All required columns found.")
        st.dataframe(df.head())
        user_query = st.text_input("Enter your analysis query", "Analyze ROAS drop")

        if st.button("Run Analysis"):
            with st.spinner("Running Agentic System..."):
                plan = planner_agent(user_query)
                summary = data_agent(df)
                insights = insight_agent(df)
                validated = evaluator_agent(insights, df)
                creatives = creative_generator_agent(df)
                report_md = create_report(summary, validated, creatives)

                st.subheader("Planner Agent - Analysis Plan")
                for step in plan:
                    st.write(step)

                st.subheader("Data Agent - Data Summary")
                st.json(summary)

                st.subheader("Insight Agent - Hypotheses")
                for h in validated:
                    st.markdown(f"- **{h['hypothesis']}** (Confidence: {h['confidence']}, Validated: {h.get('validated',False)})")
                    st.markdown(f"  - Evidence: {h['evidence']}")

                st.subheader("Creative Generator Agent - Creative Suggestions")
                for c in creatives:
                    st.markdown(f"- **Campaign:** {c['campaign']} (**Date:** {c['date']})")
                    st.markdown(f"  - Old Message: {c['old_message']}")
                    for s in c["suggestions"]:
                        st.markdown(f"    - {s}")

                st.download_button("Download Insights JSON", data=json.dumps(validated, indent=2), file_name="insights.json", mime="application/json")
                st.download_button("Download Creatives JSON", data=json.dumps(creatives, indent=2), file_name="creatives.json", mime="application/json")
                st.download_button("Download Report (Markdown)", data=report_md, file_name="report.md", mime="text/markdown")

                if ('date' in df.columns and 'roas' in df.columns):
                    st.subheader("ROAS Trend Over Time")
                    roas_by_date = df.groupby('date')['roas'].mean()
                    st.line_chart(roas_by_date)
                if 'ctr' in df.columns:
                    st.subheader("CTR Distribution")
                    st.bar_chart(df['ctr'])
else:
    st.info("Upload a CSV file with the required columns: " + ", ".join(REQUIRED_COLUMNS))
