from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from app.api.deps import get_current_user_optional
from app.models import User
from app.schemas import Source
from app.services import TrendService
from typing import Annotated

router = APIRouter()


class TrendItem(BaseModel):
    topic: str
    interest_score: float
    trend_direction: str  # rising | stable | declining
    sources: list[Source] = []  # New: source links from multiple platforms


class TrendsResponse(BaseModel):
    trends: list[TrendItem]
    period: str


@router.get("", response_model=TrendsResponse)
async def get_trends(
    period: Annotated[str | None, Query(description="3m | 6m | 12m")] = "3m",
    source: Annotated[str | None, Query(description="all | google | reddit | youtube | facebook | twitter")] = "all",
    user: Annotated[User | None, Depends(get_current_user_optional)] = None,
):
    """
    Get trending podcast topics from multiple sources
    - Google Trends
    - Reddit
    - YouTube Trending
    - Facebook Groups
    - Twitter/X Trends
    """
    trends = []
    
    # Fetch trends from specified source(s)
    if source == "all" or source == "youtube":
        youtube_trends = await TrendService.get_youtube_trends(period)
        trends.extend(youtube_trends)
    
    if source == "all" or source == "google":
        google_trends = await TrendService.get_google_trends(period)
        trends.extend(google_trends)
    
    if source == "all" or source == "reddit":
        reddit_trends = await TrendService.get_reddit_trends(period)
        trends.extend(reddit_trends)
    
    if source == "all" or source == "facebook":
        facebook_trends = await TrendService.get_facebook_trends(period)
        trends.extend(facebook_trends)
    
    if source == "all" or source == "twitter":
        twitter_trends = await TrendService.get_twitter_trends(period)
        trends.extend(twitter_trends)
    
    # Convert to TrendItem format
    trend_items = [
        TrendItem(
            topic=t.get("topic", ""),
            interest_score=t.get("interest_score", 0.0),
            trend_direction=t.get("trend_direction", "stable"),
            sources=t.get("sources", [])
        )
        for t in trends
    ]
    
    return TrendsResponse(
        period=period,
        trends=trend_items
    )
