
# ==========================================
# IMPORTS
# ==========================================
from modules.database import (
    get_interview_history,
    save_student_skills,
    get_student_skills
)
import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
from modules.auth import show_auth_page
from modules.career_twin import run_career_twin
from modules.mock_interview import run_mock_interview
from modules.interview_history import run_interview_history
from modules.recommendation import recommend_careers, get_skill_gap

# ==========================================
# APPLICATION CONFIGURATION
# ==========================================

load_dotenv()

st.set_page_config(
    page_title="CareerGuide AI",
    page_icon="🎓",
    layout="wide"
)


# ==========================================
# LOAD CUSTOM CSS
# ==========================================

def load_css():
    with open("assets/style.css", "r", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )


load_css()
# Check student login
# Initialize login session
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if not st.session_state.get("logged_in", False):
    show_auth_page()
    st.stop()

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("🎓 CareerGuide AI")

st.sidebar.caption(
    "Your AI-Powered Career Companion"
)

st.sidebar.divider()
# Logged-in student details
st.sidebar.success(
    f"Welcome, {st.session_state.user_name}!"
)

st.sidebar.caption(st.session_state.user_email)

# Logout button
if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.user_name = None
    st.session_state.user_email = None
    st.rerun()

st.sidebar.divider()

st.sidebar.markdown("### 📌 MAIN MENU")

menu = st.sidebar.selectbox(
    "Choose a Module",
    [
        "Home",
        "Student Profile",
        "Career Recommendations",
        "Skill Gap Analysis",
        "Learning Roadmap",
        "Career Chatbot",
        "AI Mock Interview",
        "Interview History",
        "Career Digital Twin"
    ],
    label_visibility="collapsed"
)

st.sidebar.divider()

st.sidebar.info(
    "🤖 AI Career Assistant\n\n"
    "Plan • Learn • Practice • Succeed"
)


# ==========================================
# HOME DASHBOARD
# ==========================================

if menu == "Home":

    st.title("🚀 Welcome to CareerGuide AI")

    st.markdown(
        "### Your Personal AI-Powered Career Development Platform"
    )

    st.write(
        "Discover your career path, identify skill gaps, "
        "practice interviews and prepare confidently for placements."
    )

    st.divider()

    # Retrieve interview history
    records = get_interview_history()

    total_interviews = len(records)

    average_score = (
        sum(record[5] for record in records) / total_interviews
        if total_interviews > 0 else 0
    )

    best_score = (
        max(record[5] for record in records)
        if total_interviews > 0 else 0
    )

    # Dashboard metrics
    st.subheader("📊 Your Career Preparation Overview")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🎯 Career Paths",
        "5"
    )

    col2.metric(
        "🎤 Interviews Completed",
        total_interviews
    )

    col3.metric(
        "⭐ Average Interview Score",
        f"{average_score:.1f}/10"
    )

    st.divider()

    # Career preparation journey
    st.subheader("✨ Your Career Preparation Journey")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("#### 🎯 Discover Your Career")

        st.write(
            "Explore suitable career paths based on your technical skills."
        )

        st.markdown("#### 📊 Improve Your Skills")

        st.write(
            "Identify missing skills and understand what you need to learn."
        )

        st.markdown("#### 📚 Follow Your Roadmap")

        st.write(
            "Build your knowledge through a structured learning journey."
        )

    with col2:

        st.markdown("#### 🤖 Ask Your AI Career Assistant")

        st.write(
            "Get guidance about careers, technologies and placement preparation."
        )

        st.markdown("#### 🎤 Practice Interviews")

        st.write(
            "Answer AI-generated interview questions and receive feedback."
        )

        st.markdown("#### 📈 Track Your Progress")

        st.write(
            "Review previous interview reports and monitor your performance."
        )

    st.divider()

    # Interview performance
    st.subheader("🏆 Interview Performance")

    if total_interviews > 0:

        st.success(
            f"You have completed {total_interviews} mock interview(s). "
            f"Your best score is {best_score:.1f}/10."
        )

    else:

        st.info(
            "You haven't completed a mock interview yet. "
            "Start your first AI Mock Interview to track your progress!"
        )

    st.divider()

    st.success(
        "💡 Your Career Starts Here! "
        "Discover your strengths, develop new skills "
        "and prepare for your dream job."
    )


