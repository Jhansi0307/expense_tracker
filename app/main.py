from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.router import api_router


app = FastAPI(title=settings.PROJECT_NAME)

# CORS (adjust allowed origins later as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include versioned API
app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["Health"])
def read_root():
    return {"message": "Expense Tracker API is running"}
