from fastapi import  APIRouter
from Models.models import Session
from controllers.sessions import getSessions, createSessions
from datetime import datetime

router = APIRouter()

@router.post('/getSessions', tags=["Session"])
def get_Sessions(search: str = ""):
    session = getSessions(search)
    return session

@router.post('/createSessions', tags=["Session"])
def create_Sessions(session: Session):
    session = createSessions(session)
    return session
