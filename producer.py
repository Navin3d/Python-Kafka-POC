import json

from contextlib import asynccontextmanager

from pydantic import TypeAdapter

from models import User

from confluent_kafka import Producer
from fastapi import FastAPI, Request
from uvicorn import run
from pathlib import Path


@asynccontextmanager
async def lifespan(app: FastAPI):
    path = Path(__file__).parent / "data.json"
    if path.exists():
        app.state.data: list[User] = TypeAdapter(list[User]).validate_python(json.loads(path.read_text(encoding="utf-8"))["users"])
        print(f"[INFO] loaded {len(app.state.data)} users.")
    else:
        print(f"[WARN] data.json missing in path {path}")
        app.state.data = []
    yield


app = FastAPI(lifespan=lifespan)

config = {
    "bootstrap.servers": "localhost:9092",
    "client.id": "navin.test.producer"
}
producer = Producer(config)
TOPIC = "navin_check"


@app.get("/health")
def health_check():
    return {
        "status": "UP",
    }


@app.get("/publish_users")
async def publish_kafka(request: Request, page_no: int = 1, page_size: int = 10):
    start = (page_no - 1) * page_size
    end = start + page_size
    datas: list[User] = request.app.state.data[start:end]

    for data in datas:
        producer.produce(TOPIC, data.model_dump_json(), str(data.id))

    # producer.flush(0)

    return {
        "status": "OK",
        "count": len(datas),
        "data": datas
    }


if __name__ == "__main__":
    run("producer:app", reload=True)
