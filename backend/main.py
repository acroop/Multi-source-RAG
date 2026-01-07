from fastapi import FastAPI
from api.ingest import router as ingest_router
from api.ask import router as ask_router
import config

app = FastAPI()
app.include_router(ingest_router)
app.include_router(ask_router)