import os

from google import genai
from google.genai import types

from student_activity.prompt import build_prompt
from student_activity.schema import ActivityAnalysis

DEFAULT_MODEL = "gemini-3.6-flash"


def analyze_image(
    *, image_bytes: bytes, mime_type: str, instruction: str, api_key: str
) -> ActivityAnalysis:
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", DEFAULT_MODEL),
        contents=[
            build_prompt(instruction),
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
        ],
        config=types.GenerateContentConfig(
            temperature=0.1,
            response_mime_type="application/json",
            response_schema=ActivityAnalysis,
        ),
    )

    if response.parsed is None:
        raise RuntimeError("Gemini returned no structured analysis.")
    return response.parsed
