from pydantic import BaseModel
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime

class Message(BaseModel):
    message: str

def read_root():
    return {"Hello": "World"}

def create_message(message: Message):
    current_date = datetime.now().date()
    body = {
        "message": message.message,
        "date": str(current_date)
    }
    return JSONResponse(status_code=200, content=body, headers={"X-Header": "There goes my header"})

def error_example():
    current_date = datetime.now().date()
    body = {
        "message": "This is an error message",
        "code": "error_code_1",
        "date": str(current_date)
    }
    raise HTTPException(status_code=400, detail=body, headers={"X-Error": "There goes my error"})