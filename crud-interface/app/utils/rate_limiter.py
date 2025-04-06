from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from typing import Dict, Optional
import time

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = {}
    
    async def check_rate_limit(self, request: Request) -> None:
        client_ip = request.client.host
        current_time = time.time()
        
        # Clean up old requests
        if client_ip in self.requests:
            self.requests[client_ip] = [
                t for t in self.requests[client_ip]
                if current_time - t < 60
            ]
        
        # Initialize if not exists
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        
        # Check rate limit
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later."
            )
        
        # Add current request
        self.requests[client_ip].append(current_time)

# Create a default rate limiter instance
rate_limiter = RateLimiter(requests_per_minute=60) 