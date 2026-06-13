"""
Pulse - Database Connection

Handles SQLite connection, table creation, and query execution.
"""

import aiosqlite

from config import settings
from db.models import SCHEMA


async def init_db():
    """Create all tables if they don't exist."""
    async with aiosqlite.connect(settings.DATABASE_PATH) as db:
        await db.executescript(SCHEMA)
        await db.commit()
        print(f"📦 Database ready at {settings.DATABASE_PATH}")


async def get_db():
    """Get a database connection."""
    db = await aiosqlite.connect(settings.DATABASE_PATH)
    db.row_factory = aiosqlite.Row
    try:
        yield db
    finally:
        await db.close()


async def execute_query(query: str, params: tuple = ()):
    """Execute a write query (INSERT, UPDATE, DELETE)."""
    async with aiosqlite.connect(settings.DATABASE_PATH) as db:
        await db.execute(query, params)
        await db.commit()


async def fetch_all(query: str, params: tuple = ()):
    """Execute a read query and return all rows as dictionaries."""
    async with aiosqlite.connect(settings.DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(query, params)
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


async def fetch_one(query: str, params: tuple = ()):
    """Execute a read query and return a single row as dictionary."""
    async with aiosqlite.connect(settings.DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(query, params)
        row = await cursor.fetchone()
        return dict(row) if row else None