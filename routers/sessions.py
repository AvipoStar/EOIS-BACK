from fastapi import APIRouter
from Models.models import Session, CreateSession
from controllers.sessions import getSessions, createSessions, editSessions
from datetime import datetime

router = APIRouter()


@router.post('/getSessions', tags=["Session"])
def get_Sessions(search: str = ""):
    session = getSessions(search)
    return session


@router.post('/createSessions', tags=["Session"])
def create_Sessions(session: CreateSession):
    session = createSessions(session)
    return session


@router.patch('/editSessions', tags=["Session"])
def edit_Sessions(session: Session):
    session = editSessions(session)
    return session
