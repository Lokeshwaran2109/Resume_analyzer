import streamlit as st
import pdfplumber

from src.analyzer.skill_extractor import extract_skills
from src.analyzer.matcher import calculate_match
from src.ai.ai_service import AIService


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
# INPUT SECTION
# -----------------------------
uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])
jd_text = st.text_area("📌 Paste Job Description here")


# -----------------------------
# PDF EXTRACTION
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

    # Step 1: Extract resume text
    resume_text = extract_text_from_pdf(uploaded_file)

    # Step 2: JD FIRST (IMPORTANT FIX YOU WANTED)
    st.subheader("📌 Job Description Analysis")

    st.info("We analyzed your job description below:")
    st.write(jd_text[:800])

    jd_skills = extract_skills(jd_text.lower())

    st.success("Key skills found in JD:")
    st.write(jd_skills)

    st.divider()

    # Step 3: Resume skills
    resume_skills = extract_skills(resume_text)

    # Step 4: Matching
    result = calculate_match(resume_skills, jd_skills)

    # -----------------------------
    # DASHBOARD
    # -----------------------------
    st.subheader("📊 Resume Match Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Match Score", f"{result['score']}%")
    col2.metric("Matched Skills", len(result["matched"]))
    col3.metric("Missing Skills", len(result["missing"]))

    st.progress(int(result["score"]))

    st.divider()

    # -----------------------------
    # SKILLS SECTION
    # -----------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.success("✔ Matched Skills")
        st.write(result["matched"] if result["matched"] else "None")

    with col2:
        st.error("❌ Missing Skills")
        st.write(result["missing"] if result["missing"] else "None")

    st.divider()

    # -----------------------------
    # AI SECTION (FREE VERSION OR API)
    # -----------------------------
    st.subheader("🤖 AI Career Suggestions")

    with st.spinner("Generating insights..."):
        ai_output = AIService.analyze_resume(resume_text, jd_text)

    st.write(ai_output)

    st.divider()

    # -----------------------------
    # CAREER INSIGHT BOX
    # -----------------------------
    st.subheader("🧠 Career Insight")

    if result["score"] >= 75:
        st.success("🔥 Strong profile - Ready for interviews")
    elif result["score"] >= 40:
        st.warning("⚠ Moderate profile - Improve skills")
    else:
        st.error("❌ Weak profile - Needs major improvement")


# -----------------------------
# SIDEBAR DEBUG
# -----------------------------
with st.sidebar:
    st.title("⚙ Debug Panel")

    if uploaded_file:
        st.write("Resume uploaded ✔")

    if jd_text:
        st.write("JD provided ✔")
