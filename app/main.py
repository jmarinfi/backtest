from fastapi import FastAPI

from app.api.endpoints import backtest


app = FastAPI()

app.include_router(backtest.router)


@app.get("/")
async def read_root():
    return {"Hello": "World"}
