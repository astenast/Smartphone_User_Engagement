import streamlit as st

def app():
    st.header("Info")
    st.markdown(
        "If you are interested in the technical details, our implementations are available on GitHub.")
    left, mid, right = st.columns(3)

    with mid:
        if st.button('GitHub Repo'):
            html_temp = """<a href="https://github.com/astenast/Smartphone_User_Engagement.git" target="_blank">Link to our GitHub Repo</a>"""
            st.markdown(html_temp, unsafe_allow_html=True)

    st.markdown(
        "Created for the assignment of 02830 Advanced project in Digital Media Engineering course offered by the Technical University of Denmark.")

    html_temp = """
            <div align="center">
            <br>
            <h6 style="text-align:center;">Copyright, 2021</h6>
            <h6 style="text-align:center;">Electra Zarafeta, Asterios Nastas</h6>
            </div><br>"""
    st.markdown(html_temp, unsafe_allow_html=True)

    st.balloons()