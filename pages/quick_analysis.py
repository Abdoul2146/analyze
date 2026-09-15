import streamlit as st

from student_activity.ui import show_analyzer, show_safety_notice

QUICK_INSTRUCTION = (
    "Describe the visible scene and activities in clear detail. Identify only "
    "directly visible potential concerns and whether supervisor attention may be "
    "appropriate."
)

st.title("Quick Analysis")
st.caption("Upload an image for an immediate structured observation.")

show_analyzer(instruction=QUICK_INSTRUCTION, key_prefix="quick")
show_safety_notice()