# ==========================================
# STUDENT PROFILE
# ==========================================

elif menu == "Student Profile":

    st.title("👤 Student Profile")

    st.subheader("Enter Your Student Profile")

    name = st.text_input("Enter your name")

    education = st.selectbox(
        "Select your education",
        [
            "2nd Year",
            "3rd Year",
            "Final Year",
            "Graduate"
        ]
    )

    skills = st.multiselect(
        "Select your technical skills",
        [
            "Python",
            "Java",
            "C",
            "SQL",
            "Machine Learning",
            "Deep Learning",
            "Data Analysis",
            "HTML",
            "CSS",
            "JavaScript"
        ]
    )

    interests = st.multiselect(
        "Select your interests",
        [
            "Artificial Intelligence",
            "Data Science",
            "Web Development",
            "Software Development",
            "Data Analytics"
        ]
    )

    if st.button("💾 Save Profile"):

        if name and skills and interests:

            st.success("Student profile saved successfully!")

            st.write("**Name:**", name)
            st.write("**Education:**", education)
            st.write("**Skills:**", ", ".join(skills))
            st.write("**Interests:**", ", ".join(interests))

        else:

            st.warning(
                "Please enter your name, skills, and interests."
            )


# ==========================================
# CAREER RECOMMENDATIONS
# ==========================================


# ==========================================
# CAREER RECOMMENDATIONS
# ==========================================
elif menu == "Career Recommendations":

    st.title("🎯 AI Career Recommendations")

    st.markdown(
        "Discover suitable career paths based on your technical skills."
    )

    st.divider()

    all_skills = [
        "Python",
        "Java",
        "C",
        "SQL",
        "Machine Learning",
        "Deep Learning",
        "Statistics",
        "Scikit-learn",
        "TensorFlow",
        "PyTorch",
        "Pandas",
        "NumPy",
        "Data Visualization",
        "Excel",
        "Power BI",
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Git",
        "Data Structures",
        "Algorithms"
    ]

    st.subheader("💡 Your Technical Skills")

    saved_profile = get_student_skills(st.session_state.user_id)

    default_skills = (
        saved_profile["skills"]
        if saved_profile
        else []
    )

    selected_skills = st.multiselect(
        "Select the skills you already know",
        all_skills,
        default=default_skills,
        placeholder="Choose your technical skills..."
    )

    if st.button(
        "🚀 Find My Career",
        use_container_width=True
    ):

        if not selected_skills:

            st.warning(
                "Please select at least one skill."
            )

        else:
            save_student_skills(
                st.session_state.user_id,
                selected_skills
            )

            # Generate career recommendations
            results = recommend_careers(selected_skills)

            st.session_state.career_results = results
            st.session_state.career_student_skills = selected_skills

            st.success("✅ Your skills have been saved successfully!")

            
    # Display recommendations
    if st.session_state.get("career_results"):

        results = st.session_state.career_results

        st.divider()

        st.subheader("🏆 Your Career Matches")

        st.caption(
            "Rankings are based on direct skill coverage. "
            "TF-IDF similarity is displayed separately."
        )

        for index, item in enumerate(results, start=1):

            with st.container(border=True):

                col1, col2 = st.columns([3, 1])

                with col1:

                    st.subheader(
                        f"{index}. 💼 {item['career']}"
                    )

                with col2:

                    st.metric(
                        "Skill Coverage",
                        f"{item['skill_match']:.1f}%"
                    )

                st.progress(
                    item["skill_match"] / 100
                )

                st.caption(
                    f"TF-IDF Similarity: {item['score']:.2f}%"
                )

                matched_col, missing_col = st.columns(2)

                with matched_col:

                    st.markdown("#### ✅ Matched Skills")

                    if item["matched_skills"]:

                        for skill in item["matched_skills"]:

                            st.markdown(
                                f"<span style='color:#16A34A;'>✔ {skill}</span>",
                                unsafe_allow_html=True
                            )

                    else:

                        st.write("No matching skills yet.")

                with missing_col:

                    st.markdown("#### 📚 Skills to Learn")

                    if item["missing_skills"]:

                        for skill in item["missing_skills"]:

                            st.markdown(
                                f"<span style='color:#F59E0B;'>● {skill}</span>",
                                unsafe_allow_html=True
                            )

                    else:

                        st.success("All listed skills matched!")

                st.caption(
                    f"Matched: {item['matched_count']} | "
                    f"Missing: {item['missing_count']} | "
                    f"Required: {item['total_required_skills']}"
                )

        st.divider()

        st.subheader("🔍 Detailed Career Skill Gap")

        career_options = [
            item["career"] for item in results
        ]

        selected_career = st.selectbox(
            "Choose a career for detailed analysis",
            career_options
        )

        gap = get_skill_gap(
            selected_career,
            st.session_state.career_student_skills
        )

        if gap:

            st.metric(
                "Your Skill Readiness",
                f"{gap['skill_match']:.2f}%"
            )

            st.progress(
                gap["skill_match"] / 100
            )

            col1, col2 = st.columns(2)

            with col1:

                st.success("✅ Skills You Know")

                for skill in gap["matched_skills"]:
                    st.write(f"✔ {skill}")

            with col2:

                st.warning("📚 Skills You Need to Learn")

                for skill in gap["missing_skills"]:
                    st.write(f"➜ {skill}")

            st.info(
                "💡 Focus on learning the missing skills "
                "to improve your readiness for this career."
            )

