from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
import os

DATA_PATH = os.environ.get('DATA_PATH', './.cache')
subscription_file_path = os.path.join(DATA_PATH, 'sub.txt')

app = FastAPI()

@app.get("/sub", response_class=PlainTextResponse)
async def sub():
    if os.path.exists(subscription_file_path):
        with open(subscription_file_path, 'r') as f:
            return f.read()
    return "Subscription not available."
