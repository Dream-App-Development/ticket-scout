import logging
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from mangum import Mangum
from app.api.api_v1.endpoints import ticket, test

logging.basicConfig(level=logging.INFO)
load_dotenv()

app = FastAPI()
app.include_router(ticket.router)
app.include_router(test.router)

lambda_handler = Mangum(app)
# https://px82x2qsic.execute-api.ap-southeast-1.amazonaws.com/staging/

# Enable Middleware
app.add_middleware(GZipMiddleware, minimum_size=500)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    pass


@app.on_event("shutdown")
async def shutdown_event():
    pass


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
