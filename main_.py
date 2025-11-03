from fastapi import FastAPI , Request
import random
import string
# from FunctionBasedMiddleware import register_rate_limit_middleware
from ClassBasedModlleware import RateLimiterMiddleware

app=FastAPI()


# register_rate_limit_middleware(app)

app.add_middleware(RateLimiterMiddleware)

@app.get("/")
async def read_root():
    return {"message": "Welcome! You’re within the rate limit. I am from main_"}


@app.get("/status")
async def check_status():
    return {"status": "Server is running"}


