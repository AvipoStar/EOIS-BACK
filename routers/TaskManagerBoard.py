from fastapi import APIRouter
from Models.models import CreateBoard, FirmId, MoveTask, CreateBoardList, MoveList
from controllers.TaskMenagerBoard import getBoards, createBoard, getTasksOnBoard, getTaskPriorities, getExecutors, \
    moveTask, createColumn, moveList

router = APIRouter()


@router.get('/getTaskPriorities', tags=["TaskManager"])
def get_Task_Priorities():
    tasks = getTaskPriorities()
    return tasks


@router.get('/getBoards/{idFirm}', tags=["TaskManager"])
def get_Boards(idFirm: int):
    boards = getBoards(idFirm)
    return boards


@router.post('/createBoard', tags=["TaskManager"])
def create_Board(board: CreateBoard):
    boardId = createBoard(board)
    return boardId


@router.post('/createColumn', tags=["TaskManager"])
def create_Column(column: CreateBoardList):
    columnId = createColumn(column)
    return columnId


@router.get('/getTasksOnBoard/{boardId}', tags=["TaskManager"])
def get_Tasks_On_Board(boardId: int):
    tasks = getTasksOnBoard(boardId)
    return tasks


@router.get('/getExecutors/{firmId}', tags=["TaskManager"])
def get_Executors(firmId: int):
    executors = getExecutors(firmId)
    return executors


@router.post('/moveTask', tags=["TaskManager"])
def move_Task(moveData: MoveTask):
    success = moveTask(moveData.taskId, moveData.newListId, moveData.newSerialNumber)
    return success


@router.post('/moveList', tags=["TaskManager"])
def move_List(moveData: MoveList):
    success = moveList(moveData.columnId, moveData.newSerialNumber)
    return success
