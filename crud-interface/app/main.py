from fastapi import FastAPI, HTTPException, Request, Depends
from routes.user import user
from routes.auth import auth
from routes.webhook import webhook
from datetime import datetime, timedelta
from utils.logger import logger
from utils.rate_limiter import rate_limiter
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth.auth import get_password_hash
from config.db import conn
from fastapi.responses import JSONResponse
from typing import Any
import json

# Initialize FastAPI app
app = FastAPI(
    title="FastAPI MongoDB Application",
    description="A RESTful API with MongoDB, authentication, and webhook functionality",
    version="1.0.1",
)

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

# Include routers
app.include_router(user)
app.include_router(auth)
app.include_router(webhook)

# Middleware for rate limiting and logging
@app.middleware("http")
async def add_middleware(request: Request, call_next):
    # Rate limiting
    try:
        await rate_limiter.check_rate_limit(request)
    except HTTPException as e:
        logger.error(f"Rate limit exceeded for {request.client.host}")
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.detail}
        )
    
    # Log request
    logger.info(
        f"Request received",
        extra={
            "method": request.method,
            "url": str(request.url),
            "client_ip": request.client.host,
            "user_agent": request.headers.get("user-agent")
        }
    )
    
    # Process request
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        raise

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
        logger.error(f"Error creating admin user: {str(e)}", exc_info=True)
        raise