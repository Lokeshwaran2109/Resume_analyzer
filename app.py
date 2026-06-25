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

st.title("🤖 AI Resume Analyzer & Career Intelligence System")


# -----------------------------
# INPUT SECTION (JD FIRST)
# -----------------------------
st.subheader("📌 Step 1: Job Description")
jd_text = st.text_area("Paste Job Description here")

st.subheader("📄 Step 2: Resume Upload")
uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])


# -----------------------------
# PDF READER
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

    jd_skills = extract_skills(jd_text.lower())
    resume_skills = extract_skills(resume_text)

    matched = set(resume_skills) & set(jd_skills)
    missing = set(jd_skills) - set(resume_skills)

    score = (len(matched) / len(jd_skills) * 100) if jd_skills else 0


    # =====================================================
    # 🚀 MODERN DASHBOARD UI (SAAS STYLE)
    # =====================================================
    st.subheader("📊 AI Resume Intelligence Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.markdown(f"""
    <div style="padding:20px;background:#111827;border-radius:12px;text-align:center">
        <h3 style="color:#60a5fa">ATS SCORE</h3>
        <h2 style="color:white">{round(score,2)}%</h2>
    </div>
    """, unsafe_allow_html=True)

    col2.markdown(f"""
    <div style="padding:20px;background:#111827;border-radius:12px;text-align:center">
        <h3 style="color:#34d399">MATCHED</h3>
        <h2 style="color:white">{len(matched)}</h2>
    </div>
    """, unsafe_allow_html=True)

    col3.markdown(f"""
    <div style="padding:20px;background:#111827;border-radius:12px;text-align:center">
        <h3 style="color:#f87171">MISSING</h3>
        <h2 style="color:white">{len(missing)}</h2>
    </div>
    """, unsafe_allow_html=True)

    st.progress(int(score))


    # =====================================================
    # 🧠 SKILL INTELLIGENCE (BADGES UI)
    # =====================================================
    st.subheader("🧠 Skill Intelligence View")

    st.markdown("### ✔ Matched Skills")

    if matched:
        st.markdown(
            " ".join([
                f"<span style='background:#14532d;padding:6px 10px;margin:4px;border-radius:8px;color:#4ade80'>✔ {s}</span>"
                for s in matched
            ]),
            unsafe_allow_html=True
        )
    else:
        st.write("No matched skills")


    st.markdown("### ❌ Missing Skills")

    if missing:
        st.markdown(
            " ".join([
                f"<span style='background:#450a0a;padding:6px 10px;margin:4px;border-radius:8px;color:#f87171'>✖ {s}</span>"
                for s in missing
            ]),
            unsafe_allow_html=True
        )
    else:
        st.write("No missing skills 🎯")


    # =====================================================
    # 🎯 ROLE PREDICTION
    # =====================================================
    st.subheader("🎯 Career Role Prediction")

    role = "Software Developer"

    if "machine learning" in resume_text or "ml" in resume_text:
        role = "Machine Learning Engineer"
    elif "sql" in resume_text or "power bi" in resume_text:
        role = "Data Analyst"
    elif "react" in resume_text or "javascript" in resume_text:
        role = "Frontend Developer"

    st.success(f"Predicted Role: {role}")


    # =====================================================
    # 🧠 CAREER INSIGHT
    # =====================================================
    st.subheader("🧠 Career Insight")

    if score >= 75:
        st.success("🔥 Strong profile - Interview ready")
        st.info("Focus: System design, advanced projects, deployment")
    elif score >= 40:
        st.warning("⚠ Moderate profile - Improve skills & projects")
        st.info("Focus: SQL, ML basics, GitHub projects")
    else:
        st.error("❌ Weak profile - Build fundamentals first")
        st.info("Focus: Python, SQL, mini projects")


    # =====================================================
    # 🤖 AI SUGGESTIONS BUTTON
    # =====================================================
    st.subheader("🤖 AI Career Suggestions")

    if st.button("✨ Generate AI Report"):

        with st.spinner("Analyzing resume intelligence..."):

            ai_output = generate_ai_suggestions(
                resume_text + " " + jd_text
            )

            st.success("Analysis Completed 🚀")
            st.write(ai_output)


# -----------------------------
# SIDEBAR DEBUG
# -----------------------------
with st.sidebar:
    st.title("⚙ Debug Panel")

    if jd_text:
        st.write("JD Loaded ✔")

    if uploaded_file:
        st.write("Resume Uploaded ✔")
