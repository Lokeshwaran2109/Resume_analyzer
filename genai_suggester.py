# from openai import AzureOpenAI

# client = AzureOpenAI(
#     api_key="Ftegq6ndAFy2splCKHwczhMogDRJcYkRvi4Cnp8PNnloVXZle8gpJQQJ99CDACqBBLyXJ3w3AAABACOGd2qJ",
#     api_version="2024-02-15-preview",
#     azure_endpoint="https://resumegenai.openai.azure.com/"
# )

# def generate_ai_suggestions(resume_text):
#     try:
#         response = client.chat.completions.create(
#             model="resume-ai",  # your deployment name
#             messages=[
#                 {
#                     "role": "system",
#                     "content": "You are a professional resume expert."
#                 },
#                 {
#                     "role": "user",
#                     "content": f"""
# Analyze this resume and provide:

# 1. Improved resume wording
# 2. Missing skills (with explanation)
# 3. Career suggestions

# Resume:
# {resume_text}
# """
#                 }
#             ],
#             max_tokens=400
#         )

#         return response.choices[0].message.content


#     except Exception as e:
#         return f"Error: {str(e)}"







def generate_ai_suggestions(resume_text: str):

    text = resume_text.lower()

    suggestions = []

    # -------------------------
    # BASIC INTELLIGENCE LOGIC
    # -------------------------

    # Python check
    if "python" not in text:
        suggestions.append("🔹 Learn Python fundamentals to improve your AI/Data Science profile.")

    # SQL check
    if "sql" not in text:
        suggestions.append("🔹 Add SQL skills (very important for Data Analyst roles).")

    # Machine Learning check
    if "machine learning" not in text:
        suggestions.append("🔹 Build at least 1 Machine Learning project (very high impact).")

    # Projects check
    if "project" not in text:
        suggestions.append("🔹 Add 2–3 strong real-world projects on GitHub.")

    # GitHub check
    if "github" not in text:
        suggestions.append("🔹 Showcase your projects on GitHub for better visibility.")

    # Internship readiness
    if len(text) < 500:
        suggestions.append("🔹 Resume looks short. Add more experience, projects, and achievements.")

    # Strong profile detection
    if "python" in text and "sql" in text and "machine learning" in text:
        suggestions.append("🔥 Strong AI/DS profile detected. You are internship-ready.")

    # -------------------------
    # DEFAULT OUTPUT
    # -------------------------
    if not suggestions:
        return "✅ Good resume structure. Keep improving with more projects."

    return "\n".join(suggestions)
