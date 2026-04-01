from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from app.api.deps import get_current_user_optional
from app.models import User
from typing import Annotated

router = APIRouter()


class CompetitorItem(BaseModel):
    name: str
    episode_count: int
    topic_overlap: float
    positioning_axis_x: float
    positioning_axis_y: float


class UnderCoveredAngle(BaseModel):
    angle: str
    opportunity: str


class CompetitiveMapResponse(BaseModel):
    niche: str
    your_position: tuple[float, float] | None  # x, y for map
    competitors: list[CompetitorItem]
    under_covered_angles: list[UnderCoveredAngle]


@router.get("", response_model=CompetitiveMapResponse)
async def get_competitive_map(
    niche: Annotated[str, Query()],
    podcast_id: Annotated[str | None, Query()] = None,
    user: Annotated[User | None, Depends(get_current_user_optional)] = None,
):
    # TODO: CompetitiveMapService
    return CompetitiveMapResponse(
        niche=niche,
        your_position=(0.5, 0.5) if podcast_id else None,
        competitors=[
            CompetitorItem(name="Competitor A", episode_count=120, topic_overlap=0.6, positioning_axis_x=0.3, positioning_axis_y=0.7),
            CompetitorItem(name="Competitor B", episode_count=80, topic_overlap=0.4, positioning_axis_x=0.7, positioning_axis_y=0.4),
        ],
        under_covered_angles=[
            UnderCoveredAngle(angle="Beginner-focused episodes", opportunity="High demand, few shows"),
        ],
    )
