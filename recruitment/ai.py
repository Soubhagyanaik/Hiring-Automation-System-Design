def evaluate_candidate(resume_text, job_description, skills):

    resume_text = resume_text.lower()
    skills_list = skills.lower().split(",")

    match_count = 0

    for skill in skills_list:
        if skill.strip() in resume_text:
            match_count += 1

    if match_count >= 2:
        return "Strong Candidate"
    else:
        return "Weak Candidate"