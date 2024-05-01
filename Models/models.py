from typing import List

from pydantic import BaseModel
from datetime import datetime, date
from fastapi import UploadFile, File


class Project(BaseModel):
    id: int = None
    nameProject: str
    descriptionProject: str
    direction: int

class CreateProject(BaseModel):
    nameProject: str
    descriptionProject: str
    direction: int


class ProjectDirectionId(BaseModel):
    directionIds: List[int] = None
    search: str


class Profile(BaseModel):
    id: int = None
    nameProfile: str


class ProjectDirection(BaseModel):
    id: int = None
    name: str


class Role(BaseModel):
    id: int = None
    nameRole: str


class EventType(BaseModel):
    id: int = None
    nameEventType: str


class Event(BaseModel):
    id: int = None
    eventTypeId: int = None
    targetUserId: int = None
    initiatorId: int = None
    datetimeEvent: datetime = None
    amount: int = 0
    description: str = ''


class UserEvent(BaseModel):
    userId: int = None
    initiator: str = ''
    datetimeEvent: datetime = None
    currentBalance: int = 0
    description: str = ''
    amount: int


class Firm(BaseModel):
    id: int = None
    number: int = None
    sessionId: int = None
    balance: int = 0


class GetFirm(BaseModel):
    sessionId: int = None


class Session(BaseModel):
    id: int = None
    dateStart: date = None
    dateEnd: date = None
    place: str = None
    firmCount: int = None


class User(BaseModel):
    id: int = None
    name: str = None
    surname: str = None
    patronymic: str = None
    bornDate: date = None
    roleId: int = None
    balance: int = None
    gender: int = None
    profileId: int = None
    studentIsAttachedToFirm: bool = False
    photoPath: str = None
    login: str = ""
    password: str = ""


class Student(BaseModel):
    id: int
    name: str
    surname: str
    patronymic: str
    bornDate: date = None
    gender: int
    profile: str
    project: str
    balance: int
    firm: int
    photoPath: str


class Curator(BaseModel):
    id: int
    name: str
    surname: str
    patronymic: str
    bornDate: date = None
    gender: int
    profile: int
    photoPath: str


class UserId(BaseModel):
    userId: int


class FirmIds(BaseModel):
    firmIds: List[int]


class ProfileId(BaseModel):
    profileIds: List[int]
    search: str


class JoinTheCompanyClass(BaseModel):
    userId: int
    firmId: int
    profileId: int
    projectIds: List[int]


class LoginClass(BaseModel):
    login: str
    password: str


class Token(BaseModel):
    token: str


class RegistrationClass(BaseModel):
    name: str = None
    surname: str = None
    patronymic: str = None
    bornDate: datetime
    gender: int
    login: str
    password: str


class changeLoginPasswordClass(BaseModel):
    id: int
    newLogin: str
    newPassword: str
    photoPath: str


class timetable(BaseModel):
    date: datetime = None
    file: UploadFile = File(...)


class Board(BaseModel):
    id: int
    name: str
    description: str
    coverColor: str

class BoardId(BaseModel):
    boardId: int

class FirmId(BaseModel):
    firmId: int

class CreateBoard(BaseModel):
    name: str
    description: str
    firmId: int
    coverColor: str


class BoardList(BaseModel):
    id: int
    name: str
    idBoard: int
    serialNumber: int


class CreateBoardList(BaseModel):
    name: str
    idBoard: int
    serialNumber: int

class Task(BaseModel):
    id: int
    name: str
    description: str
    idList: int
    serialNumber: int
    creationDateTime: datetime
    status: int
    deadline: datetime
    isDone: bool


class TaskPriority(BaseModel):
    id: int
    name: str
    color: str


class TaskAttachment(BaseModel):
    id: int
    idTask: int
    path: str


class Executors(BaseModel):
    id: int
    idUser: int
    idTask: int


class Route(BaseModel):
    id: int
    path: str
    name: str

class MoveTask(BaseModel):
    taskId: int
    newListId: int
    newSerialNumber: int

class MoveList(BaseModel):
    columnId: int
    newSerialNumber: int