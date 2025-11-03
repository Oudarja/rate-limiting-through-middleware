'''
This approach involves creating a class that inherits from starlette.middleware.base.BaseHTTPMiddleware 
and implementing an async dispatch method. The dispatch method receives the request object and a call_next 
function. This method provides a more structured way to define middleware, especially when dealing with complex
logic or requiring attributes to be initialized with the middleware. It is added to the FastAPI application using
app.add_middleware()
'''


