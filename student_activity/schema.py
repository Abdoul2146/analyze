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
    malpractice_index: int = Field(
        ge=1,
        le=10,
        description=(
            "A conservative 1-10 review index based only on directly visible "
            "indicators, not a finding of cheating or guilt."
        ),
    )
    malpractice_index_reason: str = Field(
        description="Visible evidence and uncertainty supporting the review index."
    )
    supervisor_attention: Literal["needed", "not_needed", "uncertain"]
    explanation: str = Field(
        description="A brief evidence-based reason for the attention rating."
    )
    confidence_and_limitations: str = Field(
        description="Uncertainty and limitations of judging one image."
    )
