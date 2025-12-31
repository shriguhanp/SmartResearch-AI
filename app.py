import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai

# ---------- LOAD ENV ----------
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# ---------- DYNAMIC GEMINI MODEL ----------
def get_working_model():
    for model in genai.list_models():
        if "generateContent" in model.supported_generation_methods:
            return genai.GenerativeModel(model.name)
    raise Exception("No supported Gemini models found for this API key.")

model = get_working_model()

# ---------- RESEARCH FUNCTION ----------
def run_research(query: str):
    prompt = f"""
You are an AI research assistant.

Research Query:
{query}

Tasks:
1. Explain the topic clearly
2. Provide key insights
3. Mention real-world use cases
4. Give a short conclusion

Return the response in bullet points.
"""
    response = model.generate_content(prompt)
    return response.text

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
.main {
    padding: 2rem;
}
.hero-title {
    font-size: 2.6rem;
    font-weight: 700;
    margin-bottom: 0.2rem;
}
.hero-subtitle {
    font-size: 1.1rem;
    color: #6b7280;
    margin-bottom: 2rem;
}
.section-title {
    font-size: 1.4rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}
.output-box {
    background-color: #0f172a;
    padding: 1.5rem;
    border-radius: 12px;
    color: #e5e7eb;
    line-height: 1.6;
    font-size: 1rem;
}
.block {
    background: linear-gradient(145deg, #020617, #020617);
    border: 1px solid #1e293b;
    padding: 1.2rem;
    border-radius: 14px;
    margin-bottom: 1rem;
}
.footer {
    text-align: center;
    margin-top: 3rem;
    color: #9ca3af;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# ---------- HERO ----------
st.markdown('<div class="hero-title">🧠 AI Research Automation</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Transform research questions into structured, actionable insights using Google Gemini</div>',
    unsafe_allow_html=True
)

# ---------- INPUT ----------
st.markdown('<div class="section-title">🔎 Research Query</div>', unsafe_allow_html=True)
query = st.text_area(
    "What would you like to research?",
    placeholder="Example: Applications of AI in healthcare diagnostics",
    height=120
)

col1, col2 = st.columns([1, 4])
with col1:
    generate = st.button("🚀 Generate")

# ---------- OUTPUT RENDERER ----------
def render_research_output(text):
    sections = text.split("\n\n")
    for sec in sections:
        sec_clean = sec.replace("**", "")
        if "Explanation" in sec:
            st.markdown('<div class="block">', unsafe_allow_html=True)
            st.markdown("### 🧠 Explanation")
            st.markdown(sec_clean)
            st.markdown('</div>', unsafe_allow_html=True)
        elif "How it Works" in sec:
            st.markdown('<div class="block">', unsafe_allow_html=True)
            st.markdown("### ⚙️ How It Works")
            st.markdown(sec_clean)
            st.markdown('</div>', unsafe_allow_html=True)
        elif "Key Insights" in sec:
            st.markdown('<div class="block">', unsafe_allow_html=True)
            st.markdown("### ⭐ Key Insights")
            lines = sec_clean.split("\n")[1:]
            for l in lines:
                if l.strip():
                    st.markdown(f"- ✅ {l.strip()}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown(sec_clean)

# ---------- PROCESS ----------
if generate:
    if not query.strip():
        st.warning("Please enter a research topic to continue.")
    else:
        with st.spinner("Analyzing sources and generating insights..."):
            result = run_research(query)

        st.markdown('<div class="section-title">📄 Research Output</div>', unsafe_allow_html=True)
        render_research_output(result)
        st.success("Research generated successfully!")

# ---------- FOOTER ----------
st.markdown("""
<div class="footer">
Built with ❤️ using Google Gemini • Designed for Hackathons & Research
</div>
""", unsafe_allow_html=True)
