from Models.models import Project, Profile
import mysql.connector

def getProfiles():
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
    sql = "SELECT * FROM profile"

    # Выполнение SQL запроса
    cursor.execute(sql)

    # Получение результатов запроса
    results = cursor.fetchall()

    # Создание списка объектов Project для хранения результатов
    profiles = []

    # Итерация по результатам запроса и создание объектов Project
    for result in results:
        profile = Profile(id=result[0], nameProfile=result[1])
        profiles.append(profile)

    # Закрытие соединения с базой данных
    cursor.close()
    db.close()

    # Возвращение списка проектов
    return profiles