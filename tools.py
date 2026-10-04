from langchain_core.tools import tool
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import os

def get_sheet():
    creds = Credentials.from_service_account_file(
        'credentials.json',
        scopes=[
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
    )
    client = gspread.authorize(creds)
    return client.open(os.getenv("GOOGLE_SHEET_NAME", "Real Estate Email Log")).sheet1

@tool
def log_to_sheets(
    sender: str,
    subject: str,
    category: str,
    draft_response: str,
    is_urgent: str
) -> str:
    """Log a processed email and its AI-drafted response to Google Sheets."""
    try:
        sheet = get_sheet()
        sheet.append_row([
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            sender,
            subject,
            category,
            draft_response,
            is_urgent
        ])
        return "Successfully logged to Google Sheets"
    except Exception as e:
        return f"Logging failed: {str(e)}"