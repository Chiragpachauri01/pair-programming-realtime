from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.routers import rooms, autocomplete
from app.db import init_db, async_session
from app.ws_manager import manager
from app.services.rooms_service import get_room, update_room_code
from uuid import UUID
import json
import asyncio

app = FastAPI(title="PairProg Prototype")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rooms.router)
app.include_router(autocomplete.router)

@app.on_event("startup")
async def startup():
    await init_db()

@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await manager.connect(room_id, websocket)
    try:
        await websocket.send_json({"type": "init", "code": manager.get_state(room_id)})
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            if payload.get("type") == "update":
                code = payload.get("code", "")
                manager.set_state(room_id, code)
                await manager.broadcast_to_room(room_id, {"type": "update", "code": code})
    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)
    finally:
        if not manager.active_connections.get(room_id):
            code_final = manager.get_state(room_id)
            async def save():
                async with async_session() as session:
                    room = await get_room(session, UUID(room_id))
                    if room:
                        await update_room_code(session, UUID(room_id), code_final)
            asyncio.create_task(save())
