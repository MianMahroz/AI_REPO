import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext
from llama_index.llms import LlamaCPP
from llama_index.embeddings import HuggingFaceEmbedding
import pandas as pd
from email_processor import OutlookEmailProcessor
from database import IssueDatabase
import time

# --- Config ---
st.set_page_config(
    page_title="AI Issue Tracker",
    page_icon="🔧",
    layout="wide"
)

# --- Initialize DB & AI Models ---
@st.cache_resource
def init_components():
    # Load Llama model
    llm = LlamaCPP(
        model_path="./models/llama-2-7b-chat.Q4_K_M.gguf",
        temperature=0.2,
        max_new_tokens=512,
        n_ctx=2048,
    )
    
    # Load embedding model
    embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # Initialize database
    db = IssueDatabase()
    db.init_db()
    
    return llm, embed_model, db

llm, embed_model, db = init_components()

# --- Streamlit UI ---
st.title("🔧 AI-Powered Issue Tracker")
st.markdown("Analyze Outlook emails and find past resolutions using AI.")

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Actions")
    if st.button("🔄 Fetch New Emails"):
        with st.spinner("Fetching & processing emails..."):
            processor = OutlookEmailProcessor()
            emails = processor.fetch_emails(limit=5)
            if emails:
                db.insert_emails(emails)
                st.success(f"Processed {len(emails)} new emails!")
            else:
                st.warning("No new issue emails found.")

# --- Main Dashboard ---
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🔍 Search Issues", "📥 Add Manually"])

with tab1:
    st.subheader("Recent Issues")
    issues = db.get_recent_issues(limit=10)
    st.dataframe(issues)

with tab2:
    st.subheader("Search Similar Issues")
    query = st.text_input("Describe the issue:")
    
    if st.button("🔎 Search") and query:
        with st.spinner("Finding similar issues..."):
            similar_issues = db.semantic_search(query, k=3)
            if similar_issues:
                st.write("### � Similar Past Issues")
                for issue in similar_issues:
                    st.write(f"**Subject:** {issue['subject']}")
                    st.write(f"**Error:** {issue['error_message']}")
                    st.write(f"**Resolution:** {issue['resolution']}")
                    st.divider()
            else:
                st.warning("No similar issues found.")

with tab3:
    st.subheader("Add Issue Manually")
    with st.form("new_issue"):
        subject = st.text_input("Subject")
        error = st.text_area("Error Message")
        resolution = st.text_area("Resolution")
        
        if st.form_submit_button("💾 Save Issue"):
            db.insert_manual_issue(subject, error, resolution)
            st.success("Issue saved!")