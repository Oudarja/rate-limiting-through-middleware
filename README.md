# rate-limiting-through-middleware

# Overview

This project demonstrates IP-based rate limiting in FastAPI using both:
 - Function-based middleware
 - Class-based middleware

The middleware tracks requests per client IP and enforces a limit of requests per time window to prevent abuse.

# Installation and set up
```
1. Clone the repository
git clone https://github.com/Oudarja/rate-limiting-through-middleware.git

# 2. Python version 3.9.13
 
# 3. Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate      # For Windows

# 4. Install dependencies
pip install -r requirements.txt
```

# Run the Application
```
uvicorn main:app --reload --port 8000
uvicorn main:app --reload --port 8001

Server will start at:

http://127.0.0.1:8000
http://127.0.0.1:8001
```

** Then for check just reload frequently **
