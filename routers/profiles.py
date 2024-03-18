from fastapi import  APIRouter
from Models.models import Profile
from controllers.profiles import getProfiles


router = APIRouter()

@router.get('/getProfiles', tags=["Profile"])
def get_Profiles():
    profiles = getProfiles()
    return profiles