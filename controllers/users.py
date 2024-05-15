from typing import List

from fastapi import HTTPException

from Models.models import User, JoinTheCompanyClass, Student, Curator
import mysql.connector


def getAllCurators():
    # Подключение к базе данных MySQL
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="eois"
    )

    # Создание объекта курсора
    cursor = db.cursor()

    # SQL запрос для выборки всех проектов
    sql = "SELECT * FROM user WHERE role = 1;"

    # Выполнение SQL запроса
    cursor.execute(sql)

    # Получение результатов запроса
    results = cursor.fetchall()

    users = []
    for result in results:
        user = User(id=result[0],
                    name=result[1],
                    surname=result[2],
                    patronymic=result[3],
                    bornDate=result[4],
                    roleId=result[5],
                    balance=result[6] or 0,
                    profileId=result[10],
                    photoPath=result[11]
                    )
        users.append(user)
        # Закрытие соединения с базой данных
        cursor.close()
        db.close()
    return users


def getCuratorsByProfile(profileIds: List[int], search_query: str = None):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="eois"
    )
    cursor = db.cursor()
    sql1 = "SELECT u.id_user, u.name, u.surname, u.patronymic, u.bornDate, u.gender, u.profile, u.photoPath " \
           "FROM user u " \
           "WHERE u.profile IN ("
    sql2 = ', '.join(map(str, profileIds))
    sql3 = ")"
    sql = sql1 + sql2 + sql3
    if search_query:
        sql += " AND (u.name LIKE '%{}%' OR u.surname LIKE '%{}%')".format(search_query,
                                                                           search_query,
                                                                           search_query)
    cursor.execute(sql)
    results = cursor.fetchall()
    users = []
    for result in results:
        user = Curator(id=result[0],
                       name=result[1],
                       surname=result[2],
                       patronymic=result[3],
                       bornDate=result[4],
                       gender=result[5],
                       profile=result[6],
                       photoPath=result[7] or "",
                       )
        users.append(user)
    cursor.close()
    db.close()
    return {"curators": users}


def getAllStudents():
    # Подключение к базе данных MySQL
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="eois"
    )

    # Создание объекта курсора
    cursor = db.cursor()

    # SQL запрос для выборки всех проектов
    sql = "SELECT * FROM user WHERE role = 2;"

    # Выполнение SQL запроса
    cursor.execute(sql)

    # Получение результатов запроса
    results = cursor.fetchall()
    users = []

    for result in results:
        user = User(id=result[0],
                    name=result[1],
                    surname=result[2],
                    patronymic=result[3] or "",
                    bornDate=result[4],
                    roleId=result[5],
                    balance=result[6] or 0,
                    gender=result[9],
                    profileId=result[10],
                    photoPath=result[11]
                    )
        users.append(user)
    # Закрытие соединения с базой данных
    cursor.close()
    db.close()
    return users


def getStudentsInFirms(firmIds: List[int]):
    # Подключение к базе данных MySQL
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="eois"
    )
    # Создание объекта курсора
    cursor = db.cursor()
    sql = "SELECT u1.id_user, u1.surname, u1.name, u1.patronymic " \
          "FROM usertofirmtoprofile u " \
          "JOIN user u1 ON u.id_user = u1.id_user " \
          f"WHERE u.id_firm IN ({', '.join(map(str, firmIds))});"
    print(f'sql - {sql}')
    cursor.execute(sql)
    # Получение результатов запроса
    results = cursor.fetchall()
    users = []
    for result in results:
        user = {'id': result[0],
                'name': result[2],
                'surname': result[1],
                'patronymic': result[3] or "", }

        users.append(user)
    # Закрытие соединения с базой данных
    cursor.close()
    db.close()
    return users


def getUserById(userId: int):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="eois"
        )
        cursor = db.cursor()

        sql = f"SELECT * FROM user WHERE id_user = '{userId}';"
        cursor.execute(sql)
        results = cursor.fetchall()

        db.commit()

        sql1 = f"SELECT f.id_firm " \
               f"FROM eois.usertofirmtoprofile AS e " \
               f"JOIN firm f ON f.id_firm = e.id_firm " \
               f"JOIN user u ON u.id_user = e.id_user " \
               f"JOIN session s ON f.session_id = s.id_session " \
               f"WHERE e.id_user = {userId} " \
               f"AND s.date_start <= CURDATE() " \
               f"AND s.date_end >= CURDATE();"
        cursor.execute(sql1)
        res = cursor.fetchall()

        attachedFirmId = -1
        if len(res) > 0:
            attachedFirmId = res[0][0]

        cursor.close()
        db.close()

        if len(results) != 0:
            user = User(id=results[0][0],
                        name=results[0][1],
                        surname=results[0][2],
                        patronymic=results[0][3] or "",
                        bornDate=results[0][4],
                        roleId=results[0][5],
                        balance=results[0][6],
                        login=results[0][7],
                        password=results[0][8],
                        gender=results[0][9],
                        profileId=results[0][10],
                        photoPath=results[0][11],
                        attachedFirmId=attachedFirmId
                        )
            return user
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except mysql.connector.Error as error:
        print("Произошла ошибка при получении пользователя:")
        print(error)
        return error


