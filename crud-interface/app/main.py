from fastapi import FastAPI, HTTPException
from routes.user import user
from datetime import datetime, timedelta
import logging
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


# Initialize FastAPI app
app = FastAPI(
    title="FastAPI MongoDB Application",
    description="A RESTful API with MongoDB, authentication, and webhook functionality",
    version="1.0.0",)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Authentication utilities
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(user)

@app.get("/")
def read_root():
    return {"Hello":"World"}

@app.get("/health")
def health_check():
    return {"status":"ok"}