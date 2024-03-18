from Models.models import Session
import mysql.connector
from datetime import datetime


def getSessions(search_string: str):
    print(f'search_string "{search_string}" search_string')
    # Подключение к базе данных MySQL
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="eois"
    )
    # Создание объекта курсора
    cursor = db.cursor()
    # SQL запрос для выборки всех сессий или сессий с поиском по входной строке
    if len(search_string) != 0:
        sql = "SELECT * FROM session WHERE place LIKE %s"
        cursor.execute(sql, ('%' + search_string + '%',))
    else:
        sql = "SELECT * FROM session"
        cursor.execute(sql)
    # Получение результатов запроса
    results = cursor.fetchall()
    print(f'results {results}')
    # Создание списка объектов Session для хранения результатов
    sessions = []
    # Итерация по результатам запроса и создание объектов Session
    for result in results:
        session = Session(id=result[0],
                          dateStart=result[1],
                          dateEnd=result[2],
                          place=result[3],
                          firmCount=result[4])
        sessions.append(session)
    # Закрытие соединения с базой данных
    cursor.close()
    db.close()
    # Возвращение списка сессий
    return sessions
def createSessions(session: Session):
    print(f'session {session}')
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="eois"
    )
    # Создание объекта курсора
    cursor = db.cursor()

    # SQL запрос для вставки данных проекта в таблицу
    sql = f'INSERT INTO session (place, date_start, date_end, firm_count) VALUES ' \
          f'("{session.place}", "{session.dateStart}", "{session.dateEnd}", "{session.firmCount}");'

    # Выполнение SQL запроса
    cursor.execute(sql)
    # Получение значения LAST_INSERT_ID()
    last_insert_id = cursor.lastrowid

    # Подтверждение изменений в базе данных
    db.commit()

    # Закрытие соединения с базой данных
    cursor.close()
    db.close()
    return last_insert_id
