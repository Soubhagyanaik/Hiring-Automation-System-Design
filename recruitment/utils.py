def evaluate_candidate(resume_text, skills):
    resume_text = resume_text.lower()
    skills_list = skills.lower().split(",")

    match_count = 0

    for skill in skills_list:
        if skill.strip() in resume_text:
            match_count += 1

    score = match_count * 20

    if match_count >= 2:
        status = "Strong Candidate"
    else:
        status = "Weak Candidate"

    return score, status