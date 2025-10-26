# kasparro-agentic-fb-analyst-kasi

**Agentic multi-agent system for autonomous Facebook Ads performance analysis, creative diagnostics, and recommendations.**  
Built for *Kasparro Applied AI Engineer Assignment.*

---

## 🧠 Project Overview
This project implements a multi-agent system that diagnoses Facebook Ads ROAS changes, explains fluctuations, and generates new creative ideas for low-CTR campaigns. It leverages quantitative signals and creative messaging analysis. The app features an interactive Streamlit frontend for intuitive upload, analysis, and reporting.

---

## 🎯 Assignment Goal
- Diagnose why ROAS changed over time  
- Identify drivers behind changes (audience fatigue, creative underperformance, etc.)  
- Propose new creative headlines, messages, CTAs for low-CTR campaigns, using real historic campaign messaging  

---

## 🚀 Features
- Modular agentic design: **Planner, Data Agent, Insight Agent, Evaluator, Creative Generator**  
- Upload and analyze any Facebook Ads dataset (CSV)  
- Table/chart visualizations of ROAS, CTR trends, and creative suggestions  
- Downloadable insights (`insights.json`), creative recommendations (`creatives.json`), and complete report (`report.md`)  
- Layered reasoning and robust validation  
- Fully reproducible and compatible with submission guidelines  

---

## ⚙️ Getting Started

### Prerequisites
- Python 3.8+  
- Recommended: Virtualenv or Conda environment  
- Install required packages:
  \`\`\`bash
  pip install pandas numpy streamlit
  \`\`\`

### Installation
\`\`\`bash
git clone https://github.com/<your-username>/kasparro-agentic-fb-analyst-<firstname-lastname>.git
cd kasparro-agentic-fb-analyst-<firstname-lastname>
\`\`\`

### Run the App
\`\`\`bash
streamlit run app.py
\`\`\`

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📊 Data Format
Your CSV must include:
\`\`\`text
campaign_name, adset_name, date, spend, impressions, clicks, ctr, purchases, revenue, roas, creative_type, creative_message, audience_type, platform, country
\`\`\`
Sample data file available in the repo.

---

## 🧩 Usage Steps
1. Upload your CSV file  
2. Enter your analysis query (e.g., *Analyze ROAS drop*)  
3. Click **Run Analysis**  
4. Review:
   - Planner Agent plan  
   - Data summary  
   - Insights/hypotheses  
   - Validations and recommendations  
5. Download results  

---

## 📁 Output Files
- **insights.json** – Hypotheses for ROAS/CTR patterns  
- **creatives.json** – Improved creative messaging  
- **report.md** – Full markdown report  
- **logs/** – Optional logs of agent outputs  

---

## 🧠 Architecture
**Planner Agent** → breaks down tasks  
**Data Agent** → processes datasets  
**Insight Agent** → identifies causes  
**Evaluator Agent** → validates insights  
**Creative Generator** → crafts better ad ideas  

---

## 💡 Example Output
\`\`\`text
Campaign: Men Premium Modal (Date: 2025-02-28)
Old Message: Breathable organic cotton that moves with you — limited offer on men briefs.
Suggestions:
- Reference similar successful creative: 'Hot & comfy: men boxers now 20% off — feel the difference.'
- Add urgency: 'Limited Time Offer!'
- Highlight offer/discount more explicitly.
\`\`\`

---

## 🔁 Reproducibility
Fully deterministic — outputs can be regenerated from the CSV.

---

## 🤝 Contributing
Pull requests welcome! Ensure code is modular, documented, and test-compatible.

---

## 📜 License
**MIT License**
" > README.md
