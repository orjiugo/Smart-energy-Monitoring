"""Dependency injection for API routes"""
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import get_db

async def get_current_user_or_none():
    return None

def get_db_dependency():
    return Depends(get_db)