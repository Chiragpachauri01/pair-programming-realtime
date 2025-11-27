from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db import async_session
from app.services.rooms_service import create_room, get_room
from pydantic import BaseModel

router = APIRouter(prefix="/rooms", tags=["rooms"])

class RoomOut(BaseModel):
    roomId: UUID

async def get_db():
    async with async_session() as session:
        yield session

@router.post("/", response_model=RoomOut)
async def post_room(db: AsyncSession = Depends(get_db)):
    room = await create_room(db)
    return {"roomId": room.id}

@router.get("/{room_id}")
async def get_room_endpoint(room_id: UUID, db: AsyncSession = Depends(get_db)):
    room = await get_room(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return {"roomId": room.id, "code": room.code, "language": room.language}
