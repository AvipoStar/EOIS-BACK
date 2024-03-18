from typing import List
import mysql.connector
from Models.models import Project, ProjectDirection, CreateProject


def create_project(project: CreateProject):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="eois"
        )
        cursor = db.cursor()
        sql = "INSERT INTO project (name_project, description, direction) VALUES (%s, %s, %s)"
        values = (project.nameProject, project.descriptionProject, project.direction)
        cursor.execute(sql, values)
        project_id = cursor.lastrowid
        db.commit()
        cursor.close()
        db.close()
        return project_id
    except mysql.connector.Error as error:
        print("Error creating project:")
        print(error)
        return None


def update_project(project: Project):
    global db, cursor
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="eois"
        )
        cursor = db.cursor()
        sql = "UPDATE project SET name_project = %s, description = %s WHERE id_project = %s;"
        values = (project.nameProject, project.descriptionProject, project.id)
        cursor.execute(sql, values)
        db.commit()
    except mysql.connector.Error as error:
        print("Error executing query:", error)
    finally:
        if db:
            cursor.close()
            db.close()
    return project.nameProject


def get_projects():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="eois"
    )
    cursor = db.cursor()
    sql = "SELECT p.id_project, p.name_project, p.description, pd.name FROM project p JOIN project_direction pd ON pd.id_direction = p.direction"
    cursor.execute(sql)
    results = cursor.fetchall()
    response = {"projects": []}
    for result in results:
        project = Project(id=result[0],
                          nameProject=result[1],
                          descriptionProject=result[2],
                          direction=result[3])
        response["projects"].append(project)
    cursor.close()
    db.close()
    return response


def get_projects_by_direction(directionIds, search_query=""):
    if not directionIds:
        direction_condition = "1=1"  # Условие, которое всегда истинно
    else:
        directionIds_str = ', '.join(map(str, directionIds))
        direction_condition = f"p.direction IN ({directionIds_str})"

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="eois"
    )
    cursor = db.cursor()

    sql = f"SELECT p.id_project, p.name_project, p.description, p.direction FROM project p WHERE {direction_condition}"

    if search_query:
        sql += f" AND (p.name_project LIKE '%{search_query}%' OR p.description LIKE '%{search_query}%')"

    cursor.execute(sql)
    results = cursor.fetchall()

    response = {"projects": []}
    for result in results:
        project = {
            "id": result[0],
            "nameProject": result[1],
            "descriptionProject": result[2],
            "direction": result[3]
        }
        response["projects"].append(project)

    cursor.close()
    db.close()

    return response


def get_project_directions():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="eois"
    )
    cursor = db.cursor()
    sql = "SELECT * FROM project_direction"
    cursor.execute(sql)
    results = cursor.fetchall()
    directions = []
    for result in results:
        direction = ProjectDirection(id=result[0], name=result[1])
        directions.append(direction)
    cursor.close()
    db.close()
    return directions
