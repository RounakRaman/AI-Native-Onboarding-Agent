# ⚡ Setup Copilot - Streamlit Prototype Application

An AI-Native Onboarding Agent for Agency Project Management Tools (based on the Technical PRD by Rounak Raman).

---

## 🌟 Overview & Key Features

**Setup Copilot** solves the 30-day drop-off problem for agency PM tools by tackling the root causes of early churn:
1. **Empty-State Overwhelm (Problem #1)**: 5-Step guided onboarding wizard (Intake ➔ Import ➔ Scaffold ➔ Invite ➔ Billing Prep) taking teams from blank screen to live client project in under 3 minutes.
2. **Partial Team Activation (Problem #2)**: In-flow team invite pre-populating project-specific land-direct links instead of generic workspace invites.
3. **Switching Cost From Existing Tools (Problem #3)**: CSV import (Trello/Sheets exports) and simulated OAuth import (Jira/GitHub Issues) with auto-task mapping.
4. **Grounded RAG Help Assistant**: Contextual Q&A grounded in Company FAQs + PII-scrubbed historical support tickets with vector similarity retrieval, confidence scoring guardrails (<80 words, UI click paths, fallback support ticket offers), and feedback logging.
5. **Full Agency PM Workspace**: Interactive Kanban task management, time logging against tasks, draft rate card management, and 1-click client invoice generation.
6. **Product Telemetry & A/B Testing Dashboard**: Live tracking of the North Star **7-Day Team Activation Rate** (composite metric: project created + teammate invited + first task completed), per-hypothesis breakdown, guardrails monitoring, and Control vs. Treatment cohort A/B test analytics.

---

## 📁 Repository Structure

```
setup-copilot-app/
├── .streamlit/
│   └── config.toml               # Custom dark/indigo aesthetic theme styling
├── knowledge_base/
│   ├── faqs.json                 # Documented product features & help center articles
│   └── support_tickets.json      # Historical customer support ticket resolutions (PII scrubbed)
├── sample_data/
│   ├── trello_export_sample.csv  # Sample Trello CSV for migration testing
│   └── sheets_export_sample.csv  # Sample Google Sheets CSV for migration testing
├── src/
│   ├── __init__.py
│   ├── copilot.py                # 5-step Setup Copilot onboarding state machine
│   ├── rag_engine.py             # Grounded RAG vector similarity engine & confidence guardrails
│   ├── workspace.py              # Interactive Agency PM Workspace (Tasks, Time, Invoices, Team)
│   ├── telemetry.py              # North Star telemetry dashboard & A/B testing simulator
│   └── utils.py                  # Custom CSS styling and session state management
├── app.py                        # Main Streamlit application entrypoint
├── requirements.txt              # Dependencies for deployment
├── export_zip.py                 # Script generating setup_copilot_streamlit_app.zip
└── README.md                     # Documentation & Deployment Guide
```

---

## 🚀 How to Run Locally

### 1. Prerequisites
Ensure you have Python 3.9+ installed on your system.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch Streamlit Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## ☁️ How to Deploy to Streamlit Community Cloud

1. **Create a GitHub Repository**:
   - Create a new public or private repository on GitHub (e.g. `setup-copilot-app`).
   - Push all code in this repository to GitHub:
     ```bash
     git init
     git add .
     git commit -m "Initial commit of Setup Copilot Streamlit app"
     git branch -M main
     git remote add origin https://github.com/YOUR_USERNAME/setup-copilot-app.git
     git push -u origin main
     ```

2. **Deploy on Streamlit Community Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io) and log in with GitHub.
   - Click **New App**.
   - Select your repository (`setup-copilot-app`), branch (`main`), and main file path (`app.py`).
   - Click **Deploy**! Your app will be live end-to-end within minutes.

---

## 📦 Zip Archive

A deployable zip package `setup_copilot_streamlit_app.zip` containing all source code and datasets is located at the root of the workspace. You can extract it anywhere and upload directly to GitHub or deploy to Streamlit Cloud.
