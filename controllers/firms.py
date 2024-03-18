from typing import List

from Models.models import  Student
import mysql.connector


def getFirmsOnCurrentSession():
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
    sql = "SELECT * FROM firm f JOIN session s ON f.session_id = s.id_session " \
          "WHERE s.date_start <= CURDATE() AND s.date_end >= CURDATE(); "

    # Выполнение SQL запроса
    cursor.execute(sql)

    # Получение результатов запроса
    results = cursor.fetchall()

    # Создание списка объектов Project для хранения результатов
    firms = []

    # Итерация по результатам запроса и создание объектов
    for result in results:
        print(f'result {result}')
        firm = {'id': result[0], 'number': result[1]}
        firms.append(firm)

    # Закрытие соединения с базой данных
    cursor.close()
    db.close()

    # Возвращение списка проектов
    return firms

def getFirmsOnSession(sessionId: int):
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
    sql = f"SELECT * FROM firm f WHERE f.session_id = {sessionId}"
    # Выполнение SQL запроса
    cursor.execute(sql)

    # Получение результатов запроса
    results = cursor.fetchall()

    # Создание списка объектов Project для хранения результатов
    firms = []

    # Итерация по результатам запроса и создание объектов
    for result in results:
        print(f'result {result}')
        firm = {'id': result[0], 'number': result[1]}
        firms.append(firm)

    # Закрытие соединения с базой данных
    cursor.close()
    db.close()

    # Возвращение списка проектов
    return firms


def getStudentsOnCurrentSession():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="eois"
    )
    cursor = db.cursor()
    sql = 'SELECT u.id_user, u.name, u.surname, u.patronymic, u.age, u.gender, p1.name_profile, p.name_project, u.balance, f.number  ' \
          'FROM eois.usertofirmtoprofile AS e   ' \
          'JOIN firm f ON f.id_firm = e.id_firm  ' \
          'JOIN user u ON u.id_user = e.id_user  ' \
          'JOIN session s ON f.session_id = s.id_session  ' \
          'JOIN project p ON e.id_project = p.id_project  ' \
          'JOIN profile p1 ON e.id_profile = p1.id_profile ' \
          'WHERE s.date_start <= CURDATE() AND s.date_end >= CURDATE();'
    cursor.execute(sql)
    results = cursor.fetchall()
    print(f'results {results}')
    users = []
    for result in results:
        user = Student( id=result[0],
                        name=result[1],
                        surname=result[2],
                        patronymic=result[3] or "",
                        age=result[4],
                        gender=result[5],
                        profile=result[6],
                        project=result[7],
                        balance=result[8],
                        firm=result[9],
                        )
        print(f'user {user}')
        users.append(user)
    cursor.close()
    db.close()
    return users
