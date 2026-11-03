from modules.recommendation import recommend_careers, get_skill_gap

student_skills = ["Python", "SQL", "Pandas"]

results = recommend_careers(student_skills)

print("\n========== CAREERGUIDE AI ==========")
print("STUDENT SKILLS:", student_skills)

for index, item in enumerate(results, start=1):
    print(f"\n{index}. {item['career']}")
    print(f"TF-IDF Similarity: {item['score']}%")
    print(f"Skill Coverage: {item['skill_match']}%")
    print("Matched Skills:", item["matched_skills"])
    print("Missing Skills:", item["missing_skills"])

print("\n========== SKILL GAP ANALYSIS ==========")

gap = get_skill_gap("Data Scientist", student_skills)

print("Career:", gap["career"])
print("Coverage:", gap["skill_match"], "%")
print("Skills to Learn:", gap["missing_skills"])

print("\n========== TEST COMPLETED ==========")