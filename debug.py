from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class EmailAnalysis(BaseModel):
    category: str = Field(description="One of: Property Inquiry, Viewing Request, Offer / Negotiation, Complaint, General Information, Follow-up")
    is_urgent: str = Field(description="Yes or No")
    draft_response: str = Field(description="Professional email response")

llm = ChatGroq(model="qwen/qwen3.8-27b", temperature=0.3, max_tokens=800)
structured_llm = llm.with_structured_output(EmailAnalysis)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an email assistant for a real estate agency."),
    ("human", "Process this email - From: ahmed@gmail.com, Subject: Property inquiry, Body: I want to buy a house in DHA, budget 2.5 crore.")
])

chain = prompt | structured_llm
result = chain.invoke({})
print("Category:", result.category)
print("Urgent:", result.is_urgent)
print("Response:", result.draft_response)