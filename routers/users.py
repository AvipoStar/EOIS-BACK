from fastapi import APIRouter, File, UploadFile
from starlette.responses import JSONResponse
import os

from Models.models import User, changeLoginPasswordClass, JoinTheCompanyClass, FirmIds, ProfileId, UserId
from controllers.users import getAllStudents, getAllCurators, createCurator, createStudent, getUserById, \
    changeLoginPassword, getStudentsInFirms, getCuratorsByProfile, check_user_firm_relation, attach_user_to_firm

router = APIRouter()


@router.get('/getAllStudents', tags=["User"])
def get_All_Students():
    users = getAllStudents()
    return users


@router.get('/getAllCurators', tags=["User"])
def get_All_Curators():
    users = getAllCurators()
    return users


@router.get('/getAllCurators', tags=["User"])
def get_All_Curators():
    users = getAllCurators()
    return users


@router.post('/getCuratorsByProfile', tags=["User"])
def get_Curators_By_Profile(profile: ProfileId):
    user = getCuratorsByProfile(profile.profileIds, profile.search)
    return user


@router.post('/getStudentsInFirms', tags=["User"])
def get_Users_In_Firms(firms: FirmIds):
    user = getStudentsInFirms(firms.firmIds)
    return user


@router.get('/getUserById/{id_user}', tags=["User"])
def get_User_By_Id(id_user: int):
    print(f'id_user {id_user}')
    user = getUserById(id_user)
    return user


@router.post('/createCurator', tags=["User"])
def create_Curator(user: User):
    userId = createCurator(user)
    return userId


@router.post('/createStudent', tags=["User"])
def create_Student(user: User):
    userId = createStudent(user)
    return userId


@router.post('/changeLoginPassword', tags=["User"])
def change_Login_Password(userData: changeLoginPasswordClass):
    user = changeLoginPassword(userData.id, userData.newLogin, userData.newPassword, userData.photoPath)
    return user


@router.post('/attachUserToFirm', tags=["User"])
def attachUserToFirm(userData: JoinTheCompanyClass):
    user = attach_user_to_firm(userData)
    return user


@router.post('/checkUserFirmRelation', tags=["User"])
def checkUserFirmRelation(userData: UserId):
    user = check_user_firm_relation(userData.userId)
    return user


