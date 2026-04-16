from skills import skill_map


def extract_skills(text):
    text = text.lower()
    found_skills=[]
    for main_skill,variations in skill_map.items():
        for var in variations:
            if var in text:
                found_skills.append(main_skill)
                break

    return list(set(found_skills))
