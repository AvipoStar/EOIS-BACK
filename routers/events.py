from typing import Dict

from fastapi import APIRouter
from Models.models import Event, UserId
from controllers.events import getEventTypes, getEventsForUser, createEvent


router = APIRouter()

@router.get('/getEventTypes', tags=["Event"])
def get_Event_Types():
    eventTypes = getEventTypes()
    return eventTypes

@router.post('/getEventsForUser', tags=["Event"])
def get_Events_For_User(userId: UserId):
    events = getEventsForUser(userId.userId)
    return events

@router.post('/createEvent', tags=["Event"])
def create_Event(event: Event):
    eventId = createEvent(event)
    return eventId