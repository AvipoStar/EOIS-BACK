from typing import List

from fastapi import APIRouter

from Models.models import GetFirm
from controllers.firms import getFirmsOnCurrentSession, getStudentsOnCurrentSession, getFirmsOnSession

router = APIRouter()


@router.get('/getFirmsOnCurrentSession', tags=["Firms"])
def getFirms():
    firms = getFirmsOnCurrentSession()
    return firms


@router.get('/getStudentsOnCurrentSession', tags=["Firms"])
def getStudents():
    firms = getStudentsOnCurrentSession()
    return firms


@router.post('/getFirmsOnSession', tags=["Firms"])
def getStudents(sessionId: GetFirm):
    try:
        firms = getFirmsOnSession(sessionId.sessionId)
        return firms
    except:
        return []
