"""
Trend Service - Fetches trending topics from multiple sources:
- Google Trends
- Reddit API (PRAW)
- YouTube Data API
- Facebook trends
- Twitter/X trends
"""
from typing import Optional
from app.schemas import Source
from app.core.config import get_settings

# Placeholder implementations - will integrate with real APIs


class TrendService:
    """Service to fetch trending topics from multiple sources"""

    @staticmethod
    async def get_google_trends(period: str = "3m") -> list[dict]:
        """
        Fetch trends from Google Trends
        TODO: Integrate pytrends library
        """
        return [
            {
                "topic": "AI in education",
                "interest_score": 0.85,
                "trend_direction": "rising",
                "sources": [
                    Source(name="Google Trends", url="https://trends.google.com/trends/?geo=US", icon="🔍")
                ]
            },
        ]

    @staticmethod
    async def get_reddit_trends(period: str = "3m") -> list[dict]:
        """
        Fetch trending topics from Reddit
        TODO: Integrate PRAW (Reddit API)
        """
        return [
            {
                "topic": "Podcast production tips",
                "interest_score": 0.72,
                "trend_direction": "stable",
                "sources": [
                    Source(name="Reddit r/podcasting", url="https://www.reddit.com/r/podcasting/", icon="🔗"),
                    Source(name="Reddit r/Podcasts", url="https://www.reddit.com/r/Podcasts/", icon="🔗"),
                ]
            },
        ]

    @staticmethod
    async def get_youtube_trends(period: str = "3m") -> list[dict]:
        """
        Fetch trending topics from YouTube using YouTube Data API v3
        """
        settings = get_settings()
        
        if not settings.youtube_data_api_key:
            # Return placeholder if no API key
            return [
                {
                    "topic": "Short-form video content",
                    "interest_score": 0.88,
                    "trend_direction": "rising",
                    "sources": [
                        Source(name="YouTube Trending", url="https://www.youtube.com/feed/trending", icon="📺"),
                        Source(name="YouTube Shorts", url="https://www.youtube.com/shorts", icon="📺"),
                    ]
                },
            ]
        
        try:
            from googleapiclient.discovery import build
            
            # Build YouTube API client
            youtube = build('youtube', 'v3', developerKey=settings.youtube_data_api_key)
            
            # Fetch trending videos from multiple categories
            categories = {
                '26': 'Howto & Style',  # How-to content
                '22': 'People & Blogs',  # Personal content
                '24': 'Entertainment',   # Entertainment
                '28': 'Science & Technology',  # Tech
            }
            
            trending_topics = []
            
            for category_id, category_name in categories.items():
                # Get trending videos for this category
                request = youtube.videos().list(
                    part='snippet,statistics',
                    chart='mostPopular',
                    regionCode='US',
                    videoCategoryId=category_id,
                    maxResults=10
                )
                response = request.execute()
                
                # Extract topics from video titles and tags
                for video in response.get('items', []):
                    snippet = video['snippet']
                    stats = video['statistics']
                    
                    # Calculate interest score based on views and engagement
                    views = int(stats.get('viewCount', 0))
                    likes = int(stats.get('likeCount', 0))
                    comments = int(stats.get('commentCount', 0))
                    
                    # Simple engagement score (normalized)
                    engagement_rate = (likes + comments) / max(views, 1) if views > 0 else 0
                    interest_score = min(0.5 + (engagement_rate * 1000), 1.0)  # Cap at 1.0
                    
                    # Extract prominent words from title as topics
                    title = snippet['title']
                    video_url = f"https://www.youtube.com/watch?v={video['id']}"
                    
                    trending_topics.append({
                        'title': title,
                        'category': category_name,
                        'interest_score': interest_score,
                        'views': views,
                        'url': video_url,
                        'published_at': snippet['publishedAt']
                    })
            
            # Aggregate similar topics by category
            aggregated = []
            categories_seen = set()
            
            for topic_data in trending_topics[:5]:  # Top 5 diverse topics
                category = topic_data['category']
                if category not in categories_seen:
                    categories_seen.add(category)
                    aggregated.append({
                        "topic": f"Trending: {topic_data['title'][:50]}..." if len(topic_data['title']) > 50 else f"Trending: {topic_data['title']}",
                        "interest_score": round(topic_data['interest_score'], 2),
                        "trend_direction": "rising",
                        "sources": [
                            Source(
                                name=f"YouTube {category}",
                                url=topic_data['url'],
                                icon="📺"
                            ),
                        ]
                    })
            
            return aggregated if aggregated else [
                {
                    "topic": "YouTube trending content",
                    "interest_score": 0.85,
                    "trend_direction": "rising",
                    "sources": [
                        Source(name="YouTube Trending", url="https://www.youtube.com/feed/trending", icon="📺"),
                    ]
                }
            ]
            
        except Exception as e:
            # Log error and return placeholder
            print(f"Error fetching YouTube trends: {e}")
            return [
                {
                    "topic": "Short-form video content",
                    "interest_score": 0.88,
                    "trend_direction": "rising",
                    "sources": [
                        Source(name="YouTube Trending", url="https://www.youtube.com/feed/trending", icon="📺"),
                    ]
                },
            ]

    @staticmethod
    async def get_facebook_trends(period: str = "3m") -> list[dict]:
        """
        Fetch trending topics from Facebook
        TODO: Integrate Facebook API / Meta Business Suite
        """
        return [
            {
                "topic": "Community building for podcasters",
                "interest_score": 0.68,
                "trend_direction": "rising",
                "sources": [
                    Source(name="Facebook Creator Studio", url="https://www.facebook.com/creators/", icon="👥"),
                    Source(name="Facebook Groups", url="https://www.facebook.com/groups/", icon="👥"),
                ]
            },
        ]

    @staticmethod
    async def get_twitter_trends(period: str = "3m") -> list[dict]:
        """
        Fetch trending topics from Twitter/X
        TODO: Integrate Twitter/X API v2
        """
        return [
            {
                "topic": "Podcast growth strategies",
                "interest_score": 0.79,
                "trend_direction": "rising",
                "sources": [
                    Source(name="X (Twitter) Trends", url="https://twitter.com/explore/tabs/trending", icon="𝕏"),
                ]
            },
        ]

    @staticmethod
    async def aggregate_trends(period: str = "3m") -> list[dict]:
        """
        Aggregate trending topics from all sources
        Deduplicates similar trends and combines sources
        """
        # TODO: Implement deduplication and aggregation logic
        trends = []

        # Add trends from all sources
        trends.extend(await TrendService.get_google_trends(period))
        trends.extend(await TrendService.get_reddit_trends(period))
        trends.extend(await TrendService.get_youtube_trends(period))
        trends.extend(await TrendService.get_facebook_trends(period))
        trends.extend(await TrendService.get_twitter_trends(period))

        return trends
