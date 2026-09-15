import hashlib
import os

import streamlit as st
from PIL import Image, UnidentifiedImageError
from streamlit.errors import StreamlitSecretNotFoundError

from student_activity.gemini_service import analyze_image

MAX_FILE_SIZE = 10 * 1024 * 1024


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

    st.subheader("Malpractice review index")
    st.metric("Visible indicator score", f"{result.malpractice_index}/10")
    st.progress(result.malpractice_index / 10)
    st.write(result.malpractice_index_reason)
    st.caption(
        "This review index does not establish cheating, intent, or guilt. "
        "A human must assess the surrounding context."
    )

    attention = result.supervisor_attention.upper().replace("_", " ")
    if attention == "NEEDED":
        st.error(f"Supervisor attention: {attention}")
    elif attention == "UNCERTAIN":
        st.warning(f"Supervisor attention: {attention}")
    else:
        st.success(f"Supervisor attention: {attention}")

    st.subheader("Reason")
    st.write(result.explanation)
    st.caption(f"Confidence and limitations: {result.confidence_and_limitations}")


def show_analyzer(*, instruction: str, key_prefix: str) -> None:
    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png", "webp"],
        help="JPG, PNG, or WebP; maximum 10 MB.",
        key=f"{key_prefix}_image",
    )

    image_bytes = None
    if uploaded_file is not None:
        if uploaded_file.size > MAX_FILE_SIZE:
            st.error("The image is larger than 10 MB.")
        else:
            try:
                with Image.open(uploaded_file) as image:
                    image.verify()
                uploaded_file.seek(0)
                image_bytes = uploaded_file.getvalue()
                st.image(uploaded_file, caption="Image to analyze", width=500)
            except (UnidentifiedImageError, OSError):
                st.error("This file is not a valid supported image.")

    request_id = None
    if image_bytes is not None and instruction.strip():
        request_id = hashlib.sha256(
            image_bytes + instruction.strip().encode("utf-8")
        ).hexdigest()

    if st.button(
        "Analyze",
        type="primary",
        disabled=request_id is None,
        use_container_width=True,
        key=f"{key_prefix}_analyze",
    ):
        api_key = get_api_key()
        if not api_key:
            st.error("Set GEMINI_API_KEY in Streamlit secrets or the environment.")
        else:
            with st.spinner("Analyzing image..."):
                try:
                    st.session_state[f"{key_prefix}_result"] = analyze_image(
                        image_bytes=image_bytes,
                        mime_type=uploaded_file.type,
                        instruction=instruction.strip(),
                        api_key=api_key,
                    )
                    st.session_state[f"{key_prefix}_request_id"] = request_id
                except Exception as exc:
                    st.error(f"Analysis failed: {exc}")

    if (
        request_id is not None
        and st.session_state.get(f"{key_prefix}_request_id") == request_id
    ):
        st.divider()
        show_result(st.session_state[f"{key_prefix}_result"])


def show_safety_notice() -> None:
    with st.expander("Privacy and safety", expanded=False):
        st.write(
            "Do not use this tool to identify students or infer emotions, health, "
            "disability, intent, or guilt. Use only appropriately consented images. "
            "Uploads are processed in memory and are not saved by this app."
        )

    st.divider()
    st.caption(
        "This output is an AI-generated observation, not an automated safety "
        "decision. When context is insufficient, treat the result as uncertain."
    )
