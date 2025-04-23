import os
import asyncio
import httpx
from fastapi import FastAPI

app = FastAPI()
TARGET_URL = os.getenv("TARGET_URL", "http://localhost:5003/health")

async def ping_forever():
    print(f"Scheduler started. Target URL: {TARGET_URL}")
    async with httpx.AsyncClient() as client:
        while True:
            try:
                response = await client.get(TARGET_URL)
                print(f"Response: {response.status_code} - {response.text}")
            except Exception as e:
                print(f"Failed to reach target: {e}")
            await asyncio.sleep(10)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(ping_forever())