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
# MATCH LOGIC (FIXED - NO MISSING FILE)
# -----------------------------
def calculate_match(resume_skills, jd_skills):

    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    matched = resume_set.intersection(jd_set)
    missing = jd_set - resume_set

    score = (len(matched) / len(jd_set)) * 100 if jd_set else 0

    return {
        "score": round(score, 2),
        "matched": list(matched),
        "missing": list(missing)
    }


# -----------------------------
# INPUT
# -----------------------------
uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])
jd_text = st.text_area("📌 Paste Job Description here")


# -----------------------------
# MAIN LOGIC
# -----------------------------
if uploaded_file and jd_text:

    resume_text = extract_text_from_pdf(uploaded_file)

    # JD analysis first
    st.subheader("📌 Job Description Analysis")
    st.write(jd_text[:800])

    jd_skills = extract_skills(jd_text.lower())
    resume_skills = extract_skills(resume_text)

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

    # -----------------------------
    # SKILLS
    # -----------------------------
    col1, col2 = st.columns(2)

    with col1:
        st.success("✔ Matched Skills")
        st.write(result["matched"] if result["matched"] else "None")

    with col2:
        st.error("❌ Missing Skills")
        st.write(result["missing"] if result["missing"] else "None")

    # -----------------------------
    # AI (FREE VERSION)
    # -----------------------------
    st.subheader("🤖 AI Career Suggestions")

    ai_output = generate_ai_suggestions(resume_text + " " + jd_text)
    st.write(ai_output)

    # -----------------------------
    # CAREER INSIGHT
    # -----------------------------
    st.subheader("🧠 Career Insight")

    if result["score"] >= 75:
        st.success("🔥 Strong profile - Ready for interviews")
    elif result["score"] >= 40:
        st.warning("⚠ Moderate profile - Improve skills")
    else:
        st.error("❌ Weak profile - Needs major improvement")
