import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from scraper import load_cars, run_scraper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Парсим при старте если данных нет
    cars = load_cars()
    if not cars:
        asyncio.create_task(run_scraper())
    yield


app = FastAPI(title="Encar Catalog API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/cars")
def get_cars():
    return load_cars()


@app.post("/api/parse")
async def trigger_parse(background_tasks: BackgroundTasks):
    background_tasks.add_task(asyncio.run, run_scraper())
    return {"status": "parsing started"}
