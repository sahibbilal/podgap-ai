"""
Title Generator Service - Generates podcast episode titles
Uses:
- Ollama LLM (llama3.2) - Local AI model for title generation
- Keyword extraction
- Character count optimization for various platforms
"""
from typing import Optional
from app.schemas import Source


class TitleGenerator:
    """Service to generate podcast episode titles using AI"""

    @staticmethod
    async def generate_titles(
        topic: str,
        description: Optional[str] = None,
        count: int = 5,
        style: str = "professional"  # professional | creative | clickbait
    ) -> list[dict]:
        """
        Generate creative podcast episode titles
        TODO: Integrate with Ollama LLM (llama3.2)
        """
        # Placeholder titles - in production these would come from Ollama
        titles = [
            {
                "title": f"The Art and Science of {topic}: Expert Insights for 2025",
                "character_count": len(f"The Art and Science of {topic}: Expert Insights for 2025"),
                "keywords": [topic.lower(), "expert", "insights", "2025"],
                "source": "Ollama (llama3.2) - Professional Style"
            },
            {
                "title": f"From Zero to Hero in {topic}: A Complete Guide",
                "character_count": len(f"From Zero to Hero in {topic}: A Complete Guide"),
                "keywords": [topic.lower(), "guide", "tutorial"],
                "source": "Ollama (llama3.2) - Educational Style"
            },
            {
                "title": f"Why Everyone's Talking About {topic} in 2025",
                "character_count": len(f"Why Everyone's Talking About {topic} in 2025"),
                "keywords": [topic.lower(), "trending", "2025", "discussion"],
                "source": "Ollama (llama3.2) - Trendy Style"
            },
        ]

        return titles[:count]

    @staticmethod
    async def optimize_for_platform(
        title: str,
        platform: str = "spotify"  # spotify | apple | youtube | custom
    ) -> dict:
        """
        Optimize title for specific podcast platform constraints
        - Spotify: max 100 characters
        - Apple Podcasts: max 255 characters
        - YouTube: max 100 characters
        """
        max_lengths = {
            "spotify": 100,
            "apple": 255,
            "youtube": 100,
            "custom": 255,
        }

        max_length = max_lengths.get(platform, 255)
        optimized = title if len(title) <= max_length else title[:max_length - 3] + "..."

        return {
            "original": title,
            "optimized": optimized,
            "platform": platform,
            "character_count": len(optimized),
            "within_limits": len(title) <= max_length,
            "sources": [
                Source(name="Ollama (llama3.2)", url="https://ollama.ai/", icon="🤖"),
            ]
        }

    @staticmethod
    async def extract_keywords(title: str, max_keywords: int = 5) -> list[str]:
        """
        Extract important keywords from a title
        TODO: Use NLP/Ollama for better extraction
        """
        # Simple placeholder implementation
        words = title.lower().split()
        # Filter out common stop words
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "for", "of", "to"}
        keywords = [w for w in words if w not in stop_words and len(w) > 3]
        return keywords[:max_keywords]

    @staticmethod
    async def rate_title_quality(title: str) -> dict:
        """
        Rate a title's quality based on various metrics
        """
        # TODO: Implement comprehensive rating algorithm
        length = len(title)
        word_count = len(title.split())

        # Scoring logic
        length_score = 0.9 if 30 <= length <= 100 else 0.7
        word_score = 0.9 if 3 <= word_count <= 12 else 0.7
        clarity_score = 0.85  # TODO: Use AI to assess clarity

        overall_score = (length_score + word_score + clarity_score) / 3

        return {
            "title": title,
            "overall_score": overall_score,
            "metrics": {
                "character_count": length,
                "word_count": word_count,
                "length_score": length_score,
                "word_score": word_score,
                "clarity_score": clarity_score,
            },
            "recommendations": [
                "Consider adding power words like 'Ultimate', 'Complete', 'Master'" if clarity_score < 0.8 else "Great title clarity!",
            ]
        }
