from pdf_parser import extract_text
from cleaner import clean_text
from skill_extractor import extract_skills
from sklearn.feature_extraction.text import  TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from genai_suggester import genrate_suggestions
def main():
    file = "resume.pdf"

    raw_text = extract_text(file)

    if not raw_text:
        print("extraction fails")
        return
    
    clean = clean_text(raw_text)

    found_skills=extract_skills(clean)

    print("skill found:")
    print(found_skills)

    required_skills={
        "python","sql","machine learning","data science","statistics"
    }


    missing = []

    for skills in required_skills:
        if skills not in found_skills:
            missing.append(skills)


    print("\n missing skills")
    print(missing)

    matched=0
    for skill in required_skills:
        if skill in found_skills:
            matched+=1

    score = (matched/len(required_skills))*100
    print("\n resume score",round(score,2))

    job_decription="""Looking for a Data Scientist with experience in Python, SQL, Machine Learning, Deep Learning, and Data Analysis."""
    job_description = clean_text(job_decription)
    texts=[clean,job_description]

    vectorizer =  TfidfVectorizer()
    vectors = vectorizer.fit_transform(texts)
    similarity=cosine_similarity(vectors[0],vectors[1])
    match_score= similarity[0][0]*100
 
    print("\n📌 Resume Summary:")
    print(f"Score: {round(score,2)} | Job Match: {round(match_score,2)}%")
    
    suggestion  = genrate_suggestions(found_skills, missing,score)
    print("\n AI Career Analysis\n")

    for i, s in enumerate(suggestion, 1):
        print(f"{i}. {s}")
if __name__ == "__main__":
    main()