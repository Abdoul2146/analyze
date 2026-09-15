from typing import Literal

from pydantic import BaseModel, Field


class ActivityAnalysis(BaseModel):
    caption: str = Field(description="A short, neutral caption of visible facts.")
    visible_activities: list[str] = Field(
        description="Only activities directly visible in the image."
    )
    potential_concerns: list[str] = Field(
        description="Visible concerns, or an empty list when none are visible."
    )
    supervisor_attention: Literal["needed", "not_needed", "uncertain"]
    explanation: str = Field(
        description="A brief evidence-based reason for the attention rating."
    )
    confidence_and_limitations: str = Field(
        description="Uncertainty and limitations of judging one image."
    )
