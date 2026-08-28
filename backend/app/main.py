from fastapi import FastAPI

app = FastAPI(
    title="SkyGuard AI",
    description="AI/ML-based Intelligent Anomaly Detection System for Automatic Weather Stations",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "project": "SkyGuard AI",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }