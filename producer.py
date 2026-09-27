import json

from contextlib import asynccontextmanager

from pydantic import TypeAdapter

from models import User

from confluent_kafka import Producer
from fastapi import FastAPI, Request
from uvicorn import run
from pathlib import Path


config = {
    "bootstrap.servers": "localhost:9092",
    "client.id": "navin.test.producer"
}
producer = Producer(config)


@asynccontextmanager
async def lifespan(app: FastAPI):
    path = Path(__file__).parent / "data.json"
    if path.exists():
        app.state.data: list[User] = TypeAdapter(list[User]).validate_python(
            json.loads(path.read_text(encoding="utf-8"))["users"])
        print(f"[INFO] loaded {len(app.state.data)} users.")
    else:
        print(f"[WARN] data.json missing in path {path}")
        app.state.data = []
    yield
    producer.flush()

app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health_check():
    return {
        "status": "UP",
    }


@app.get("/basic_publish_users")
async def basic_publish_kafka(request: Request, page_no: int = 1, page_size: int = 10):
    start = (page_no - 1) * page_size
    end = start + page_size
    datas: list[User] = request.app.state.data[start:end]

    TOPIC = "navin_basic_check"

    for data in datas:
        producer.produce(TOPIC, data.model_dump_json().encode("utf-8"), str(data.id).encode("utf-8"))

    return {
        "status": "OK",
        "count": len(datas),
        "data": datas
    }


@app.get("/protobuf_publish_users")
async def protobuf_publish_kafka(request: Request, page_no: int = 1, page_size: int = 10):
    start = (page_no - 1) * page_size
    end = start + page_size
    datas: list[User] = request.app.state.data[start:end]

    TOPIC = "navin_protobuf_check"

    for data in datas:
        producer.produce(TOPIC, data.model_dump_json().encode("utf-8"), str(data.id).encode("utf-8"))

    return {
        "status": "OK",
        "count": len(datas),
        "data": datas
    }

if __name__ == "__main__":
    run("producer:app", reload=True)
