
import sqlite3
import json
from datetime import datetime

DATABASE_NAME = "career_guide.db"


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ==========================================
# CREATE DATABASE AND TABLES
# ==========================================

def create_database():

    conn = get_connection()
    cursor = conn.cursor()

    # Student accounts
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Interview history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_name TEXT,
            target_role TEXT,
            interview_type TEXT,
            total_questions INTEGER,
            average_score REAL,
            interview_date TEXT,
            final_report TEXT,
            user_id INTEGER REFERENCES users(id)
        )
    """)

    # Check existing interview table
    cursor.execute("PRAGMA table_info(interview_history)")
    columns = [column[1] for column in cursor.fetchall()]

    if "user_id" not in columns:
        cursor.execute("""
            ALTER TABLE interview_history
            ADD COLUMN user_id INTEGER REFERENCES users(id)
        """)

    # Career Digital Twin profile
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS career_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            education TEXT,
            career_goal TEXT,
            interests TEXT,
            technical_skills TEXT,
            projects TEXT,
            github_link TEXT,
            updated_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # NEW: Student skills and career preferences
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            skills TEXT NOT NULL,
            preferred_career TEXT,
            updated_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


# ==========================================
# SAVE INTERVIEW RESULT
# ==========================================

def save_interview(
    candidate_name,
    target_role,
    interview_type,
    total_questions,
    average_score,
    final_report,
    user_id=None
):

    if user_id is None:
        raise ValueError("A logged-in user ID is required.")

    create_database()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO interview_history (
            candidate_name,
            target_role,
            interview_type,
            total_questions,
            average_score,
            interview_date,
            final_report,
            user_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        candidate_name,
        target_role,
        interview_type,
        total_questions,
        average_score,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        final_report,
        user_id
    ))

    conn.commit()
    conn.close()


# ==========================================
# GET PERSONAL INTERVIEW HISTORY
# ==========================================

def get_interview_history(user_id=None):

    if user_id is None:
        return []

    create_database()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM interview_history
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    records = cursor.fetchall()
    conn.close()

    return records


# ==========================================
# SAVE CAREER DIGITAL TWIN PROFILE
# ==========================================

def save_career_profile(
    user_id,
    education,
    career_goal,
    interests,
    technical_skills,
    projects,
    github_link
):

    create_database()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO career_profiles (
            user_id,
            education,
            career_goal,
            interests,
            technical_skills,
            projects,
            github_link,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)

        ON CONFLICT(user_id) DO UPDATE SET
            education = excluded.education,
            career_goal = excluded.career_goal,
            interests = excluded.interests,
            technical_skills = excluded.technical_skills,
            projects = excluded.projects,
            github_link = excluded.github_link,
            updated_at = excluded.updated_at
    """, (
        user_id,
        education,
        career_goal,
        interests,
        technical_skills,
        projects,
        github_link,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


# ==========================================
# GET PERSONAL CAREER PROFILE
# ==========================================

def get_career_profile(user_id):

    create_database()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM career_profiles
        WHERE user_id = ?
    """, (user_id,))

    profile = cursor.fetchone()
    conn.close()

    return profile


# ==========================================
# NEW: SAVE STUDENT SKILLS
# ==========================================

def save_student_skills(
    user_id,
    skills,
    preferred_career=None
):

    if user_id is None:
        raise ValueError("A logged-in user ID is required.")

    create_database()

    # Convert Python skill list into JSON text
    skills_json = json.dumps(skills)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO student_skills (
            user_id,
            skills,
            preferred_career,
            updated_at
        )
        VALUES (?, ?, ?, ?)

        ON CONFLICT(user_id) DO UPDATE SET
            skills = excluded.skills,
            preferred_career = excluded.preferred_career,
            updated_at = excluded.updated_at
    """, (
        user_id,
        skills_json,
        preferred_career,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


# ==========================================
# NEW: GET STUDENT SKILLS
# ==========================================

def get_student_skills(user_id):

    if user_id is None:
        return None

    create_database()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT skills, preferred_career, updated_at
        FROM student_skills
        WHERE user_id = ?
    """, (user_id,))

    record = cursor.fetchone()
    conn.close()

    if record is None:
        return None

    return {
        "skills": json.loads(record[0]),
        "preferred_career": record[1],
        "updated_at": record[2]
    }
