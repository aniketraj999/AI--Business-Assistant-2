import streamlit as st
import hashlib
import time

# -----------------------------
# Change your password here
# -----------------------------
PASSWORD = "Aniket@123"

PASSWORD_HASH = hashlib.sha256(PASSWORD.encode()).hexdigest()


def verify_password(password):
    return hashlib.sha256(password.encode()).hexdigest() == PASSWORD_HASH


def login():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        return

    st.markdown("""
<style>

.stApp{
background:linear-gradient(-45deg,#0F172A,#1D4ED8,#2563EB,#7C3AED);
background-size:400% 400%;
animation:bg 12s ease infinite;
}

@keyframes bg{

0%{background-position:0% 50%;}

50%{background-position:100% 50%;}

100%{background-position:0% 50%;}

}

.login-card{

width:500px;

margin:auto;

margin-top:90px;

padding:40px;

border-radius:25px;

background:rgba(255,255,255,.10);

backdrop-filter:blur(25px);

border:1px solid rgba(255,255,255,.25);

box-shadow:0 20px 60px rgba(0,0,0,.30);

animation:popup .7s ease;

}

@keyframes popup{

from{

opacity:0;

transform:translateY(30px);

}

to{

opacity:1;

transform:translateY(0);

}

}

.lock{

font-size:70px;

text-align:center;

}

.title{

text-align:center;

font-size:34px;

font-weight:bold;

color:white;

}

.subtitle{

text-align:center;

color:#ddd;

margin-bottom:20px;

}

</style>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="login-card">

<div class="lock">🔒</div>

<div class="title">Enterprise Dashboard</div>

<div class="subtitle">

Secure Login Required

</div>

</div>
""", unsafe_allow_html=True)

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter password"
    )

    if st.button(
        "🚀 Unlock Dashboard",
        use_container_width=True
    ):

        if verify_password(password):

            with st.spinner("Authenticating..."):

                time.sleep(1.5)

            st.success("Welcome 👋")

            st.balloons()

            st.session_state.logged_in = True

            st.rerun()

        else:

            st.error("Incorrect Password")

    st.stop()
