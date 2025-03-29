from fastapi import FastAPI, HTTPException
from routes.user import user
from routes.auth import auth
from datetime import datetime, timedelta
import logging
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth.auth import get_password_hash
from config.db import conn

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
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

app.include_router(user)
app.include_router(auth)

@app.get("/")
def read_root():
    return {"Hello":"World"}

@app.get("/health")
def health_check():
    return {"status":"ok"}

@app.on_event("startup")
async def startup_event():
    try:
        # Create admin user if it doesn't exist
        admin_user = {
            "name": "Admin",
            "email": "admin@example.com",
            "hashed_password": get_password_hash("adminpassword"),
            "role": "admin",
            "disabled": False
        }
        
        # Check if admin user exists
        existing_admin = conn.local.user.find_one({"email": "admin@example.com"})
        if not existing_admin:
            conn.local.user.insert_one(admin_user)
            logger.info("Admin user created successfully")
        else:
            logger.info("Admin user already exists")
    except Exception as e:
        logger.error(f"Error creating admin user: {str(e)}")
        raise