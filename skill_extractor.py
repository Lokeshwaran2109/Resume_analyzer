from skills import skill_map
import re

def extract_skills(text: str):

    if not text:
        return []

    text = text.lower()

    # clean text
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    found_skills = set()

    for main_skill, variations in skill_map.items():
        for var in variations:
            pattern = r'\b' + re.escape(var) + r'\b'
            if re.search(pattern, text):
                found_skills.add(main_skill)
                break

    return sorted(list(found_skills))
