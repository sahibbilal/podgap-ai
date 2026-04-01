from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.api.deps import get_current_user_optional
from app.models import User
from app.schemas import Source
from typing import Annotated

router = APIRouter()


class NicheIntersectionRequest(BaseModel):
    niche_a: str
    niche_b: str | None = None


class NicheCombo(BaseModel):
    combination: str
    opportunity_score: float
    rationale: str
    sources: list[Source] = []  # New: source links


class NicheIntersectionResponse(BaseModel):
    niche_a: str
    niche_b: str | None
    opportunity_score: float
    suggestions: list[NicheCombo]


@router.post("", response_model=NicheIntersectionResponse)
async def run_niche_intersection(
    body: NicheIntersectionRequest,
    user: Annotated[User | None, Depends(get_current_user_optional)] = None,
):
    # TODO: IntersectionFinder service
    combo = f"{body.niche_a} + {body.niche_b}" if body.niche_b else body.niche_a
    return NicheIntersectionResponse(
        niche_a=body.niche_a,
        niche_b=body.niche_b,
        opportunity_score=0.72,
        suggestions=[
            NicheCombo(
                combination=combo,
                opportunity_score=0.72,
                rationale="Emerging intersection with low competition.",
                sources=[
                    Source(name="Listen Notes", url="https://www.listennotes.com/", icon="🎙️"),
                    Source(name="Podtrac Analytics", url="https://analytics.podtrac.com/", icon="📊"),
                ]
            ),
        ],
    )
