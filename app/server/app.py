from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from server.routes.route import router as DocRouter

app = FastAPI()

# Allow all origins, allow all methods, allow all headers
origins = ["*"]

# Apply CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware to log every request
class RequestLoggerMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        request = Request(scope, receive)
        print(f"Received request: {request.method} {request.url}")
        response = await self.app(scope, receive, send)
        return response

# Add the custom middleware to the app
app.add_middleware(RequestLoggerMiddleware)

app.include_router(DocRouter, tags=["Doc"], prefix="/getdoc")

@app.get('/', tags=['Root'])
async def read_root():
    msg = {
        "message":"Server is Working! "
    }
    data = jsonable_encoder(msg)
    return data