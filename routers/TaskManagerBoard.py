from fastapi import APIRouter
from Models.models import CreateBoard, FirmId, MoveTask, CreateBoardList, MoveList, FirmIds, BoardId, Board, CreateTask, \
    Task, UpdateTask
from controllers.TaskMenagerBoard import getBoards, createBoard, getTasksOnBoard, getTaskPriorities, getExecutors, \
    moveTask, createColumn, moveList, deleteBoard, editBoard, createTask, updateTask

router = APIRouter()


@router.get('/getTaskPriorities', tags=["TaskManager"])
def get_Task_Priorities():
    tasks = getTaskPriorities()
    return tasks


@router.post('/getBoards', tags=["TaskManager"])
def get_Boards(ids: FirmIds):
    boards = getBoards(ids.firmIds)
    return boards


@router.post('/createBoard', tags=["TaskManager"])
def create_Board(board: CreateBoard):
    boardId = createBoard(board)
    return boardId

@router.patch('/editBoard', tags=["TaskManager"])
def edit_Board(board: Board):
    boardId = editBoard(board)
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


@router.delete('/deleteBoard', tags=["TaskManager"])
def delete_board(board: BoardId):
    result = deleteBoard(board.boardId)
    return result

@router.post('/createTask', tags=["TaskManager"])
def create_task(task: CreateTask):
    result = createTask(task)
    return result

@router.patch('/updateTask', tags=["TaskManager"])
def update_ask(task: UpdateTask):
    result = updateTask(task)
    return result
