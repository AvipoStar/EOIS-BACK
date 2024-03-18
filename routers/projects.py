from typing import List

from fastapi import APIRouter

from Models.models import Project, ProjectDirectionId, CreateProject
from controllers.projects import create_project, get_projects, update_project, \
    get_projects_by_direction, get_project_directions

router = APIRouter()


@router.post('/createProject', tags=["Project"])
def create_Project(item: CreateProject):
    project = create_project(item)
    return project


@router.put('/updateProject', tags=["Project"])
def update_Project(item: Project):
    project = update_project(item)
    return project


@router.get('/getProjects', tags=["Project"])
def get_Project():
    project: Project = get_projects()
    return project


@router.post('/getProjectsByDirection', tags=["Project"])
def get_Projects_By_Direction(directions: ProjectDirectionId):
    project = get_projects_by_direction(directions.directionIds, directions.search)
    return project


@router.get('/getDirections', tags=["Project"])
def get_Directions():
    directions = get_project_directions()
    return directions
