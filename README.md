# 🏠 Real Estate Email Agent

An AI-powered email processing agent for Pakistani real estate agencies. Paste any client email — the agent classifies it, drafts a professional response, flags urgent cases, and logs everything to Google Sheets automatically.

---

## The Problem

Real estate agencies in Pakistan receive dozens of client emails daily — property inquiries, viewing requests, offers, complaints. Responding promptly and professionally to each one is time-consuming, repetitive, and easy to miss. Urgent emails like viewing requests and offers get buried alongside routine ones.

---

## The Solution

A LangGraph-powered autonomous agent that processes every incoming email in seconds — classifying it, drafting a context-aware response, and logging it to a shared Google Sheet so nothing slips through.

---

## Features

- **6-Category Classification** — Property Inquiry, Viewing Request, Offer/Negotiation, Complaint, General Information, Follow-up
- **AI-Drafted Responses** — Professional, warm replies in the same language as the client (English or Urdu)
- **Urgency Detection** — Viewing Requests and Offers flagged for immediate human attention
- **Google Sheets Logging** — Every processed email logged automatically with timestamp, category, and draft response
- **Clean Streamlit Dashboard** — Simple interface, no technical knowledge required

---

## Architecture

```
Client Email Input
        ↓
  LangGraph Agent
        ↓
  ┌─────────────┐
  │  Classify   │ → Category + Urgency Flag
  │  & Draft    │ → Professional Response
  └─────────────┘
        ↓
  ┌─────────────┐
  │  Log to     │ → Google Sheets row appended
  │  Sheets     │
  └─────────────┘
        ↓
  Streamlit Dashboard
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Agent Orchestration | LangGraph |
| LLM Framework | LangChain |
| Language Model | Qwen3 27B via Groq API |
| Structured Output | Pydantic with_structured_output() |
| Logging | Google Sheets API via gspread |
| Frontend | Streamlit |
| Language | Python 3.13 |

---

## Project Structure

```
real-estate-email-agent/
├── app.py                  # Streamlit UI and dashboard
├── agent.py                # LangGraph graph definition and nodes
├── tools.py                # Google Sheets logging tool
├── prompts.py              # System prompt and response guidelines
├── credentials.json        # Google Service Account (never committed)
├── .env                    # API keys (never committed)
├── .gitignore
└── requirements.txt
```

---

## Getting Started

**1. Clone the repository**
```bash
git clone https://github.com/Arsliator-r/real-estate-email-agent.git
cd real-estate-email-agent
```

**2. Create and activate a virtual environment**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Create a `.env` file:
```
GROQ_API_KEY=your_groq_api_key
GOOGLE_SHEET_NAME=Real Estate Email Log
```

Get a free Groq API key at [console.groq.com](https://console.groq.com)

**5. Set up Google Sheets integration**

- Create a Google Cloud project and enable Google Sheets API and Google Drive API
- Create a Service Account and download the credentials as `credentials.json`
- Create a Google Sheet named `Real Estate Email Log` with headers:
  `Timestamp | Sender | Subject | Category | Draft Response | Urgent`
- Share the Sheet with your service account email (Editor access)

**6. Run the app**
```bash
streamlit run app.py
```

---

## Usage

1. Paste the client's email — sender, subject, and body
2. Click **Process Email**
3. The agent returns a category, urgency flag, and draft response in seconds
4. The email is automatically logged to your Google Sheet
5. Review the draft, personalise if needed, and send

---

## Email Categories

| Category | Urgent | Description |
|---|---|---|
| Property Inquiry | No | Client asking about a specific listing |
| Viewing Request | **Yes** | Client wants to schedule a visit |
| Offer / Negotiation | **Yes** | Client making or countering an offer |
| Complaint | No | Client has an issue or grievance |
| General Information | No | Asking about area, pricing, availability |
| Follow-up | No | Chasing a previous conversation |

---

## Roadmap

- [ ] Gmail API integration — fetch and process emails automatically without manual paste
- [ ] WhatsApp notification via Twilio for urgent emails
- [ ] FastAPI backend — expose agent as a REST API for integration with CRM systems
- [ ] Multi-agency support — separate sheets and configurations per client
- [ ] Response history and thread tracking

---

## Context

This is the fourth project in a series building AI tools for real Pakistani market problems. Previous projects include Smart Car Advisor (ML pricing engine, 97.18% R²) and a Pakistani Car Deal Evaluator (LangChain + RAG). This project adds LangGraph multi-node orchestration and real third-party API integration to the stack.

---

## Author

**Muhammad Arsalan**
AI Engineer — Agentic Systems & LLM Applications
[LinkedIn](https://linkedin.com/in/arsliator-r) · [GitHub](https://github.com/Arsliator-r)

---

## License

MIT License — free to use, modify, and distribute.