# ==========================================
# SKILL GAP ANALYSIS
# ==========================================

elif menu == "Skill Gap Analysis":

    st.title("📊 AI Skill Gap Analysis")

    st.write(
        "Compare your current skills with industry-required skills "
        "and discover what you need to learn."
    )

    st.divider()

    career_skills = {

        "AI/ML Engineer": [
            "Python",
            "SQL",
            "Machine Learning",
            "Deep Learning",
            "Statistics",
            "Scikit-learn"
        ],

        "Data Scientist": [
            "Python",
            "SQL",
            "Statistics",
            "Machine Learning",
            "Pandas",
            "Data Visualization"
        ],

        "Data Analyst": [
            "Python",
            "SQL",
            "Excel",
            "Statistics",
            "Data Visualization"
        ],

        "Frontend Developer": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Git"
        ]
    }

    career = st.selectbox(
        "🎯 Select your target career",
        list(career_skills.keys())
    )

    student_skills = st.multiselect(
        "✅ Select the skills you already know",
        [
            "Python",
            "SQL",
            "Machine Learning",
            "Deep Learning",
            "Statistics",
            "Scikit-learn",
            "Pandas",
            "Data Visualization",
            "Excel",
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Git"
        ]
    )

    if st.button("🔍 Analyze My Skill Gap"):

        required = career_skills[career]

        available = [
            skill for skill in required
            if skill in student_skills
        ]

        missing = [
            skill for skill in required
            if skill not in student_skills
        ]

        percentage = len(available) / len(required) * 100

        st.divider()

        st.subheader("📈 Your Skill Readiness")

        st.metric(
            "Skill Match Percentage",
            f"{percentage:.1f}%"
        )

        st.progress(percentage / 100)

        col1, col2 = st.columns(2)

        with col1:

            st.success(
                f"✅ Skills You Know: {len(available)}"
            )

            for skill in available:
                st.write(f"✔️ {skill}")

        with col2:

            st.warning(
                f"📚 Skills to Learn: {len(missing)}"
            )

            for skill in missing:
                st.write(f"📌 {skill}")

        st.divider()

        st.subheader("🚀 Personalized Learning Suggestions")

        learning_resources = {

            "Python": "Practice Python programming and problem-solving.",
            "SQL": "Learn joins, subqueries and database queries.",
            "Machine Learning": "Study regression, classification and clustering.",
            "Deep Learning": "Learn neural networks, CNNs and RNNs.",
            "Statistics": "Practice probability, hypothesis testing and statistics.",
            "Scikit-learn": "Build ML models using Scikit-learn.",
            "Pandas": "Practice data cleaning and data manipulation.",
            "Data Visualization": "Learn Matplotlib, Seaborn and Power BI.",
            "Excel": "Practice formulas, charts and pivot tables.",
            "HTML": "Learn semantic HTML and web page structure.",
            "CSS": "Practice responsive design, Flexbox and Grid.",
            "JavaScript": "Learn functions, DOM and events.",
            "React": "Learn components, props and hooks.",
            "Git": "Practice version control using Git and GitHub."
        }

        if missing:

            for skill in missing:

                st.info(
                    f"**{skill}:** {learning_resources[skill]}"
                )

        else:

            st.balloons()

            st.success(
                "🎉 Excellent! You have all the listed skills "
                "for this career."
            )


