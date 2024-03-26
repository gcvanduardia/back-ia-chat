from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.test import test
from routes.chat import chat

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(test)
app.include_router(chat, prefix="/v1", tags=["v1"])