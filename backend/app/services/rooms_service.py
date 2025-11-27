from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from app.models import Room
from datetime import datetime

async def create_room(db: AsyncSession) -> Room:
    room = Room()
    db.add(room)
    await db.commit()
    await db.refresh(room)
    return room

async def get_room(db: AsyncSession, room_id: UUID) -> Room | None:
    statement = select(Room).where(Room.id == room_id)
    res = await db.exec(statement)
    return res.one_or_none()

async def update_room_code(db: AsyncSession, room_id: UUID, code: str):
    room = await get_room(db, room_id)
    if not room:
        return None
    room.code = code
    room.updated_at = datetime.utcnow()
    db.add(room)
    await db.commit()
    await db.refresh(room)
    return room
