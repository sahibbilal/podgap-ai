"""Run FastAPI with uvicorn. From backend dir: python run.py  OR  python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
