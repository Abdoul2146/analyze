import streamlit as st

st.set_page_config(page_title="Student Activity Review", layout="centered")
st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 760px;
        animation: screen-in 240ms ease-out;
    }
    @keyframes screen-in {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @media (prefers-reduced-motion: reduce) {
        .main .block-container { animation: none; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

navigation = st.navigation(
    [
        st.Page("pages/quick_analysis.py", title="Quick Analysis"),
        st.Page("pages/custom_analysis.py", title="Custom Analysis"),
    ],
    position="top",
)
navigation.run()
