
from modules.database import (
    create_database,
    save_interview,
    get_interview_history
)

# Create database
create_database()

# Insert sample interview
save_interview(
    candidate_name="Test Student",
    target_role="Python Developer",
    interview_type="Technical Interview",
    total_questions=5,
    average_score=8.0,
    final_report="Sample interview performance report."
)

# Retrieve interview records
records = get_interview_history()

print("INTERVIEW HISTORY")

for record in records:
    print(record)