# ==========================================
# LEARNING ROADMAP
# ==========================================

elif menu == "Learning Roadmap":

    st.title("📚 Personalized Learning Roadmap")

    st.write(
        "Follow your career learning journey and track "
        "your progress step by step."
    )

    st.divider()

    roadmaps = {

        "AI/ML Engineer": {

            "Phase 1: Python Fundamentals": [
                "Python Programming",
                "Functions and OOP",
                "NumPy",
                "Pandas"
            ],

            "Phase 2: Mathematics and Statistics": [
                "Linear Algebra",
                "Probability",
                "Descriptive Statistics",
                "Calculus Basics"
            ],

            "Phase 3: Machine Learning": [
                "Supervised Learning",
                "Unsupervised Learning",
                "Regression",
                "Classification",
                "Scikit-learn"
            ],

            "Phase 4: Deep Learning": [
                "Neural Networks",
                "CNN",
                "RNN and LSTM",
                "PyTorch or TensorFlow"
            ],

            "Phase 5: Projects and Deployment": [
                "Build an ML Project",
                "Build a Deep Learning Project",
                "Flask or Streamlit",
                "Git and GitHub",
                "Deploy Your Project"
            ]
        },

        "Data Scientist": {

            "Phase 1: Python Fundamentals": [
                "Python Basics",
                "Functions and OOP",
                "NumPy",
                "Pandas"
            ],

            "Phase 2: Mathematics and Statistics": [
                "Probability",
                "Statistics",
                "Hypothesis Testing",
                "Linear Algebra"
            ],

            "Phase 3: Data Analysis": [
                "Data Cleaning",
                "Exploratory Data Analysis",
                "Matplotlib",
                "Seaborn"
            ],

            "Phase 4: Machine Learning": [
                "Regression",
                "Classification",
                "Clustering",
                "Model Evaluation",
                "Scikit-learn"
            ],

            "Phase 5: Projects": [
                "Data Analysis Project",
                "Prediction Model",
                "Portfolio",
                "Git and GitHub"
            ]
        },

        "Data Analyst": {

            "Phase 1: Excel": [
                "Excel Basics",
                "Formulas",
                "Pivot Tables",
                "Data Cleaning"
            ],

            "Phase 2: SQL": [
                "SQL Queries",
                "Joins",
                "Subqueries",
                "Aggregate Functions"
            ],

            "Phase 3: Python": [
                "Python Basics",
                "NumPy",
                "Pandas",
                "Data Cleaning"
            ],

            "Phase 4: Visualization": [
                "Matplotlib",
                "Seaborn",
                "Power BI",
                "Dashboard Creation"
            ],

            "Phase 5: Projects": [
                "Sales Analysis",
                "Customer Analysis",
                "Business Dashboard",
                "Git and GitHub"
            ]
        },

        "Frontend Developer": {

            "Phase 1: HTML": [
                "HTML Basics",
                "Forms",
                "Tables",
                "Semantic HTML"
            ],

            "Phase 2: CSS": [
                "CSS Basics",
                "Flexbox",
                "Grid",
                "Responsive Design"
            ],

            "Phase 3: JavaScript": [
                "Variables",
                "Functions",
                "DOM Manipulation",
                "Events"
            ],

            "Phase 4: React": [
                "Components",
                "Props and State",
                "Hooks",
                "API Integration"
            ],

            "Phase 5: Projects": [
                "Portfolio Website",
                "React Application",
                "Git and GitHub",
                "Deploy Website"
            ]
        }
    }

    career = st.selectbox(
        "🎯 Choose your target career",
        list(roadmaps.keys())
    )

    phases = roadmaps[career]

    # Initialize progress storage
    if "roadmap_completed" not in st.session_state:

        st.session_state.roadmap_completed = {}

    completed = st.session_state.roadmap_completed

    all_topics = [

        f"{career}_{phase}_{topic}"

        for phase, topics in phases.items()

        for topic in topics
    ]

    completed_count = sum(
        completed.get(topic, False)
        for topic in all_topics
    )

    total_topics = len(all_topics)

    percentage = completed_count / total_topics * 100

    st.subheader("📈 Your Overall Progress")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Topics", total_topics)

    col2.metric("Completed", completed_count)

    col3.metric("Progress", f"{percentage:.1f}%")

    st.progress(percentage / 100)

    st.divider()

    st.subheader(f"🚀 Learning Plan: {career}")

    for phase_index, (phase, topics) in enumerate(phases.items()):

        phase_keys = [
            f"{career}_{phase}_{topic}"
            for topic in topics
        ]

        phase_completed = sum(
            completed.get(key, False)
            for key in phase_keys
        )

        phase_percentage = phase_completed / len(topics)

        with st.expander(
            f"{phase} — {phase_completed}/{len(topics)} completed",
            expanded=(phase_index == 0)
        ):

            st.progress(phase_percentage)

            for topic, key in zip(topics, phase_keys):

                completed[key] = st.checkbox(
                    topic,
                    value=completed.get(key, False),
                    key=f"checkbox_{key}"
                )

            if phase_completed == len(topics):

                st.success("🎉 Phase completed!")

    st.divider()

    if completed_count == total_topics:

        st.balloons()

        st.success(
            "🏆 Congratulations! You completed your roadmap!"
        )

    else:

        st.info(
            f"Keep going! {total_topics - completed_count} topics remaining."
        )

    if st.button("🔄 Reset Learning Progress"):

        for key in all_topics:
            completed.pop(key, None)

        st.session_state.roadmap_completed = completed

        st.rerun()


