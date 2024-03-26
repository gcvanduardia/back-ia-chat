from fastapi import APIRouter
from controllers.test import read_root, create_message, error_example

test = APIRouter()

test.get("/test/")(read_root)
test.post("/test/message/")(create_message)
test.get("/test/error/")(error_example)