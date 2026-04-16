import streamlit as st
from pdf_parser import extract_text
from cleaner import clean_text
from skill_extractor import extract_skills
from genai_suggester import genrate_suggestions

# Page config
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("🤖 AI Resume Analyzer & Career Guide")
st.markdown("Upload your resume and compare it with a Job Description 🚀")

# Upload resume
uploaded_file = st.file_uploader("📄 Upload Resume (PDF)")

# Job Description input
jd_text = st.text_area("📌 Paste Job Description here")

if uploaded_file:

    # Save file
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    # Process resume
    raw_text = extract_text("temp.pdf")
    clean_resume = clean_text(raw_text)
    found_skills = extract_skills(clean_resume)

    # Process JD
    jd_clean = clean_text(jd_text)
    jd_skills = extract_skills(jd_clean)

    # Matching logic
    matched = [s for s in jd_skills if s in found_skills]
    missing = [s for s in jd_skills if s not in found_skills]

    # Score calculation
    score = (len(matched) / len(jd_skills)) * 100 if jd_skills else 0

    # UI Display
    st.subheader("📊 Job Match Score")
    st.progress(int(score))
    st.write(f"{score:.2f}% match with job")

    # Layout
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Skills Found in Resume")
        st.write(", ".join(found_skills) if found_skills else "No skills detected")

    with col2:
        st.subheader("❌ Missing Skills (from JD)")
        st.write(", ".join(missing) if missing else "No missing skills 🎯")

    # AI Suggestions
    suggestions = genrate_suggestions(found_skills, missing, score)

    st.subheader("🤖 AI Career Insights")

    for s in suggestions:
        st.write("•", s)

else:
    st.info("Please upload a resume to begin.")