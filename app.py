import streamlit as st

from modules.email_recon import email_recon
from modules.username_recon import username_recon
from modules.domain_recon import domain_recon

st.set_page_config(
    page_title="OSINTX",
    page_icon="🕵️",
    layout="wide"
)

st.title("🕵️ OSINTX")
st.caption("External Exposure Assessment Tool")

tab1, tab2, tab3 = st.tabs(
    ["Email", "Username", "Domain"]
)

with tab1:

    email = st.text_input(
        "Email Address"
    )

    if st.button(
        "Run Email Recon"
    ):

        result = email_recon(email)

        st.json(result)

with tab2:

    username = st.text_input(
        "Username"
    )

    if st.button(
        "Run Username Recon"
    ):

        result = username_recon(
            username
        )

        st.json(result)

with tab3:

    domain = st.text_input(
        "Domain"
    )

    if st.button(
        "Run Domain Recon"
    ):

        result = domain_recon(domain)

        st.json(result)

