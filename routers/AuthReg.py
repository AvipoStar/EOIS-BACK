from fastapi import APIRouter

from Models.models import LoginClass, RegistrationClass, Token, UserId
from controllers.AuthReg import registerFunc, loginFunc, checkToken, getMenu

router = APIRouter()


@router.post('/register', tags=["Auth"])
def reg(registrationData: RegistrationClass):
    token = registerFunc(registrationData)
    return token


@router.post('/login', tags=["Auth"])
def auth(loginData: LoginClass):
    token = loginFunc(loginData.login, loginData.password)
    return token


@router.post('/checkToken', tags=["Auth"])
def check_Token(token: Token):
    tokenInfo = checkToken(token.token)
    return tokenInfo


@router.post('/getMenu', tags=['Auth'])
def get_Menu(userId: UserId):
    routes = getMenu(userId.userId)
    return routes
