def genrate_suggestions(found_skills,missing_skills,score):

    suggestion = []

    if missing_skills:
        for skill in missing_skills:
            suggestion.append(f"Consider adding {skill} to your resume will improve your score.")


    if score<50:
        suggestion.append("your resume score is week. focus on building storang projects")   

    elif score<80:
        suggestion.append("Your resume is average. Add more relevant skills and projects.")
    else:
        suggestion.append("Your resume is strong. Try applying for internships and jobs.")     



    if "machine learning" in found_skills:
        suggestion.append("You are suitable for Machine Learning Engineer roles.")
    if "data analysis" in found_skills or "sql" in found_skills:
        suggestion.append("You are suitable for Data Analyst roles.")
    if "deep learning" in found_skills:
        suggestion.append("You can explore AI Engineer roles.")


    roadmap = []

    if "sql" not in found_skills:
        roadmap.append("Learn SQL")

    if "machine learning" not in found_skills:
        roadmap.append("Learn Machine Learning")

    if "power bi" not in found_skills:
        roadmap.append("Learn Power BI")

    if roadmap:
        suggestion.append("Recommended roadmap: " + " → ".join(roadmap))

    return suggestion
        