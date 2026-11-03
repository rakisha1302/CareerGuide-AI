
import streamlit as st
from modules.database import (
    save_career_profile,
    get_career_profile
)


def run_career_twin():

    st.title("🧬 My Career Digital Twin")

    st.write(
        "Your personal AI-powered career identity. "
        "Build your profile and track your career journey."
    )

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.error("Please log in first.")
        return

    profile = get_career_profile(user_id)

    # Load existing profile
    if profile:
        education = profile[2] or ""
        career_goal = profile[3] or ""
        interests = profile[4] or ""
        technical_skills = profile[5] or ""
        projects = profile[6] or ""
        github_link = profile[7] or ""
    else:
        education = ""
        career_goal = ""
        interests = ""
        technical_skills = ""
        projects = ""
        github_link = ""

    st.subheader("👤 Student Identity")

    st.text_input(
        "Student Name",
        value=st.session_state.user_name,
        disabled=True
    )

    st.text_input(
        "Email",
        value=st.session_state.user_email,
        disabled=True
    )

    st.divider()

    st.subheader("🎯 Career Goal")

    education = st.text_input(
        "Education",
        value=education,
        placeholder="B.Tech Artificial Intelligence and Data Science"
    )

    career_goal = st.selectbox(
        "Target Career",
        [
            "Select a career",
            "Data Scientist",
            "AI/ML Engineer",
            "Data Analyst",
            "Software Developer",
            "Python Developer",
            "Business Analyst"
        ],
        index=(
            [
                "Select a career",
                "Data Scientist",
                "AI/ML Engineer",
                "Data Analyst",
                "Software Developer",
                "Python Developer",
                "Business Analyst"
            ].index(career_goal)
            if career_goal in [
                "Select a career",
                "Data Scientist",
                "AI/ML Engineer",
                "Data Analyst",
                "Software Developer",
                "Python Developer",
                "Business Analyst"
            ]
            else 0
        )
    )

    interests = st.text_area(
        "Career Interests",
        value=interests,
        placeholder="AI, Machine Learning, Data Analytics..."
    )

    st.divider()

    st.subheader("💻 Technical Skills")

    technical_skills = st.text_area(
        "Skills you currently know",
        value=technical_skills,
        placeholder="Python, SQL, Pandas, NumPy, Machine Learning..."
    )

    st.divider()

    st.subheader("🚀 Project Portfolio")

    projects = st.text_area(
        "Your Projects",
        value=projects,
        placeholder="Project name and a short description..."
    )

    github_link = st.text_input(
        "GitHub Profile or Repository Link",
        value=github_link,
        placeholder="https://github.com/yourusername"
    )

    if st.button("💾 Save My Career Twin", use_container_width=True):

        if not education.strip() or career_goal == "Select a career":
            st.warning("Please enter your education and select a career goal.")

        else:
            save_career_profile(
                user_id,
                education,
                career_goal,
                interests,
                technical_skills,
                projects,
                github_link
            )

            st.success("Your Career Digital Twin has been updated!")
            st.rerun()

    st.divider()

    st.subheader("📊 Your Career Identity")

    st.write("**Target Role:**", career_goal)
    st.write("**Technical Skills:**", technical_skills or "Not added yet")
    st.write("**Projects:**", projects or "Not added yet")

    if github_link:
        st.markdown(f"[View GitHub Portfolio]({github_link})")
