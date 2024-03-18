from Models.models import Role
import mysql.connector

def getRoles():
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
    sql = "SELECT * FROM role"

    # Выполнение SQL запроса
    cursor.execute(sql)

    # Получение результатов запроса
    results = cursor.fetchall()

    # Создание списка объектов Project для хранения результатов
    roles = []

    # Итерация по результатам запроса и создание объектов Project
    for result in results:
        role = Role(id=result[0], nameRole=result[1])
        roles.append(role)

    # Закрытие соединения с базой данных
    cursor.close()
    db.close()

    # Возвращение списка проектов
    return roles
