import streamlit as st

from pdf_parser import extract_text
from skill_extractor import extract_skills
from genai_suggester import generate_ai_suggestions


# ---------------- UI ----------------
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.title("🤖 AI Resume Analyzer & Career Guide")


uploaded_file = st.file_uploader("Upload Resume PDF", type=["pdf"])
jd_text = st.text_area("Paste Job Description")


# ---------------- LOGIC ----------------
if uploaded_file and jd_text:

    resume_text = extract_text(uploaded_file)

    st.subheader("📌 Job Description")
    st.write(jd_text[:800])

    jd_skills = extract_skills(jd_text)
    resume_skills = extract_skills(resume_text)

    matched = set(resume_skills) & set(jd_skills)
    missing = set(jd_skills) - set(resume_skills)

    score = (len(matched) / len(jd_skills) * 100) if jd_skills else 0


    # ---------------- DASHBOARD ----------------
    st.subheader("📊 Match Score")

    col1, col2, col3 = st.columns(3)

    col1.metric("Score", f"{round(score,2)}%")
    col2.metric("Matched", len(matched))
    col3.metric("Missing", len(missing))

    st.progress(int(score))


    # ---------------- SKILLS ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.success("Matched Skills")
        st.write(list(matched) if matched else "None")

    with col2:
        st.error("Missing Skills")
        st.write(list(missing) if missing else "None")


    # ---------------- AI ----------------
    st.subheader("🤖 AI Suggestions")

    ai_output = generate_ai_suggestions(resume_text + " " + jd_text)
    st.write(ai_output)


    # ---------------- CAREER ----------------
    st.subheader("🧠 Career Insight")

    if score > 75:
        st.success("Strong profile 🚀")
    elif score > 40:
        st.warning("Moderate profile ⚠")
    else:
        st.error("Weak profile ❌")
