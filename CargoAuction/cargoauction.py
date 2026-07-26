import streamlit as st

from auth import current_profile, render_login_form, sign_out
from models import init_db

st.set_page_config(page_title="Cargo Auction", page_icon="🚢", layout="wide")

try:
    init_db()
except Exception as exc:
    st.error(f"Database connection failed: {exc}")
    st.stop()

if "auth_user" not in st.session_state:
    login_page = st.Page(render_login_form, title="Login")
    st.navigation([login_page], position="hidden").run()
    st.stop()

profile = current_profile()
if profile is None:
    st.error("Logged in, but no profile record was found. Please contact an administrator.")
    if st.button("Log out"):
        sign_out()
        st.rerun()
    st.stop()

with st.sidebar:
    st.write(f"**{profile.username}**")
    st.caption(f"{profile.role} · {profile.email}")
    if st.button("Log out"):
        sign_out()
        st.rerun()

if profile.role == "admin":
    pages = [
        st.Page("pages/3_Admin_Vessels.py", title="Manage Vessels", icon="🚢"),
        st.Page("pages/4_Admin_Auctions.py", title="Manage Auctions", icon="📋"),
    ]
else:
    pages = [
        st.Page("pages/1_Browse_Auctions.py", title="Browse Auctions", icon="🔍"),
        st.Page("pages/2_My_Bids.py", title="My Bids", icon="📄"),
    ]

pg = st.navigation(pages)
pg.run()
