import streamlit as st
import pdfplumber
from genai_suggester import generate_ai_suggestions

# -----------------------------
# SKILLS DATABASE
# -----------------------------
SKILLS = [
    # Data Science
    "python", "machine learning", "deep learning", "nlp", "data science",
    "pandas", "numpy", "matplotlib", "statistics", "sql", "tableau", "power bi",

    # Software Dev
    "java", "c++", "spring boot", "rest api", "dsa", "git",

    # Web
    "html", "css", "javascript", "react",

    # Cloud
    "aws", "azure", "docker", "linux"
]

# -----------------------------
# FUNCTIONS
# -----------------------------
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.lower()


def extract_skills(text):
    found = []
    for skill in SKILLS:
        if skill in text:
            found.append(skill)
    return list(set(found))


# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("🤖 AI Resume Analyzer & Career Guide")

# Upload Resume
uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

# Job Description
jd_text = st.text_area("📌 Paste Job Description here")

# -----------------------------
# MAIN LOGIC
# -----------------------------
if uploaded_file is not None:

    # Extract resume text
    resume_text = extract_text_from_pdf(uploaded_file)

    # Extract skills
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text.lower())

    # -----------------------------
    # MATCHING LOGIC (FIXED)
    # -----------------------------
    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    matched = resume_set.intersection(jd_set)
    missing = jd_set - resume_set

    if len(jd_set) == 0:
        match_score = 0
    else:
        match_score = (len(matched) / len(jd_set)) * 100

    # -----------------------------
    # UI OUTPUT
    # -----------------------------
    st.subheader("📊 Job Match Score")
    st.progress(int(match_score))
    st.write(f"{round(match_score,2)}% match with job")

    col1, col2 = st.columns(2)

    with col1:
        st.success("✔ Skills Found in Resume")
        st.write(resume_skills)

    with col2:
        st.error("❌ Missing Skills (from JD)")
        if missing:
            st.write(list(missing))
        else:
            st.write("No missing skills 🎯")

    # -----------------------------
    # AI SUGGESTIONS
    # -----------------------------
    st.subheader("🤖 GenAI Suggestions")

    if st.button("Get AI Suggestions"):
        with st.spinner("Analyzing with AI..."):
            ai_output = generate_ai_suggestions(resume_text)

            st.write(ai_output)

    # -----------------------------
    # CAREER INSIGHTS
    # -----------------------------
    st.subheader("🧠 Career Insights")

    if match_score > 75:
        st.success("You are a strong match for this role.")
    elif match_score > 40:
        st.warning("You partially match. Improve missing skills.")
    else:
        st.error("Low match. Focus on required skills.")

    # -----------------------------
    # DEBUG PANEL (VERY USEFUL)
    # -----------------------------
    st.sidebar.subheader("⚙ Debug Info")
    st.sidebar.write("Resume Skills:", resume_skills)
    st.sidebar.write("JD Skills:", jd_skills)
    st.sidebar.write("Matched:", list(matched))
    st.sidebar.write("Missing:", list(missing))
