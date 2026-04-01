# PodGap AI - API Integration Guide

## Implemented Features ✅
- Professional dashboard UI with multiple options
- Source links for all data points
- Multi-tab navigation (Overview, Trends, Gap Analysis, Titles)
- Service layer architecture for extensibility

## Integration Roadmap 🚀

### 1. **Google Trends API** 
- **File**: `backend/app/services/trend_service.py`
- **Method**: `get_google_trends()`
- **Status**: Placeholder
- **Integration Steps**:
  ```bash
  pip install pytrends
  ```
- **Setup**:
  ```python
  from pytrends.request import TrendReq
  
  async def get_google_trends(keywords: list[str], period: str = "3m"):
      pytrends = TrendReq(hl='en-US', tz=360)
      pytrends.build(timeframe=period)
      return pytrends.interest_over_time()
  ```

### 2. **Reddit API (PRAW)**
- **File**: `backend/app/services/trend_service.py`  
- **Method**: `get_reddit_trends()`
- **Status**: Already in requirements.txt
- **Setup**:
  ```python
  import praw
  
  reddit = praw.Reddit(
      client_id='YOUR_CLIENT_ID',
      client_secret='YOUR_CLIENT_SECRET',
      user_agent='PodGapAI/1.0'
  )
  ```
- **Add to .env**:
  ```
  REDDIT_CLIENT_ID=your_id
  REDDIT_CLIENT_SECRET=your_secret
  ```

### 3. **YouTube Data API**
- **File**: `backend/app/services/trend_service.py`
- **Method**: `get_youtube_trends()`
- **Status**: Placeholder
- **Integration Steps**:
  1. Create project at [Google Cloud Console](https://console.cloud.google.com/)
  2. Enable YouTube Data API v3
  3. Create API key
  ```bash
  pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
  ```
- **Setup**:
  ```python
  from googleapiclient.discovery import build
  
  youtube = build('youtube', 'v3', developerKey='YOUR_API_KEY')
  ```
- **Add to .env**:
  ```
  YOUTUBE_API_KEY=your_key
  ```

### 4. **Facebook/Meta API**
- **File**: `backend/app/services/trend_service.py`
- **Method**: `get_facebook_trends()`
- **Status**: Placeholder
- **Integration Steps**:
  1. Create app at [Meta Developers](https://developers.facebook.com/)
  2. Get access token
  ```bash
  pip install facebook-sdk
  ```
- **Setup**:
  ```python
  import facebook
  
  graph = facebook.GraphAPI(access_token='YOUR_TOKEN')
  ```
- **Add to .env**:
  ```
  FACEBOOK_ACCESS_TOKEN=your_token
  ```

### 5. **Twitter/X API v2**
- **File**: `backend/app/services/trend_service.py`
- **Method**: `get_twitter_trends()`
- **Status**: Placeholder
- **Integration Steps**:
  1. Create app at [Twitter Developer Portal](https://developer.twitter.com/)
  2. Get bearer token
  ```bash
  pip install tweepy
  ```
- **Setup**:
  ```python
  import tweepy
  
  client = tweepy.Client(bearer_token='YOUR_BEARER_TOKEN')
  ```
- **Add to .env**:
  ```
  TWITTER_BEARER_TOKEN=your_token
  ```

### 6. **Listen Notes API**
- **File**: `backend/app/services/gap_analyzer.py`
- **Method**: `analyze_niche()`
- **Status**: In requirements (partially)
- **Setup**:
  ```bash
  pip install listennotes
  ```
- **Add to .env**:
  ```
  LISTEN_NOTES_API_KEY=your_key  # Already in requirements
  ```

### 7. **Ollama Integration**
- **File**: `backend/app/services/title_generator.py`
- **Method**: `generate_titles()`
- **Status**: Placeholder
- **Setup**:
  ```bash
  pip install ollama
  ```
- **Running Ollama**:
  ```bash
  ollama pull llama3.2
  ollama serve
  ```
- **Usage**:
  ```python
  from ollama import Client
  
  client = Client(host='http://localhost:11434')
  response = client.generate(
      model='llama3.2',
      prompt='Generate 5 podcast titles about: ...'
  )
  ```

## Quick Setup for Multi-Source Trends

```bash
# Install all API clients
pip install pytrends praw google-auth-oauthlib google-api-python-client facebook-sdk tweepy

# Configure .env
REDDIT_CLIENT_ID=your_id
REDDIT_CLIENT_SECRET=your_secret
YOUTUBE_API_KEY=your_key
FACEBOOK_ACCESS_TOKEN=your_token
TWITTER_BEARER_TOKEN=your_token
LISTEN_NOTES_API_KEY=your_key
```

## Testing the Integrations

```bash
# Test backend
cd backend
python -m pytest tests/test_services.py

# Test API endpoints
curl -X GET http://localhost:8000/api/v1/trends?period=3m&source=all
curl -X POST http://localhost:8000/api/v1/niche-gap -d '{"niche":"AI Podcasts"}'
```

## Frontend Usage

The updated dashboard automatically displays:
- ✅ Source links for all data points
- ✅ Professional card-based UI
- ✅ Multi-tab navigation
- ✅ Real-time data fetching with loading states
- ✅ Copy-to-clipboard for titles
- ✅ Color-coded saturation levels
- ✅ Source attribution with icons

## Architecture

```
PodGap AI Backend
├── API Routes (app/api/)
│   ├── trends.py (Multi-source trends)
│   ├── niche_gap.py (Gap analysis)
│   ├── titles.py (Title generation)
│   └── ...
├── Services (app/services/)
│   ├── trend_service.py (Google, Reddit, YouTube, Facebook, Twitter/X)
│   ├── gap_analyzer.py (Listen Notes integration)
│   └── title_generator.py (Ollama integration)
├── Models (app/models/)
└── Database (app/db/)
```

## Next Steps

1. **Implement real API integrations** - Start with Google Trends + Reddit
2. **Add API key validation** - Ensure all keys are set before use
3. **Implement caching** - Cache trends to reduce API calls
4. **Add error handling** - Graceful fallbacks when APIs fail
5. **Monitor rate limits** - Respect API quotas
6. **Add data deduplication** - Merge similar trends from multiple sources
7. **Implement result ranking** - Score trends by relevance & interest

## Support & Resources

- [pytrends Docs](https://pypi.org/project/pytrends/)
- [PRAW Docs](https://praw.readthedocs.io/)
- [YouTube API](https://developers.google.com/youtube/v3)
- [Meta API](https://developers.facebook.com/docs/)
- [Twitter API v2](https://developer.twitter.com/en/docs/twitter-api)
- [Ollama](https://ollama.ai/)
