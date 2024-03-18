from fastapi import APIRouter
from Models.models import CreateBoard, FirmId
from controllers.TaskMenagerBoard import getBoards, createBoard

router = APIRouter()


@router.post('/getBoards/', tags=["TaskManager"])
def get_Boards(idFirm: FirmId):
    boards = getBoards(idFirm.firmId)
    return boards


@router.post(f'/createBoard', tags=["TaskManager"])
def create_Board(board: CreateBoard):
    boardId = createBoard(board)
    return boardId
