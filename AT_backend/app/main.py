import asyncio
import time

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db import Base, engine, get_db
from app.routers import api_router as api

from app.serve.KafkaContainer import ProducerContainer, ConsumerContainer, ConnectionManager
import app.result.service as result_service



def create_app():
    app = FastAPI()

    producer = ProducerContainer().producer()
    consumer = ConsumerContainer().consumer()
    connection_manager = ConnectionManager()

    @app.on_event("startup")
    async def startup():
        Base.metadata.create_all(bind=engine)
        await producer.start()
        await consumer.start()

        async def receive_and_send():
            db = next(get_db())
            async for msg in consumer:
                data = msg.value
                result = result_service.create_by_dict(db_session=db, result_in=data)
                await connection_manager.broadcast({
                    "topic": "PREDICT_RESULT",
                    "id": result.id,
                    "start_timestamp": result.start_timestamp,
                    "end_timestamp": result.end_timestamp,
                })

        asyncio.create_task(receive_and_send())

    @app.on_event("shutdown")
    async def shutdown_event():
        await producer.stop()
        await consumer.stop()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOW_ORIGIN,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api)

    @app.websocket("/ws/{client_id}")
    async def websocket_endpoint(websocket: WebSocket, client_id: int):
        await connection_manager.connect(client_id, websocket)
        count = 0
        start_time = time.monotonic()

        try:
            while True:
                data = await websocket.receive_json()
                await connection_manager.broadcast(data)

                count += 1
                if count % 5 == 0:
                    elapsed_time = time.monotonic() - start_time
                    print(f"Throughput: {count / elapsed_time:.2f} /sec")
                    start_time = time.monotonic()
                    count = 0
                if data.get("topic") == "DETECTED":
                    await producer.send_and_wait("predict_input", value=data)

        except WebSocketDisconnect:
            connection_manager.disconnect(client_id)

    return app
