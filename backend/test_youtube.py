"""Test YouTube Data API integration"""
import asyncio
from app.services.trend_service import TrendService
from app.core.config import get_settings

async def test_youtube_trends():
    """Test fetching YouTube trends"""
    settings = get_settings()
    print(f"YouTube API Key configured: {bool(settings.youtube_data_api_key)}")
    print(f"API Key starts with: {settings.youtube_data_api_key[:10] if settings.youtube_data_api_key else 'None'}...")
    
    print("\nFetching YouTube trends...")
    trends = await TrendService.get_youtube_trends()
    
    print(f"\nFound {len(trends)} trends:")
    for i, trend in enumerate(trends, 1):
        print(f"\n{i}. {trend['topic']}")
        print(f"   Score: {trend['interest_score']}")
        print(f"   Direction: {trend['trend_direction']}")
        print(f"   Sources: {len(trend['sources'])}")

if __name__ == "__main__":
    asyncio.run(test_youtube_trends())