# ==========================================
# CAREER CHATBOT
# ==========================================

elif menu == "Career Chatbot":

    st.title("🤖 CareerGuide AI Chatbot")

    st.write(
        "Hello! I am your AI Career Assistant. "
        "Ask me anything about careers, Python, SQL, "
        "Machine Learning, interviews, resumes and placements."
    )

    st.divider()

    if "chat_history" not in st.session_state:

        st.session_state.chat_history = []

    # Display previous messages
    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):

            st.write(message["content"])

    # User question
    question = st.chat_input(
        "Ask your career question..."
    )

    if question:

        st.session_state.chat_history.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):

            st.write(question)

        with st.chat_message("assistant"):

            with st.spinner("Generating your answer..."):

                try:

                    api_key = os.getenv("GROQ_API_KEY")

                    if not api_key:

                        st.error(
                            "API key not found. Check your .env file."
                        )

                        st.stop()

                    client = Groq(api_key=api_key)

                    conversation = [

                        {
                            "role": "system",

                            "content": (
                                "You are CareerGuide AI, an intelligent "
                                "career guidance assistant. Answer questions "
                                "about Python, SQL, DSA, aptitude, AI, Data "
                                "Science, projects, resumes, interviews and "
                                "placements. Generate original answers based "
                                "on the user's exact request. Follow requested "
                                "numbers and formats. If asked for exactly "
                                "10 questions, provide exactly 10 numbered "
                                "questions. Explain concepts simply for beginners."
                            )
                        }
                    ]

                    conversation.extend(
                        st.session_state.chat_history[-12:]
                    )

                    response = client.chat.completions.create(
                        model="openai/gpt-oss-120b",
                        messages=conversation,
                        temperature=0.7,
                        max_completion_tokens=2000
                    )

                    answer = response.choices[0].message.content

                    st.write(answer)

                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": answer
                    })

                except Exception as e:

                    st.error(f"AI Error: {e}")

    if st.button("🗑️ Clear Chat"):

        st.session_state.chat_history = []

        st.rerun()


# ==========================================
# AI MOCK INTERVIEW
# ==========================================

elif menu == "AI Mock Interview":

    run_mock_interview()


# ==========================================
# INTERVIEW HISTORY
# ==========================================

elif menu == "Interview History":

    run_interview_history()
elif menu == "Career Digital Twin":
    run_career_twin()