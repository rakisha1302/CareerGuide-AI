
import sqlite3
import hashlib
import streamlit as st

DATABASE_NAME = "career_guide.db"


# ==========================================
# DATABASE
# ==========================================

def create_users_table():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(name, email, password):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
        """, (name, email.lower(), hash_password(password)))

        conn.commit()
        return True, "Account created successfully!"

    except sqlite3.IntegrityError:
        return False, "This email is already registered."

    finally:
        conn.close()


def login_user(email, password):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email
        FROM users
        WHERE email = ? AND password = ?
    """, (email.lower(), hash_password(password)))

    user = cursor.fetchone()
    conn.close()

    return user


# ==========================================
# LOGIN PAGE DESIGN
# ==========================================

def show_auth_page():

    create_users_table()

    st.markdown("""
    <style>

    /* Main background */
    .stApp {
        background:
            linear-gradient(
                180deg,
                #dceaff 0%,
                #b8d9f7 45%,
                #6eabd5 75%,
                #17465d 100%
            );
        min-height: 100vh;
    }

    /* Hide Streamlit header */
    header[data-testid="stHeader"] {
        background: transparent;
    }

    /* Main content */
    .block-container {
        padding-top: 1rem;
        max-width: 1100px;
    }

    /* Navigation bar */
    .nav-title {
        font-size: 25px;
        font-weight: 800;
        color: #172c50;
        letter-spacing: 1px;
    }

    .nav-links {
        text-align: right;
        color: #172c50;
        font-size: 14px;
        font-weight: 700;
        padding-top: 12px;
    }

    /* Welcome heading */
    .welcome-heading {
        text-align: center;
        color: #172c50;
        font-size: 34px;
        font-weight: 800;
        margin-top: 45px;
        margin-bottom: 8px;
    }

    .welcome-caption {
        text-align: center;
        color: #314d70;
        font-size: 15px;
        margin-bottom: 25px;
    }

    /* Glass login card */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.30);
        border: 1px solid rgba(255, 255, 255, 0.55);
        border-radius: 22px;
        box-shadow: 0 15px 40px rgba(15, 48, 80, 0.18);
        backdrop-filter: blur(18px);
        padding: 20px;
    }

    /* Input fields */
    .stTextInput input {
        background: rgba(255, 255, 255, 0.82);
        border: none;
        border-bottom: 2px solid #426c94;
        border-radius: 7px;
        color: #172c50;
    }

    /* Buttons */
    .stButton button {
        width: 100%;
        border: none;
        border-radius: 9px;
        background: linear-gradient(90deg, #4776cf, #7058d9);
        color: white;
        font-weight: 700;
        min-height: 45px;
        transition: 0.3s;
    }

    .stButton button:hover {
        background: linear-gradient(90deg, #315da9, #5540bd);
        color: white;
        border: none;
        transform: translateY(-2px);
    }

    /* Radio options */
    .stRadio label {
        color: #172c50 !important;
        font-weight: 600;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #ffffff;
        font-size: 13px;
        margin-top: 30px;
    }

    </style>
    """, unsafe_allow_html=True)

    # Navigation
    nav1, nav2 = st.columns([1, 2])

    with nav1:
        st.markdown(
            '<div class="nav-title">🎓 CareerGuide AI</div>',
            unsafe_allow_html=True
        )

    with nav2:
        st.markdown(
            '<div class="nav-links">HOME　 ABOUT　 SERVICES　 CONTACT</div>',
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="welcome-heading">Welcome to Your Future</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="welcome-caption">'
        'Your AI-powered career companion. Discover your potential.'
        '</div>',
        unsafe_allow_html=True
    )

    # Center login card
    left, center, right = st.columns([1, 1.5, 1])

    with center:

        with st.container(border=True):

            st.markdown(
                "<h2 style='text-align:center;color:#172c50;'>"
                "STUDENT ACCOUNT</h2>",
                unsafe_allow_html=True
            )

            choice = st.radio(
                "Select an option",
                ["Login", "Register"],
                horizontal=True,
                label_visibility="collapsed"
            )

            st.divider()

            # ==================================
            # REGISTRATION
            # ==================================

            if choice == "Register":

                st.subheader("Create Your Account")

                name = st.text_input(
                    "Full Name",
                    key="register_name",
                    placeholder="Enter your full name"
                )

                email = st.text_input(
                    "Email Address",
                    key="register_email",
                    placeholder="Enter your email"
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    key="register_password",
                    placeholder="Create a password"
                )

                confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    key="confirm_password",
                    placeholder="Re-enter your password"
                )

                if st.button("Create Account", key="register_button"):

                    if not all([
                        name.strip(),
                        email.strip(),
                        password,
                        confirm_password
                    ]):
                        st.error("Please fill in all fields.")

                    elif "@" not in email or "." not in email:
                        st.error("Enter a valid email address.")

                    elif len(password) < 8:
                        st.error("Password must contain at least 8 characters.")

                    elif password != confirm_password:
                        st.error("Passwords do not match.")

                    else:
                        success, message = register_user(
                            name.strip(),
                            email.strip(),
                            password
                        )

                        if success:
                            st.success(message)
                            st.info("Select Login to access your account.")
                        else:
                            st.error(message)

            # ==================================
            # LOGIN
            # ==================================

            else:

                st.subheader("Student Login")

                email = st.text_input(
                    "Email Address",
                    key="login_email",
                    placeholder="Enter your email"
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    key="login_password",
                    placeholder="Enter your password"
                )

                remember = st.checkbox("Remember Me")

                if st.button("Login", key="login_button"):

                    if not email.strip() or not password:
                        st.warning("Please enter your email and password.")

                    else:
                        user = login_user(email.strip(), password)

                        if user:
                            st.session_state.logged_in = True
                            st.session_state.user_id = user[0]
                            st.session_state.user_name = user[1]
                            st.session_state.user_email = user[2]

                            st.rerun()

                        else:
                            st.error("Invalid email or password.")

                st.caption(
                    "Don't have an account? Select Register above."
                )

    st.markdown(
        '<div class="footer">'
        '© 2026 CareerGuide AI | Your Journey, Your Future'
        '</div>',
        unsafe_allow_html=True
    )
