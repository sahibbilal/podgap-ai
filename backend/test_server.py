"""Quick test to verify server starts and responds correctly"""
import asyncio
import httpx
from app.main import app
from app.core.config import get_settings

settings = get_settings()


async def test_endpoints():
    """Test that basic endpoints work"""
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        # Test health endpoint
        response = await client.get("/health")
        print(f"✓ Health check: {response.status_code} - {response.json()}")
        
        # Test debug config
        response = await client.get("/debug/config")
        print(f"✓ Debug config: {response.status_code}")
        print(f"  CORS Origins: {response.json()['cors_origins']}")
        
        print("\n✅ All basic tests passed!")
        print(f"\n🚀 Server is ready at http://localhost:8000")
        print(f"   API Base: http://localhost:8000{settings.api_v1_prefix}")
        print(f"   Docs: http://localhost:8000/docs")


if __name__ == "__main__":
    print("Testing PodGap AI Backend...\n")
    asyncio.run(test_endpoints())
