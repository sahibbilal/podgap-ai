"""
Services package for PodGap AI
Includes:
- TrendService: Multi-source trend aggregation
- GapAnalyzer: Podcast niche analysis
- TitleGenerator: AI-powered title generation
"""

from .trend_service import TrendService
from .gap_analyzer import GapAnalyzer
from .title_generator import TitleGenerator

__all__ = ["TrendService", "GapAnalyzer", "TitleGenerator"]
