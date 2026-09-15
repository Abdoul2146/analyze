import os

import streamlit as st
from PIL import Image, UnidentifiedImageError
from streamlit.errors import StreamlitSecretNotFoundError

from student_activity.gemini_service import analyze_image

MAX_FILE_SIZE = 10 * 1024 * 1024
DEFAULT_INSTRUCTION = (
    "Analyze student activity and identify anything needing attention."
)


def get_api_key() -> str | None:
    try:
        return st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    except (FileNotFoundError, StreamlitSecretNotFoundError):
        return os.getenv("GEMINI_API_KEY")


def show_result(result) -> None:
    st.subheader("Caption")
    st.write(result.caption)

    st.subheader("Observed activity")
    for activity in result.visible_activities:
        st.write(f"- {activity}")

    st.subheader("Potential concerns")
    if result.potential_concerns:
        for concern in result.potential_concerns:
            st.write(f"- {concern}")
    else:
        st.write("None visible in this image.")

    attention = result.supervisor_attention.upper()
    if attention == "NEEDED":
        st.error(f"Supervisor attention: {attention}")
    elif attention == "UNCERTAIN":
        st.warning(f"Supervisor attention: {attention}")
    else:
        st.success(f"Supervisor attention: {attention}")

    st.subheader("Reason")
    st.write(result.explanation)
    st.caption(f"Confidence and limitations: {result.confidence_and_limitations}")


def show_header(step: int, description: str) -> None:
    st.caption(f"STEP {step} OF 2")
    st.title("Student Activity Review")
    st.caption(description)


def show_instruction_screen() -> None:
    show_header(1, "Describe what you want Gemini to review.")
    instruction = st.text_area(
        "Instruction",
        value=st.session_state.saved_instruction,
        key="instruction_input",
        height=120,
    )

    if st.button("Continue", type="primary", use_container_width=True):
        if not instruction.strip():
            st.error("Enter an instruction.")
        else:
            st.session_state.saved_instruction = instruction.strip()
            st.session_state.screen = "upload"
            st.session_state.pop("analysis_result", None)
            st.rerun()

    with st.expander("Privacy and safety", expanded=False):
        st.write(
            "Do not use this tool to identify students or infer emotions, health, "
            "disability, intent, or guilt. Use only appropriately consented images. "
            "Uploads are processed in memory and are not saved by this app."
        )


def show_upload_screen() -> None:
    show_header(2, "Upload an image and review the structured observation.")

    if st.button("Back to instruction"):
        st.session_state.screen = "instruction"
        st.session_state.pop("analysis_result", None)
        st.rerun()

    st.caption("Instruction")
    st.info(st.session_state.saved_instruction)

    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png", "webp"],
        help="JPG, PNG, or WebP; maximum 10 MB.",
        key="image_upload",
    )

    valid_image = uploaded_file is not None
    if uploaded_file is not None:
        if uploaded_file.size > MAX_FILE_SIZE:
            st.error("The image is larger than 10 MB.")
            valid_image = False
        else:
            try:
                with Image.open(uploaded_file) as image:
                    image.verify()
                uploaded_file.seek(0)
                st.image(uploaded_file, caption="Image to analyze", width=500)
            except (UnidentifiedImageError, OSError):
                st.error("This file is not a valid supported image.")
                valid_image = False

    if st.button(
        "Analyze", type="primary", disabled=not valid_image, use_container_width=True
    ):
        api_key = get_api_key()
        if not api_key:
            st.error("Set GEMINI_API_KEY in Streamlit secrets or the environment.")
        else:
            image_bytes = uploaded_file.getvalue()
            with st.spinner("Analyzing image..."):
                try:
                    st.session_state.analysis_result = analyze_image(
                        image_bytes=image_bytes,
                        mime_type=uploaded_file.type,
                        instruction=st.session_state.saved_instruction,
                        api_key=api_key,
                    )
                except Exception as exc:
                    st.error(f"Analysis failed: {exc}")
                finally:
                    del image_bytes

    if result := st.session_state.get("analysis_result"):
        st.divider()
        show_result(result)


st.set_page_config(page_title="Student Activity Review")
st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 720px;
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

st.session_state.setdefault("screen", "instruction")
st.session_state.setdefault("saved_instruction", DEFAULT_INSTRUCTION)

if st.session_state.screen == "instruction":
    show_instruction_screen()
else:
    show_upload_screen()

st.divider()
st.caption(
    "This output is an AI-generated observation, not an automated safety decision. "
    "When context is insufficient, treat the result as uncertain."
)
