from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from routes import auth, movies, recommendations
from recommender.content_based import ContentBasedRecommender
from recommender.collaborative import CollaborativeRecommender
from recommender.hybrid import HybridRecommender

load_dotenv()

# Global recommender instances (loaded once at startup)
content_rec = ContentBasedRecommender()
collab_rec = CollaborativeRecommender()
hybrid_rec = HybridRecommender(content_rec, collab_rec)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: connect DB and load models
    app.state.mongo = AsyncIOMotorClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
    app.state.db = app.state.mongo["recommendation_engine"]
    print("MongoDB connected")

    # Load pre-trained recommendation models
    content_rec.load()
    collab_rec.load()
    print("Recommendation models loaded")

    yield

    # Shutdown: close DB connection
    app.state.mongo.close()
    print("MongoDB disconnected")

app = FastAPI(
    title="Movie Recommendation Engine API",
    description="Content-Based + Collaborative Filtering recommender system",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", os.getenv("FRONTEND_URL", "*")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(movies.router, prefix="/movies", tags=["Movies"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["Recommendations"])

@app.get("/", tags=["Health"])
async def root():
    return {"message": "Movie Recommendation Engine API", "status": "running", "docs": "/docs"}
