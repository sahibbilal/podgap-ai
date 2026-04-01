from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.api.deps import get_current_user_optional
from app.models import User
from app.schemas import Source
from typing import Annotated

router = APIRouter()


class NicheGapRequest(BaseModel):
    niche: str
    category: str | None = None


class TopicGap(BaseModel):
    topic: str
    search_volume_score: float
    episode_count: int
    opportunity_score: float
    saturation: str  # low | medium | high
    sources: list[Source] = []  # New: source links


class NicheGapResponse(BaseModel):
    niche: str
    topics: list[TopicGap]
    heat_map_data: list[dict]  # [{ "topic": str, "saturation": str, "value": float }]


@router.post("", response_model=NicheGapResponse)
async def run_niche_gap(
    body: NicheGapRequest,
    user: Annotated[User | None, Depends(get_current_user_optional)] = None,
):
    # TODO: call GapAnalyzer service (Listen Notes + vector DB + Ollama embeddings)
    # For now return stub with sources
    return NicheGapResponse(
        niche=body.niche,
        topics=[
            TopicGap(
                topic=f"Sample topic in {body.niche}",
                search_volume_score=0.7,
                episode_count=12,
                opportunity_score=0.85,
                saturation="low",
                sources=[
                    Source(name="Listen Notes", url="https://www.listennotes.com/", icon="🎙️"),
                    Source(name="Spotify for Podcasters", url="https://www.spotify.com/podcasters/", icon="🎵"),
                ]
            ),
        ],
        heat_map_data=[{"topic": body.niche, "saturation": "low", "value": 0.3}],
    )
