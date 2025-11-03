import time
from fastapi import FastAPI, Request, HTTPException, status

# ===============================
# Rate Limiting Configuration
# ===============================

MAX_CALLS = 5          # Max requests allowed
TIME_FRAME = 60        # Time window in seconds
# The rate_limit_store dictionary initializes once per server process, not per request, so
# timestamps persist across requests. But if server is reloaded then it gets reintialized.
rate_limit_store = {}  # {client_ip: [timestamps]}


def register_rate_limit_middleware(app):
    """
    Middleware-based IP-specific rate limiter.
    Keeps timestamps for each client's requests.
    """

    @app.middleware("http")
    async def rate_limit_middleware(request: Request, call_next):
        client_ip = request.client.host
        now = time.time()

        # Get list of previous calls for this IP, or initialize
        calls = rate_limit_store.get(client_ip, [])

        # Keep only timestamps within the last TIME_FRAME seconds
        recent_calls = [ts for ts in calls if ts >= now - TIME_FRAME]

        # Update store
        rate_limit_store[client_ip] = recent_calls

        # Check if client exceeded limit
        if len(recent_calls) >= MAX_CALLS:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Try again later.",
            )

        # Record this call
        rate_limit_store[client_ip].append(now)

        if(len(rate_limit_store[client_ip])>MAX_CALLS):
            del rate_limit_store[client_ip][:-MAX_CALLS]

        # Proceed to next middleware or route handler
        response = await call_next(request)
        return response
