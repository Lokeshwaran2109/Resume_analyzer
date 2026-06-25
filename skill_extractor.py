from src.skills import skill_map


def extract_skills(text: str):
    """
    Extract skills using keyword + variation matching.
    """

    if not text:
        return []

    text = text.lower()
    found_skills = set()

    for main_skill, variations in skill_map.items():
        for var in variations:

            # safer matching (avoids partial word issues)
            if f" {var} " in f" {text} ":
                found_skills.add(main_skill)
                break

    return sorted(list(found_skills))
