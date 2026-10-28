import streamlit as st
import google.generativeai as genai
from typing import Optional

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(
    page_title="Business AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------- SIDEBAR & AUTH ----------------------
with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input("Enter your Google Gemini API Key", type="password", 
                           help="Get free key from: https://aistudio.google.com/apikey")
    
    st.divider()
    st.markdown("### 📋 Features")
    selected_feature = st.radio("Choose a tool:", [
        "💬 Business Chat Assistant",
        "📄 Document Summarizer",
        "✉️ Email Writer & Responder",
        "📢 Marketing Content Generator"
    ])
    
    st.divider()
    st.info("Made for small & medium businesses")

# ---------------------- AI CONFIGURATION ----------------------
def init_ai() -> Optional[genai.GenerativeModel]:
    if not api_key:
        return None
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        return model
    except Exception as e:
        st.error(f"⚠️ API configuration failed: {str(e)}")
        return None

model = init_ai()

# ---------------------- MAIN APPLICATION ----------------------
st.title("🤖 Business AI Application")
st.subheader("Your all-in-one smart business companion")

if not model:
    st.warning("👆 Please enter your Gemini API key in the sidebar to get started.")
    st.markdown("""
    **What this app can do:**
    - Answer business questions & give advice
    - Summarize long reports, articles, or documents
    - Write professional emails & draft replies
    - Generate marketing posts, captions & ad copy
    """)
    st.stop()

# --- Feature 1: Chat Assistant ---
if selected_feature == "💬 Business Chat Assistant":
    st.header("Business Chat Assistant")
    business_prompt = st.text_area(
        "What would you like to ask or discuss?",
        placeholder="e.g., How can I improve my customer retention? Give me 5 ideas to grow my local business...",
        height=150
    )
    
    if st.button("🚀 Get AI Advice", type="primary") and business_prompt:
        with st.spinner("Thinking..."):
            full_prompt = f"""You are an expert business consultant. Provide clear, practical, actionable advice.
            Question: {business_prompt}"""
            response = model.generate_content(full_prompt)
            st.markdown("### 💡 Response")
            st.write(response.text)

# --- Feature 2: Document Summarizer ---
elif selected_feature == "📄 Document Summarizer":
    st.header("Document Summarizer")
    doc_text = st.text_area("Paste your document text below:", height=250)
    summary_length = st.select_slider("Summary length:", 
                                     options=["Short (1-2 paragraphs)", 
                                              "Medium (balanced)", 
                                              "Detailed (key points)"])
    
    if st.button("📝 Summarize", type="primary") and doc_text:
        with st.spinner("Analyzing document..."):
            full_prompt = f"""Summarize this business document clearly and accurately.
            Preferred length: {summary_length}
            Document: {doc_text}"""
            response = model.generate_content(full_prompt)
            st.markdown("### 📋 Summary")
            st.write(response.text)

# --- Feature 3: Email Writer ---
elif selected_feature == "✉️ Email Writer & Responder":
    st.header("Professional Email Assistant")
    email_topic = st.text_input("What is the email about?")
    tone = st.selectbox("Email tone:", ["Professional", "Friendly", "Formal", "Persuasive"])
    key_points = st.text_area("Key details to include:", height=120)
    
    if st.button("✉️ Generate Email", type="primary") and email_topic:
        with st.spinner("Drafting email..."):
            full_prompt = f"""Write a {tone} business email about: {email_topic}.
            Include these details: {key_points}
            Structure: Subject line, greeting, body, closing.
            """
            response = model.generate_content(full_prompt)
            st.markdown("### 📧 Your Email")
            st.write(response.text)

# --- Feature 4: Marketing Generator ---
elif selected_feature == "📢 Marketing Content Generator":
    st.header("Marketing Content Creator")
    product_name = st.text_input("Product/Service name:")
    target_audience = st.text_input("Who is your audience?")
    platform = st.selectbox("Where will you post this?", 
                           ["Social Media (General)", "Instagram/Facebook", 
                            "LinkedIn", "Twitter/X", "Email Campaign"])
    
    if st.button("✨ Generate Content", type="primary") and product_name:
        with st.spinner("Creating marketing content..."):
            full_prompt = f"""Create engaging marketing copy for: {product_name}.
            Target audience: {target_audience}
            Platform: {platform}
            Make it persuasive, clear, and ready to publish.
            """
            response = model.generate_content(full_prompt)
            st.markdown("### 🎯 Your Content")
            st.write(response.text)

# ---------------------- FOOTER ----------------------
st.divider()
st.markdown("💼 **Business AI App** — Grow smarter, work faster")
