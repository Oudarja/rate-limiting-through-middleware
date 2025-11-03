'''
This approach involves creating a class that inherits from starlette.middleware.base.BaseHTTPMiddleware 
and implementing an async dispatch method. The dispatch method receives the request object and a call_next 
function. This method provides a more structured way to define middleware, especially when dealing with complex
logic or requiring attributes to be initialized with the middleware. It is added to the FastAPI application using
app.add_middleware()
'''


import time
from fastapi import FastAPI, Request, HTTPException, status
# BaseHTTPMiddleware →a Starlette class inherited from to create class-based middleware 
# in FastAPI.
from starlette.middleware.base import BaseHTTPMiddleware

MAX_CALLS = 5       # Max requests allowed
TIME_FRAME = 60     # Time window in seconds


class RateLimiterMiddleware(BaseHTTPMiddleware):
    # __init__ → called when the middleware is added to the app.
    def __init__(self,app):
        # initializes the base middleware with the FastAPI app instance.
        super().__init__(app)
        # {client_ip: [timestamps]}
        self.rate_limit_store = {}

    async def dispatch(self,request:Request,call_next):

        client_ip=request.client.host

        now=time.time()

        # Get list of previous calls for this IP, or initialize
        calls = self.rate_limit_store.get(client_ip, [])

        # Keep only timestamps within the last TIME_FRAME seconds
        recent_calls = [ts for ts in calls if ts >= now - TIME_FRAME]

        # Update store
        self.rate_limit_store[client_ip] = recent_calls

        # Check if client exceeded limit
        if len(recent_calls) >= MAX_CALLS:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Try again later.",
            )

        # Record this call
        self.rate_limit_store[client_ip].append(now)

        if(len(self.rate_limit_store[client_ip])>MAX_CALLS):
            del self.rate_limit_store[client_ip][:-MAX_CALLS]

        # Proceed to next middleware or route handler
        response = await call_next(request)
        return response















