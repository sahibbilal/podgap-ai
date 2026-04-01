from fastapi import APIRouter, Depends
from app.api.deps import get_current_user_optional
from app.models import User
from typing import Annotated

from . import niche_gap, niche_intersection, trends, titles, competitive

router = APIRouter()
OptionalUser = Annotated[User | None, Depends(get_current_user_optional)]


def optional_auth_dep(user: OptionalUser):
    return user


router.include_router(niche_gap.router, prefix="/niche-gap", tags=["niche-gap"])
router.include_router(niche_intersection.router, prefix="/niche-intersection", tags=["niche-intersection"])
router.include_router(trends.router, prefix="/trends", tags=["trends"])
router.include_router(titles.router, prefix="/titles", tags=["titles"])
router.include_router(competitive.router, prefix="/competitive-map", tags=["competitive-map"])