def createCurator(user: User):
    # Подключение к базе данных MySQL
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="eois"
    )
    # Создание объекта курсора
    cursor = db.cursor()
    # SQL запрос для вставки данных пользователя в таблицу
    sql = "INSERT INTO user (name, surname, patronymic, age, role, login, password, profile) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    # Значения для вставки в запрос
    values = (user.name, user.surname, user.patronymic, user.age, 1, user.login, user.password, user.profileId)
    # Выполнение SQL запроса
    cursor.execute(sql, values)
    # Подтверждение изменений в базе данных
    db.commit()
    # Закрытие соединения с базой данных
    cursor.close()
    db.close()
    return cursor.lastrowid


def createStudent(user: User):
    # Подключение к базе данных MySQL
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="eois"
    )
    # Создание объекта курсора
    cursor = db.cursor()
    # SQL запрос для вставки данных студента в таблицу
    sql = f"INSERT INTO user (name, surname, patronymic, age, role, balance, login, password) VALUES ('{user.name}', '{user.surname}', '{user.patronymic}', '{user.age}', 2, 0, '{user.login}', '{user.password}');"
    # Выполнение SQL запроса
    cursor.execute(sql)
    # Подтверждение изменений в базе данных
    db.commit()
    # Закрытие соединения с базой данных
    cursor.close()
    db.close()
    return "Студент успешно создан"


def changeLoginPassword(id: int, newLogin: str, newPassword: str, photoPath: str):
    # Подключение к базе данных MySQL
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="eois"
    )
    # Создание объекта курсора
    cursor = db.cursor()
    # SQL запрос для обновления логина и пароля
    sql = f"UPDATE user SET login = '{newLogin}', password = '{newPassword}', photoPath = '{photoPath}' WHERE id_user = {id};"
    # Выполнение SQL запроса
    cursor.execute(sql)
    # Подтверждение изменений в базе данных
    db.commit()
    # Запрос для получения обновленного элемента
    select_sql = f"SELECT id_user, login, password FROM user WHERE id_user = {id};"
    cursor.execute(select_sql)
    result = cursor.fetchone()
    # Закрытие соединения с базой данных
    cursor.close()
    db.close()
    # Создание словаря с обновленным элементом
    return {'id': result[0], 'login': result[1] or "", 'password': result[2] or ""}


def check_user_firm_relation(userId: int):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="eois"
    )
    cursor = db.cursor()
    cursor.execute("SELECT f.number, f.name, GROUP_CONCAT(p1.name_project SEPARATOR ', ') AS projects, p.id_profile " \
                   "FROM usertoproject u " \
                   "JOIN usertofirmtoprofile u1 ON u.userId = u1.id " \
                   "JOIN user u2 ON u1.id_user = u2.id_user " \
                   "JOIN firm f ON u1.id_firm = f.id_firm " \
                   "JOIN project p1 ON u.projectId = p1.id_project " \
                   "JOIN profile p ON u1.id_profile = p.id_profile " \
                   f"WHERE u1.id_user = {userId} " \
                   "GROUP BY f.number, f.name, u2.photoPath, p.id_profile;")
    existing_record = cursor.fetchone()
    cursor.close()
    db.close()
    print(existing_record)
    return {'firm_number': existing_record[0], 'firm_name': existing_record[1], 'projects': existing_record[2],
            'profile': existing_record[3]}


def attach_user_to_firm(userData: JoinTheCompanyClass):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="eois"
    )
    cursor = db.cursor()

    # Добавляем каждый проект из списка projectIds

    sql1 = f"INSERT INTO usertofirmtoprofile (id_user, id_firm, id_profile) " \
           f"VALUES ({userData.userId}, {userData.firmId}, {userData.profileId});"
    cursor.execute(sql1)
    last_insert_id = cursor.lastrowid

    for projectId in userData.projectIds:
        sql2 = f"INSERT INTO usertoproject (userId, projectId)" \
               f"VALUES ({last_insert_id}, {projectId});"
        cursor.execute(sql2)

    db.commit()
    cursor.close()
    db.close()

    return True


def getUserSessions(userId: int):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="eois"
        )
        cursor = db.cursor()

        sql = f"SELECT ufp.id_user,  f.number, f.name, f.session_id, p.id_profile " \
              f"FROM usertofirmtoprofile ufp " \
              f"JOIN profile p ON p.id_profile = ufp.id_profile " \
              f"JOIN firm f ON f.id_firm = ufp.id_firm " \
              f"WHERE id_user = '{userId}';"
        cursor.execute(sql)
        results = cursor.fetchall()

        db.commit()
        sessions = []
        for result in results:
            session = {"id_user": result[0],
                       "firm_number": result[1],
                       "firm_name": result[2],
                       "session_id": result[3],
                       "id_profile": result[4],
                       }
            sessions.append(session)
        return sessions

    except mysql.connector.Error as error:
        print("Произошла ошибка при получении смен:")
        print(error)
        return error
