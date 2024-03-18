from fastapi import  APIRouter
from Models.models import Role
from controllers.roles import getRoles


router = APIRouter()

@router.get('/getRoles', tags=["Roles"])
def get_Roles():
    profiles = getRoles()
    return profiles
