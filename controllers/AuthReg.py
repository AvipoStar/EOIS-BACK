import mysql.connector
import datetime
import secrets
import string
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, status

from Models.models import RegistrationClass, Route

app = FastAPI()


def generate_token():
    token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
    expiration_date = datetime.now() + timedelta(days=1)
    return token, expiration_date


# Регистрация пользователя
def registerFunc(reg_data: RegistrationClass):
    # Подключение к базе данных MySQL
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="eois"
    )
    cursor = db.cursor()
    # Проверка наличия пользователя с таким логином
    cursor.execute("SELECT id_user FROM user WHERE login = %s", (reg_data.login,))
    if cursor.fetchone():
        db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Пользователь с таким логином уже существует")

    # Проверка наличия пользователя с такими ФИО
    cursor.execute("SELECT id_user FROM user WHERE name = %s AND surname = %s AND patronymic = %s",
                   (reg_data.name, reg_data.surname, reg_data.patronymic))
    if cursor.fetchone():
        db.close()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь с такими ФИО уже существует")

    # Регистрация нового пользователя
    cursor.execute("INSERT INTO user (name, surname, patronymic, bornDate, role, balance, login, password, gender) "
                   "VALUES (%s, %s, %s, %s, 2, 0, %s, %s, %s)",
                   (reg_data.name, reg_data.surname, reg_data.patronymic, reg_data.bornDate, reg_data.login,
                    reg_data.password, reg_data.gender))
    db.commit()
    db.close()


# Аутентификация пользователя
def loginFunc(login: str, password: str):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="eois"
    )
    cursor = db.cursor()
    cursor.execute("SELECT id_user, password FROM user WHERE login = %s", (login,))
    result = cursor.fetchone()

    if result:
        user_id, stored_password = result
        cursor.execute("SELECT token_value FROM token WHERE id_user = %s", (user_id,))
        existing_token = cursor.fetchone()

        if existing_token:
            token = existing_token[0]
            db.close()
            return {"token": token, "user_id": user_id}
        else:
            if password == stored_password:
                token, expiration_date = generate_token()
                cursor.execute("INSERT INTO token (id_user, token_value, create_time) VALUES (%s, %s, %s)",
                               (user_id, token, datetime.now()))
                db.commit()
                db.close()
                return {"token": token, "user_id": user_id}
            else:
                db.close()
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный пароль")
    else:
        db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")


# Проверяет наличие токена и его актуальность
def checkToken(token: str):
    # Подключение к базе данных MySQL
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="eois"
    )
    cursor = db.cursor()
    # Получение информации о токене из базы данных
    cursor.execute("SELECT id_user, create_time FROM token WHERE token_value = %s", (token,))
    result = cursor.fetchone()

    if result:
        user_id, create_time = result
        current_time = datetime.now()

        # Проверка актуальности токена (не истек ли срок его действия)
        if (current_time - create_time).days <= 1:
            db.close()
            return {'success': True, "user_id": user_id, "token": token}
        else:
            # Удаление просроченного токена из базы данных
            cursor.execute("DELETE FROM token WHERE token_value = %s", (token,))
            db.commit()
    db.close()
    return {'success': False, "user_id": -1, "token": token}


def getMenu(userId: int):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="eois"
        )
        cursor = db.cursor()

        cursor.execute(
            f'SELECT r.id, r.name FROM roletoroute rr '
            f'JOIN routes r ON rr.id_route = r.id '
            f'JOIN role ro ON ro.id = rr.id_role '
            f'JOIN user u ON u.id_user = {userId} '
            f'WHERE ro.id = u.role;'
        )
        results = cursor.fetchall()

        routeIds = []
        for result in results:
            routeId = {'id': result[0],
                       'name': result[1]}
            routeIds.append(routeId)

        cursor.close()
        db.close()
        return routeIds
    except mysql.connector.Error as error:
        print("Произошла ошибка при получении меню:")
        print(error)
        return error
