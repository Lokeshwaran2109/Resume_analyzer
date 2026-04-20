from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="Ftegq6ndAFy2splCKHwczhMogDRJcYkRvi4Cnp8PNnloVXZle8gpJQQJ99CDACqBBLyXJ3w3AAABACOGd2qJ",
    api_version="2024-02-15-preview",
    azure_endpoint="https://resumegenai.openai.azure.com/"
)

def generate_ai_suggestions(resume_text):
    try:
        response = client.chat.completions.create(
            model="resume-ai",  # your deployment name
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional resume expert."
                },
                {
                    "role": "user",
                    "content": f"""
Analyze this resume and provide:

1. Improved resume wording
2. Missing skills (with explanation)
3. Career suggestions

Resume:
{resume_text}
"""
                }
            ],
            max_tokens=400
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"