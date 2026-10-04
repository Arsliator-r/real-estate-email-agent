import streamlit as st
from agent import process_email

st.set_page_config(
    page_title="Real Estate Email Agent",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Real Estate Email Agent")
st.markdown("AI-powered email processing for Pakistani real estate agencies.")

# ── Input Section ────────────────────────────────────────────
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    sender = st.text_input(
        "Sender Email",
        value=st.session_state.get('test_sender', ''),
        placeholder="client@example.com"
    )

    subject = st.text_input(
        "Subject",
        value=st.session_state.get('test_subject', ''),
        placeholder="Inquiry about DHA Phase 6 property"
    )

with col2:
    body = st.text_area(
        "Email Body",
        value=st.session_state.get('test_body', ''),
        placeholder="Paste the client email here...",
        height=150
    )

# ── Process Button ───────────────────────────────────────────
if st.button("Process Email", type="primary", use_container_width=True):
    if not sender or not subject or not body:
        st.warning("Please fill in all fields before processing.")
    else:
        with st.spinner("Agent is processing the email..."):
            result = process_email(sender, subject, body)

        st.markdown("---")

        if result.get("error"):
            st.error(f"Something went wrong: {result['error']}")
        else:
            # ── Results ──────────────────────────────────────
            col_a, col_b = st.columns(2)

            with col_a:
                # Category badge
                category = result["category"]
                is_urgent = result["is_urgent"]

                urgent_color = "🔴" if is_urgent == "Yes" else "🟢"
                st.markdown(f"### {urgent_color} {category}")

                if is_urgent == "Yes":
                    st.error("⚡ URGENT — Requires immediate attention")
                else:
                    st.success("✅ Standard priority")

                st.markdown(f"**Logged to Sheets:** {result.get('log_result', 'N/A')}")

            with col_b:
                st.markdown("### 📝 Suggested Response")
                st.info(result["draft_response"])

                # Copy button workaround
                st.code(result["draft_response"], language=None)

# ── Recent Emails Section ────────────────────────────────────
st.markdown("---")
st.markdown("### 📊 Recent Processing Log")
st.markdown("Check your [Google Sheet](https://sheets.google.com) for the full log.")

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### About")
    st.markdown("""
    This agent processes incoming real estate client emails using LangGraph.

    **What it does:**
    - Classifies email into 6 categories
    - Drafts a professional response
    - Flags urgent emails
    - Logs everything to Google Sheets

    **Built with:**
    - LangGraph
    - LangChain
    - Groq (Qwen)
    - Google Sheets API
    - Streamlit
    """)

    st.markdown("### Test Emails")
    st.markdown("Try these sample inputs:")

    if st.button("Load Property Inquiry"):
        st.session_state['test_sender'] = "ahmed.khan@gmail.com"
        st.session_state['test_subject'] = "3 Bed Apartment DHA Phase 6"
        st.session_state['test_body'] = "Assalam o Alaikum, I saw your listing for a 3 bedroom apartment in DHA Phase 6. Can you please share more details about the price and available date? My budget is around 2.5 crore."

    if st.button("Load Viewing Request"):
        st.session_state['test_sender'] = "sara.malik@hotmail.com"
        st.session_state['test_subject'] = "Viewing Request - Gulberg Property"
        st.session_state['test_body'] = "Hi, I am interested in the Gulberg 2 property listed at 1.8 crore. Can we schedule a viewing this weekend, preferably Saturday afternoon? Please let me know what time works."