import streamlit as st

from student_activity.ui import show_analyzer, show_safety_notice

st.title("Custom Analysis")
st.caption("Tell Gemini what to review, then upload an image.")

instruction = st.text_area(
    "Instruction",
    placeholder="Example: Describe what the students are doing.",
    height=110,
)

if not instruction.strip():
    st.info("Enter an instruction to enable analysis.")

show_analyzer(instruction=instruction, key_prefix="custom")
show_safety_notice()
