from fastapi import FastAPI , Request
import random
import string
from FunctionBasedMiddleware import register_rate_limit_middleware
app=FastAPI()


register_rate_limit_middleware(app)

@app.get("/")
async def read_root():
    return {"message": "Welcome! You’re within the rate limit."}


@app.get("/status")
async def check_status():
    return {"status": "Server is running"}





