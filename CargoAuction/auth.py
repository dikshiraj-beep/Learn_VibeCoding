import streamlit as st
from supabase import Client, create_client

from db import _secret_or_env, get_session_factory
from models import Profile


@st.cache_resource
def get_supabase_client() -> Client:
    url = _secret_or_env("SUPABASE_URL")
    anon_key = _secret_or_env("SUPABASE_ANON_KEY")
    return create_client(url, anon_key)


def get_profile(user_id: str) -> Profile | None:
    session_factory = get_session_factory()
    with session_factory() as session:
        return session.get(Profile, user_id)


def upsert_profile(user_id: str, username: str, email: str, company_name: str, role: str = "customer") -> Profile:
    session_factory = get_session_factory()
    with session_factory() as session:
        profile = session.get(Profile, user_id)
        if profile is None:
            profile = Profile(id=user_id, username=username, email=email, company_name=company_name, role=role)
            session.add(profile)
        else:
            profile.username = username
            profile.company_name = company_name
        session.commit()
        session.refresh(profile)
        return profile


def sign_up(email: str, password: str, username: str, company_name: str) -> tuple[bool, str]:
    client = get_supabase_client()
    try:
        response = client.auth.sign_up({"email": email, "password": password})
    except Exception as exc:
        return False, str(exc)

    if response.user is None:
        return False, "Sign up failed. Please check your details and try again."

    upsert_profile(response.user.id, username, email, company_name, role="customer")

    if response.session is None:
        return True, "Account created. Check your email to confirm before logging in."

    st.session_state.auth_user = response.user
    st.session_state.auth_profile = get_profile(response.user.id)
    return True, "Account created and logged in."


def sign_in(email: str, password: str) -> tuple[bool, str]:
    client = get_supabase_client()
    try:
        response = client.auth.sign_in_with_password({"email": email, "password": password})
    except Exception as exc:
        return False, str(exc)

    if response.user is None:
        return False, "Invalid email or password."

    st.session_state.auth_user = response.user
    st.session_state.auth_profile = get_profile(response.user.id)
    return True, "Logged in."


def sign_out() -> None:
    client = get_supabase_client()
    try:
        client.auth.sign_out()
    except Exception:
        pass
    for key in ("auth_user", "auth_profile"):
        st.session_state.pop(key, None)


def current_profile() -> Profile | None:
    return st.session_state.get("auth_profile")


def render_login_form() -> None:
    st.title("Cargo Auction Login")
    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        with st.form("login_form", clear_on_submit=True):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Log in")
            if submitted:
                success, message = sign_in(email, password)
                if success:
                    st.rerun()
                else:
                    st.error(message)

    with register_tab:
        st.caption("Registration creates a customer account. Admin accounts are created separately.")
        with st.form("register_form", clear_on_submit=True):
            username = st.text_input("Username")
            company_name = st.text_input("Company name")
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            reg_submitted = st.form_submit_button("Create account")
            if reg_submitted:
                if not username or not reg_email or not reg_password:
                    st.warning("Username, email, and password are required.")
                else:
                    success, message = sign_up(reg_email, reg_password, username, company_name)
                    if success:
                        st.success(message)
                        if "auth_user" in st.session_state:
                            st.rerun()
                    else:
                        st.error(message)
