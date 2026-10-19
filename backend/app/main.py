
import os
import secrets

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router

load_dotenv()

API_KEY = os.getenv("ATLAS_API_KEY")
if not API_KEY:
    raise RuntimeError("ATLAS_API_KEY is missing from backend/.env")


def verify_api_key(x_api_key: str = Header(default="")):
    if not secrets.compare_digest(x_api_key, API_KEY):
        raise HTTPException(status_code=401, detail="Invalid or missing API key")


app = FastAPI(
    title="Project Atlas API",
    description="Generative AI and Agentic AI System",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5501",
        "http://localhost:5501",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Protect all business endpoints in this router.
app.include_router(router, dependencies=[Depends(verify_api_key)])


@app.get("/health")
def health_check():
    return {"status": "healthy", "project": "Project Atlas"}


@app.get("/")
def home():
    return {"message": "Project Atlas API is running"}
