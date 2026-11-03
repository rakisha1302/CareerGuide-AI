
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ==========================================
# 1. CAREER DATABASE
# ==========================================

career_data = {
    "AI/ML Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "Statistics",
        "Scikit-learn",
        "TensorFlow",
        "PyTorch"
    ],

    "Data Scientist": [
        "Python",
        "SQL",
        "Statistics",
        "Machine Learning",
        "Pandas",
        "NumPy",
        "Data Visualization"
    ],

    "Data Analyst": [
        "Python",
        "SQL",
        "Excel",
        "Statistics",
        "Power BI",
        "Data Visualization"
    ],

    "Frontend Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Git"
    ],

    "Software Developer": [
        "Python",
        "Java",
        "C",
        "Data Structures",
        "Algorithms",
        "SQL",
        "Git"
    ]
}


# ==========================================
# 2. NORMALIZE STUDENT SKILLS
# ==========================================

def normalize_skills(skills):

    if not skills:
        return []

    if isinstance(skills, str):
        skills = [skills]

    normalized = []

    for skill in skills:

        if isinstance(skill, str) and skill.strip():

            cleaned_skill = skill.strip().lower()

            if cleaned_skill not in normalized:
                normalized.append(cleaned_skill)

    return normalized


# ==========================================
# 3. RECOMMEND CAREERS
# ==========================================

def recommend_careers(student_skills):

    normalized_student_skills = normalize_skills(
        student_skills
    )

    if not normalized_student_skills:
        return []

    career_names = list(career_data.keys())

    # Convert career skills into text documents
    career_documents = [
        " ".join(career_data[career])
        for career in career_names
    ]

    # Convert student skills into one document
    student_document = " ".join(
        normalized_student_skills
    )

    # TF-IDF vectorization
    vectorizer = TfidfVectorizer()

    all_documents = career_documents + [
        student_document
    ]

    tfidf_matrix = vectorizer.fit_transform(
        all_documents
    )

    # Calculate cosine similarity
    similarity_scores = cosine_similarity(
        tfidf_matrix[-1],
        tfidf_matrix[:-1]
    )[0]

    recommendations = []

    # Analyze each career
    for index, career in enumerate(career_names):

        required_skills = career_data[career]

        normalized_required = [
            skill.lower()
            for skill in required_skills
        ]

        matched_skills = [
            skill
            for skill in required_skills
            if skill.lower() in normalized_student_skills
        ]

        missing_skills = [
            skill
            for skill in required_skills
            if skill.lower() not in normalized_student_skills
        ]

        total_required = len(required_skills)

        matched_count = len(matched_skills)

        missing_count = len(missing_skills)

        # Direct skill coverage percentage
        skill_match = (
            matched_count / total_required
        ) * 100

        # TF-IDF similarity percentage
        similarity_score = (
            float(similarity_scores[index]) * 100
        )

        recommendations.append({

            "career": career,

            "score": round(
                similarity_score, 2
            ),

            "skill_match": round(
                skill_match, 2
            ),

            "skills": required_skills,

            "matched_skills": matched_skills,

            "missing_skills": missing_skills,

            "total_required_skills": total_required,

            "matched_count": matched_count,

            "missing_count": missing_count

        })

    # Rank careers by direct skill coverage
    recommendations.sort(
        key=lambda item: (
            item["skill_match"],
            item["score"]
        ),
        reverse=True
    )

    return recommendations


# ==========================================
# 4. DETAILED SKILL GAP ANALYSIS
# ==========================================

def get_skill_gap(career, student_skills):

    if career not in career_data:
        return None

    normalized_student_skills = normalize_skills(
        student_skills
    )

    required_skills = career_data[career]

    matched_skills = [
        skill
        for skill in required_skills
        if skill.lower() in normalized_student_skills
    ]

    missing_skills = [
        skill
        for skill in required_skills
        if skill.lower() not in normalized_student_skills
    ]

    total_required = len(required_skills)

    matched_count = len(matched_skills)

    missing_count = len(missing_skills)

    skill_match = (
        matched_count / total_required
    ) * 100

    return {

        "career": career,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "total_required_skills": total_required,

        "matched_count": matched_count,

        "missing_count": missing_count,

        "skill_match": round(
            skill_match, 2
        )

    }


# ==========================================
# 5. GET ALL AVAILABLE CAREERS
# ==========================================

def get_available_careers():

    return list(career_data.keys())


# ==========================================
# 6. GET REQUIRED SKILLS FOR A CAREER
# ==========================================

def get_required_skills(career):

    if career not in career_data:
        return []

    return career_data[career]
