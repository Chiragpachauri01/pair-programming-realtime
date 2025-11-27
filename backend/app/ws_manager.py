from fastapi import WebSocket
from typing import Dict, List
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.room_state: Dict[str, str] = {}
        self.locks: Dict[str, asyncio.Lock] = {}

    async def connect(self, room_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(room_id, []).append(websocket)
        self.locks.setdefault(room_id, asyncio.Lock())

    def disconnect(self, room_id: str, websocket: WebSocket):
        conns = self.active_connections.get(room_id, [])
        if websocket in conns:
            conns.remove(websocket)

    async def broadcast_to_room(self, room_id: str, message: dict):
        for conn in list(self.active_connections.get(room_id, [])):
            try:
                await conn.send_json(message)
            except:
                pass

    def get_state(self, room_id: str) -> str:
        return self.room_state.get(room_id, "")

    def set_state(self, room_id: str, code: str):
        self.room_state[room_id] = code

manager = ConnectionManager()
