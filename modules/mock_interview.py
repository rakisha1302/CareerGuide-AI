
import os
import re
import streamlit as st
from groq import Groq

from modules.database import (
    create_database,
    save_interview
)


# =========================================
# GROQ CLIENT
# =========================================

def get_groq_client():

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError(
            "Groq API key not found. Please check your .env file."
        )

    return Groq(api_key=api_key)


# =========================================
# AI RESPONSE GENERATOR
# =========================================

def generate_ai_response(client, messages):

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=messages,
        temperature=0.8,
        max_completion_tokens=1800
    )

    return response.choices[0].message.content


# =========================================
# EXTRACT SCORES FROM AI FEEDBACK
# =========================================

def extract_score(feedback):

    patterns = [
        r"score\s*(?:out of\s*10)?\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*/\s*10",
        r"(\d+(?:\.\d+)?)\s*/\s*10"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            feedback,
            re.IGNORECASE
        )

        if match:

            score = float(match.group(1))

            if 0 <= score <= 10:
                return score

    return None


# =========================================
# INITIALIZE SESSION STATE
# =========================================

def initialize_mock_session():

    defaults = {

        "mock_started": False,
        "mock_completed": False,

        "mock_history": [],

        "mock_question": None,
        "mock_feedback": None,

        "mock_final_report": None,

        "mock_question_number": 0,
        "mock_answer_submitted": False,

        "mock_candidate_name": "",
        "mock_role": "",
        "mock_skills": "",
        "mock_experience": "",
        "mock_type": "",

        "mock_total": 10,

        "mock_saved": False,
        "mock_save_error": None,

        "mock_owner_id": None

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value


# =========================================
# RESET INTERVIEW
# =========================================

def reset_mock_interview():

    st.session_state.mock_started = False
    st.session_state.mock_completed = False

    st.session_state.mock_history = []

    st.session_state.mock_question = None
    st.session_state.mock_feedback = None

    st.session_state.mock_final_report = None

    st.session_state.mock_question_number = 0
    st.session_state.mock_answer_submitted = False

    st.session_state.mock_candidate_name = ""
    st.session_state.mock_role = ""
    st.session_state.mock_skills = ""
    st.session_state.mock_experience = ""
    st.session_state.mock_type = ""

    st.session_state.mock_total = 10

    st.session_state.mock_saved = False
    st.session_state.mock_save_error = None


# =========================================
# RUN MOCK INTERVIEW
# =========================================

def run_mock_interview():

    # Initialize session
    initialize_mock_session()

    # Get logged-in student's ID
    user_id = st.session_state.get("user_id")

    if not user_id:

        st.error("Please log in before starting an interview.")
        st.stop()

    # Prevent one student's interview from appearing
    # when another student logs in using the same session.
    if st.session_state.mock_owner_id != user_id:

        reset_mock_interview()

        st.session_state.mock_owner_id = user_id

    # Initialize database
    try:

        create_database()

    except Exception as e:

        st.error(f"Database initialization failed: {e}")
        st.stop()

    # Page heading
    st.title("🎯 CareerGuide AI - Smart Mock Interview")

    st.write(
        "Experience an AI-powered interview that adapts "
        "to your skills, answers and performance."
    )

    st.divider()

    # =====================================
    # 1. CANDIDATE PROFILE
    # =====================================

    if (
        not st.session_state.mock_started
        and not st.session_state.mock_completed
    ):

        st.subheader("👨‍🎓 Your Interview Profile")

        candidate_name = st.text_input(
            "Candidate Name",
            placeholder="Enter your name",
            key="candidate_name_input"
        )

        role = st.text_input(
            "Target Job Role",
            placeholder="Example: Python Developer",
            key="role_input"
        )

        skills = st.text_area(
            "Your Technical Skills",
            placeholder="Example: Python, SQL, Machine Learning, Pandas",
            key="skills_input"
        )

        experience = st.selectbox(
            "Experience Level",
            ["Fresher", "Intermediate", "Advanced"],
            key="experience_input"
        )

        interview_type = st.selectbox(
            "Interview Type",
            [
                "Technical Interview",
                "HR Interview",
                "Coding Interview",
                "Project-Based Interview",
                "Mixed Interview"
            ],
            key="interview_type_input"
        )

        question_count = st.number_input(
            "Number of Questions",
            min_value=1,
            max_value=30,
            value=10,
            step=1,
            key="question_count_input"
        )

        # ---------------------------------
        # START INTERVIEW
        # ---------------------------------

        if st.button(
            "🚀 Start AI Interview",
            type="primary"
        ):

            if not candidate_name.strip():

                st.warning("Please enter your name.")

            elif not role.strip():

                st.warning("Please enter your target job role.")

            elif not skills.strip():

                st.warning("Please enter your technical skills.")

            else:

                st.session_state.mock_candidate_name = (
                    candidate_name.strip()
                )

                st.session_state.mock_role = role.strip()

                st.session_state.mock_skills = skills.strip()

                st.session_state.mock_experience = experience

                st.session_state.mock_type = interview_type

                st.session_state.mock_total = int(question_count)

                # Start interview
                st.session_state.mock_started = True
                st.session_state.mock_completed = False

                # Clear previous interview data
                st.session_state.mock_history = []

                st.session_state.mock_question = None
                st.session_state.mock_feedback = None

                st.session_state.mock_final_report = None

                st.session_state.mock_question_number = 0

                st.session_state.mock_answer_submitted = False

                st.session_state.mock_saved = False
                st.session_state.mock_save_error = None

                st.rerun()

    # =====================================
    # 2. INTERVIEW ENGINE
    # =====================================

    if st.session_state.mock_started:

        try:

            client = get_groq_client()

        except Exception as e:

            st.error(f"Groq configuration error: {e}")
            st.stop()

        role = st.session_state.mock_role
        skills = st.session_state.mock_skills
        experience = st.session_state.mock_experience
        interview_type = st.session_state.mock_type
        total = st.session_state.mock_total

        st.divider()

        st.subheader(f"🎤 Interview: {role}")

        st.write(
            f"**Candidate:** "
            f"{st.session_state.mock_candidate_name}"
        )

        st.write(
            f"**Level:** {experience} | "
            f"**Interview:** {interview_type}"
        )

        # ---------------------------------
        # PROGRESS BAR
        # ---------------------------------

        progress = (
            st.session_state.mock_question_number / total
        )

        st.progress(min(progress, 1.0))

        st.caption(
            f"Question {st.session_state.mock_question_number} "
            f"of {total}"
        )

        # ---------------------------------
        # GENERATE QUESTION
        # ---------------------------------

        if (
            st.session_state.mock_question is None
            and st.session_state.mock_question_number < total
        ):

            with st.spinner(
                "AI is preparing your next question..."
            ):

                try:

                    question_prompt = f"""

                    Conduct a realistic job interview.

                    Candidate role: {role}

                    Candidate skills: {skills}

                    Experience level: {experience}

                    Interview type: {interview_type}

                    Question number:
                    {st.session_state.mock_question_number + 1}

                    Previous interview conversation:
                    {st.session_state.mock_history}

                    Instructions:

                    1. Create ONE original interview question.
                    2. Adapt it to the candidate's role and skills.
                    3. Consider previous answers and evaluations.
                    4. Ask relevant follow-up questions when appropriate.
                    5. Avoid repeating questions.
                    6. Adjust difficulty based on performance.
                    7. Do not reveal the answer.
                    8. Return only ONE question.

                    """

                    question = generate_ai_response(
                        client,
                        [
                            {
                                "role": "system",
                                "content": (
                                    "You are an experienced professional "
                                    "technical and HR interviewer. "
                                    "Conduct realistic adaptive interviews."
                                )
                            },
                            {
                                "role": "user",
                                "content": question_prompt
                            }
                        ]
                    )

                    if not question or not question.strip():

                        raise ValueError(
                            "AI returned an empty interview question."
                        )

                    st.session_state.mock_question = question.strip()

                    st.session_state.mock_question_number += 1

                    st.rerun()

                except Exception as e:

                    st.error(
                        f"Question generation failed: {e}"
                    )

                    st.stop()

        # ---------------------------------
        # DISPLAY QUESTION
        # ---------------------------------

        if st.session_state.mock_question:

            st.subheader(
                f"Question "
                f"{st.session_state.mock_question_number} "
                f"of {total}"
            )

            st.info(st.session_state.mock_question)

            answer = st.text_area(
                "✍️ Enter your answer",
                placeholder="Explain your answer in your own words...",
                height=150,
                key=(
                    f"mock_answer_"
                    f"{st.session_state.mock_question_number}"
                ),
                disabled=st.session_state.mock_answer_submitted
            )

            # ---------------------------------
            # SUBMIT ANSWER
            # ---------------------------------

            if not st.session_state.mock_answer_submitted:

                if st.button(
                    "Submit My Answer",
                    type="primary"
                ):

                    if not answer.strip():

                        st.warning("Please enter your answer.")

                    else:

                        with st.spinner(
                            "AI is evaluating your answer..."
                        ):

                            try:

                                evaluation_prompt = f"""

                                Evaluate this interview response fairly.

                                Candidate role: {role}

                                Candidate skills: {skills}

                                Experience: {experience}

                                Question:
                                {st.session_state.mock_question}

                                Candidate answer:
                                {answer}

                                Return:

                                1. Score out of 10
                                2. Answer quality
                                3. Technical correctness
                                4. What the candidate did well
                                5. Missing important points
                                6. Suggestions for improvement
                                7. Example of a stronger answer

                                Be constructive and specific.

                                Do not predict guaranteed placement.

                                Clearly mention the score in this format:
                                Score: X/10

                                """

                                feedback = generate_ai_response(
                                    client,
                                    [
                                        {
                                            "role": "system",
                                            "content": (
                                                "You are a professional "
                                                "interview evaluator. "
                                                "Give fair and constructive "
                                                "feedback. Always provide "
                                                "a numeric score out of 10."
                                            )
                                        },
                                        {
                                            "role": "user",
                                            "content": evaluation_prompt
                                        }
                                    ]
                                )

                                if not feedback or not feedback.strip():

                                    raise ValueError(
                                        "AI returned empty evaluation feedback."
                                    )

                                # Save answer and evaluation
                                st.session_state.mock_history.append(
                                    {
                                        "question": (
                                            st.session_state.mock_question
                                        ),
                                        "answer": answer.strip(),
                                        "feedback": feedback
                                    }
                                )

                                st.session_state.mock_feedback = feedback

                                st.session_state.mock_answer_submitted = True

                                st.rerun()

                            except Exception as e:

                                st.error(
                                    f"Evaluation failed: {e}"
                                )

            # ---------------------------------
            # DISPLAY AI EVALUATION
            # ---------------------------------

            if st.session_state.mock_answer_submitted:

                st.divider()

                st.subheader("📊 AI Evaluation")

                st.markdown(
                    st.session_state.mock_feedback
                )

                # ---------------------------------
                # NEXT QUESTION OR FINISH
                # ---------------------------------

                if (
                    st.session_state.mock_question_number < total
                ):

                    if st.button(
                        "➡️ Next Interview Question"
                    ):

                        st.session_state.mock_question = None

                        st.session_state.mock_feedback = None

                        st.session_state.mock_answer_submitted = False

                        st.rerun()

                else:

                    if st.button(
                        "🏆 Finish Interview",
                        type="primary"
                    ):

                        st.session_state.mock_started = False

                        st.session_state.mock_completed = True

                        st.rerun()

        # ---------------------------------
        # END INTERVIEW
        # ---------------------------------

        if st.button("❌ End Interview"):

            reset_mock_interview()

            st.rerun()

    # =====================================
    # 3. FINAL INTERVIEW REPORT
    # =====================================

    if st.session_state.mock_completed:

        st.divider()

        st.title("🏆 Interview Performance Report")

        history = st.session_state.mock_history

        # ---------------------------------
        # CANDIDATE DETAILS
        # ---------------------------------

        st.markdown(
            f"""
            **Candidate Name:** {st.session_state.mock_candidate_name}

            **Target Role:** {st.session_state.mock_role}

            **Technical Skills:** {st.session_state.mock_skills}

            **Experience Level:** {st.session_state.mock_experience}

            **Interview Type:** {st.session_state.mock_type}

            **Questions Attempted:** {len(history)}
            """
        )

        st.divider()

        # ---------------------------------
        # GENERATE FINAL REPORT
        # ---------------------------------

        if history:

            if st.session_state.mock_final_report is None:

                with st.spinner(
                    "Generating your final performance report..."
                ):

                    try:

                        client = get_groq_client()

                        report_prompt = f"""

                        Prepare a detailed final interview performance report.

                        Candidate name:
                        {st.session_state.mock_candidate_name}

                        Candidate role:
                        {st.session_state.mock_role}

                        Candidate skills:
                        {st.session_state.mock_skills}

                        Experience:
                        {st.session_state.mock_experience}

                        Interview type:
                        {st.session_state.mock_type}

                        Interview answers and evaluations:
                        {history}

                        Include:

                        1. Overall performance summary
                        2. Average score if scores are available
                        3. Technical strengths
                        4. Weak areas
                        5. Communication assessment
                        6. Recommended skills to improve
                        7. Personalized next steps

                        Be honest, constructive and specific.

                        Do not invent scores.

                        Do not make unsupported claims about the candidate.

                        """

                        report = generate_ai_response(
                            client,
                            [
                                {
                                    "role": "system",
                                    "content": (
                                        "You are an expert career coach "
                                        "preparing a professional interview "
                                        "performance report."
                                    )
                                },
                                {
                                    "role": "user",
                                    "content": report_prompt
                                }
                            ]
                        )

                        if not report or not report.strip():

                            raise ValueError(
                                "AI returned an empty final report."
                            )

                        st.session_state.mock_final_report = report

                    except Exception as e:

                        st.error(
                            f"Report generation failed: {e}"
                        )

            # ---------------------------------
            # DISPLAY REPORT AND SAVE TO DB
            # ---------------------------------

            if st.session_state.mock_final_report:

                st.markdown(
                    st.session_state.mock_final_report
                )

                # Calculate average score
                scores = []

                for item in history:

                    score = extract_score(item["feedback"])

                    if score is not None:

                        scores.append(score)

                average_score = (
                    sum(scores) / len(scores)
                    if scores else 0.0
                )

                st.divider()

                st.subheader("📈 Interview Score")

                if scores:

                    st.metric(
                        "Average Score",
                        f"{average_score:.2f}/10"
                    )

                else:

                    st.warning(
                        "Could not extract numeric scores from "
                        "the AI feedback. The database will store "
                        "0.00 until scores are available."
                    )

                # ---------------------------------
                # SAVE INTERVIEW ONLY ONCE
                # ---------------------------------

                if not st.session_state.mock_saved:

                    try:

                        save_interview(
                            candidate_name=(
                                st.session_state.mock_candidate_name
                            ),
                            target_role=(
                                st.session_state.mock_role
                            ),
                            interview_type=(
                                st.session_state.mock_type
                            ),
                            total_questions=len(history),
                            average_score=average_score,
                            final_report=(
                                st.session_state.mock_final_report
                            ),
                            user_id=user_id
                        )

                        st.session_state.mock_saved = True

                        st.session_state.mock_save_error = None

                        st.success(
                            "✅ Interview result saved successfully!"
                        )

                    except Exception as e:

                        st.session_state.mock_save_error = str(e)

                        st.error(
                            f"Could not save interview result: {e}"
                        )

                else:

                    st.success(
                        "✅ Interview result is saved in the database."
                    )

                # ---------------------------------
                # RETRY SAVING IF FAILED
                # ---------------------------------

                if st.session_state.mock_save_error:

                    if st.button("🔁 Retry Saving Interview"):

                        try:

                            save_interview(
                                candidate_name=(
                                    st.session_state.mock_candidate_name
                                ),
                                target_role=(
                                    st.session_state.mock_role
                                ),
                                interview_type=(
                                    st.session_state.mock_type
                                ),
                                total_questions=len(history),
                                average_score=average_score,
                                final_report=(
                                    st.session_state.mock_final_report
                                ),
                                user_id=user_id
                            )

                            st.session_state.mock_saved = True

                            st.session_state.mock_save_error = None

                            st.success(
                                "Interview saved successfully!"
                            )

                            st.rerun()

                        except Exception as e:

                            st.session_state.mock_save_error = str(e)

                            st.error(
                                f"Saving failed again: {e}"
                            )

        else:

            st.warning(
                "No interview answers were recorded."
            )

        # ---------------------------------
        # START NEW INTERVIEW
        # ---------------------------------

        st.divider()

        if st.button(
            "🔄 Start a New Interview",
            type="primary"
        ):

            reset_mock_interview()

            st.rerun()
