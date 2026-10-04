from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field
from typing import TypedDict, List
from tools import log_to_sheets
from prompts import SYSTEM_PROMPT
from dotenv import load_dotenv
import os

load_dotenv()

# ── State ─────────────────────────────────────────────────────
class EmailState(TypedDict):
    sender: str
    subject: str
    body: str
    category: str
    is_urgent: str
    draft_response: str
    log_result: str
    error: str

# ── Pydantic schema for structured output ────────────────────
class EmailAnalysis(BaseModel):
    category: str = Field(description="One of: Property Inquiry, Viewing Request, Offer / Negotiation, Complaint, General Information, Follow-up")
    is_urgent: str = Field(description="Yes or No")
    draft_response: str = Field(description="Professional email response in the same language as the input")

# ── LLM ──────────────────────────────────────────────────────
llm = ChatGroq(model="qwen/qwen3.8-27b", temperature=0.3, max_tokens=800)
structured_llm = llm.with_structured_output(EmailAnalysis)

# ── Nodes ────────────────────────────────────────────────────
def classify_and_draft(state: EmailState) -> EmailState:
    """Classify the email and draft a response."""
    try:
        prompt = ChatPromptTemplate.from_messages([
            ("system", SYSTEM_PROMPT),
            ("human", """Process this email:

From: {sender}
Subject: {subject}
Body: {body}

Classify it, determine urgency, and draft a professional response.""")
        ])

        chain = prompt | structured_llm
        result = chain.invoke({
            "sender": state["sender"],
            "subject": state["subject"],
            "body": state["body"]
        })

        return {
            **state,
            "category": result.category,
            "is_urgent": result.is_urgent,
            "draft_response": result.draft_response,
            "error": ""
        }

    except Exception as e:
        return {
            **state,
            "error": f"Classification failed: {str(e)}"
        }

def log_email(state: EmailState) -> EmailState:
    """Log the processed email to Google Sheets."""
    if state.get("error"):
        return state

    try:
        result = log_to_sheets.invoke({
            "sender": state["sender"],
            "subject": state["subject"],
            "category": state["category"],
            "draft_response": state["draft_response"],
            "is_urgent": state["is_urgent"]
        })
        return {**state, "log_result": result}

    except Exception as e:
        return {**state, "log_result": f"Logging failed: {str(e)}"}

def should_continue(state: EmailState) -> str:
    """Route based on whether classification succeeded."""
    if state.get("error"):
        return "end"
    return "log"

# ── Build the Graph ──────────────────────────────────────────
def build_agent():
    graph = StateGraph(EmailState)

    graph.add_node("classify", classify_and_draft)
    graph.add_node("log", log_email)

    graph.set_entry_point("classify")

    graph.add_conditional_edges(
        "classify",
        should_continue,
        {
            "log": "log",
            "end": END
        }
    )

    graph.add_edge("log", END)

    return graph.compile()

agent = build_agent()

def process_email(sender: str, subject: str, body: str) -> dict:
    """Main function called from app.py"""
    initial_state = EmailState(
        sender=sender,
        subject=subject,
        body=body,
        category="",
        is_urgent="",
        draft_response="",
        log_result="",
        error=""
    )

    result = agent.invoke(initial_state)
    return result