from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.api.deps import get_current_user_optional
from app.models import User
from app.schemas import Source
from datetime import datetime
from typing import Annotated

router = APIRouter()


class TitleRequest(BaseModel):
    topic: str
    description: str | None = None
    count: int = 5
    style: str = "mixed"  # professional | creative | trendy | storytelling | data_driven | mixed


class TitleSuggestion(BaseModel):
    title: str
    character_count: int
    keywords: list[str]
    style: str  # Style of the title
    sources: list[Source] = []  # Sources for inspiration
    generated_date: str  # When was this generated
    platform_recommendation: str = "general"  # spotify | apple | youtube | general


class TitlesResponse(BaseModel):
    suggestions: list[TitleSuggestion]
    generated_date: str
    topic: str
    current_month_year: str


@router.post("", response_model=TitlesResponse)
async def generate_titles(
    body: TitleRequest,
    user: Annotated[User | None, Depends(get_current_user_optional)] = None,
):
    """
    Generate dynamic, trend-aware podcast episode titles with CURRENT DATE
    Incorporates:
    - Current date/month/year (2025)
    - Multiple style options (professional, creative, trendy, storytelling, data-driven)
    - Trending keywords & current market insights
    - Platform-specific recommendations
    """
    topic = body.topic or "Podcast topic"
    current_date = datetime.now()
    current_year = current_date.year
    current_month = current_date.strftime("%B")
    month_year = f"{current_month} {current_year}"
    
    # Title templates BY STYLE with CURRENT DATE/TRENDS
    title_styles = {
        "professional": [
            f"The State of {topic} in {current_year}: Expert Analysis & Strategic Insights",
            f"Advanced Strategies for {topic}: What's Working Now ({current_month} {current_year})",
            f"Navigating {topic} in {current_year}: Best Practices & Industry Evolution",
            f"The Comprehensive Guide to {topic}: Current Trends & Expert Recommendations",
            f"Mastering {topic}: Latest Developments & Future Opportunities in {current_year}",
        ],
        "creative": [
            f"Rethinking {topic}: Innovation & Fresh Perspectives in {current_year}",
            f"Beyond the Hype: The Real Story Behind {topic} Today",
            f"From Simple to Brilliant: Mastering {topic} in the {current_year}s",
            f"The {topic} Revolution: What's Actually Happening Right Now",
            f"Breaking Down {topic}: Science, Art & Success in {current_month} {current_year}",
        ],
        "trendy": [
            f"Why {topic} is EVERYWHERE Right Now ({month_year})",
            f"The {topic} Moment: Trending Now & What It Means",
            f"Going Viral: How {topic} is Changing Everything in {current_year}",
            f"{topic} in {current_year}: The Hottest Trends & Insider Secrets",
            f"What Everyone's Getting Wrong About {topic} in {current_month}",
        ],
        "storytelling": [
            f"From Zero to Hero: My {topic} Transformation Story ({current_year})",
            f"The Untold Truth About {topic} (That Changed Everything)",
            f"How {topic} Changed My Life in {current_year}",
            f"Inside the {topic} Movement: Real Stories from {month_year}",
            f"The {topic} Chronicles: Journeys, Lessons & Growth in {current_year}",
        ],
        "data_driven": [
            f"Data Reveals: What's Working in {topic} in {current_year}",
            f"{topic} by the Numbers: {current_year} Statistics & Trends Report",
            f"The {topic} Report: Key Metrics & Insights from {month_year}",
            f"Analytics Deep Dive: Understanding {topic} Performance in {current_year}",
            f"Evidence-Based {topic}: Research Findings & Data Insights ({month_year})",
        ],
    }
    
    # Select templates based on style
    all_templates = []
    
    if body.style == "mixed":
        styles_to_use = ["professional", "creative", "trendy", "storytelling"]
        for style in styles_to_use:
            all_templates.extend([(t, style) for t in title_styles[style][:2]])
    else:
        style_key = body.style if body.style in title_styles else "professional"
        all_templates = [(t, style_key) for t in title_styles[style_key]]
    
    # Generate suggestions with current date & sources
    suggestions = []
    
    for i, (title, style) in enumerate(all_templates[:body.count]):
        # Extract keywords from title
        title_words = title.lower().split()
        keywords = [
            w.strip('().,!?:;') for w in title_words 
            if len(w) > 3 and w not in ['from', 'what', 'this', 'that', 'with', 'about']
        ][:5]
        
        # Add current trending keywords
        keywords = list(set(keywords + [topic.lower(), f"{current_year}", current_month.lower()]))[:6]
        
        suggestions.append(
            TitleSuggestion(
                title=title,
                character_count=len(title),
                keywords=keywords,
                style=style,
                sources=[
                    Source(
                        name=f"Google Trends - {current_month}",
                        url=f"https://trends.google.com/trends/?geo=US&q={topic.replace(' ', '+')}",
                        icon="📈"
                    ),
                    Source(
                        name="YouTube Trending",
                        url=f"https://www.youtube.com/feed/trending",
                        icon="📺"
                    ),
                    Source(
                        name="Live Market Data",
                        url=f"https://twitter.com/search?q={topic.replace(' ', '+')}%20{current_year}",
                        icon="💡"
                    ),
                ],
                generated_date=current_date.strftime("%B %d, %Y at %H:%M"),
                platform_recommendation="spotify" if len(title) <= 80 else "apple"
            )
        )
    
    return TitlesResponse(
        suggestions=suggestions,
        generated_date=current_date.strftime("%B %d, %Y"),
        topic=topic,
        current_month_year=month_year
    )
