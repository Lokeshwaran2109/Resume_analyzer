import streamlit as st
import pdfplumber

from skill_extractor import extract_skills
from genai_suggester import generate_ai_suggestions


# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    layout="wide",
    page_icon="🤖"
)

st.title("🤖 AI Resume Analyzer & Career Guide")


# -----------------------------
# INPUT SECTION (JD FIRST)
# -----------------------------
st.subheader("📌 Step 1: Paste Job Description")
jd_text = st.text_area("Enter Job Description here")

st.subheader("📄 Step 2: Upload Resume")
uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])


# -----------------------------
# PDF TEXT EXTRACTION
# -----------------------------
def extract_text_from_pdf(file):
    text = ""

    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

    except Exception as e:
        st.error(f"PDF Error: {e}")
        return ""

    return text.lower()


# -----------------------------
# MAIN LOGIC
# -----------------------------
if uploaded_file and jd_text:

    resume_text = extract_text_from_pdf(uploaded_file)

    # -----------------------------
    # JD ANALYSIS (FIRST)
    # -----------------------------
    st.subheader("📌 Job Description Analysis")
    st.info("We analyzed your Job Description")

    st.write(jd_text[:800])

    jd_skills = extract_skills(jd_text.lower())
    resume_skills = extract_skills(resume_text)

    # -----------------------------
    # MATCHING
    # -----------------------------
    matched = set(resume_skills) & set(jd_skills)
    missing = set(jd_skills) - set(resume_skills)

    score = (len(matched) / len(jd_skills) * 100) if jd_skills else 0

    # -----------------------------
    # DASHBOARD
    # -----------------------------
    st.subheader("📊 Resume Match Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Match Score", f"{round(score,2)}%")
    col2.metric("Matched Skills", len(matched))
    col3.metric("Missing Skills", len(missing))

    st.progress(int(score))

    # -----------------------------
    # SKILLS DISPLAY
    # -----------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.success("✔ Matched Skills")
        if matched:
            for skill in matched:
                st.write("✔", skill)
        else:
            st.write("None")

    with col2:
        st.error("❌ Missing Skills")
        if missing:
            for skill in missing:
                st.write("✖", skill)
        else:
            st.write("None")

    # -----------------------------
    # AI SUGGESTION BUTTON (IMPORTANT)
    # -----------------------------
    st.subheader("🤖 AI Career Suggestions")

    if st.button("✨ Get AI Suggestions"):

        with st.spinner("Analyzing resume with AI..."):

            ai_output = generate_ai_suggestions(
                resume_text + " " + jd_text
            )

            st.success("AI Analysis Completed 🚀")
            st.write(ai_output)

    # -----------------------------
    # CAREER INSIGHT
    # -----------------------------
    st.subheader("🧠 Career Insight")

    if score >= 75:
        st.success("🔥 Strong profile - Ready for interviews")
    elif score >= 40:
        st.warning("⚠ Moderate profile - Improve skills")
    else:
        st.error("❌ Weak profile - Needs major improvement")


# -----------------------------
# SIDEBAR DEBUG
# -----------------------------
with st.sidebar:
    st.title("⚙ Debug Panel")

    if jd_text:
        st.write("JD Loaded ✔")

    if uploaded_file:
        st.write("Resume Uploaded ✔")
