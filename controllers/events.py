from Models.models import EventType, Event, UserEvent
import mysql.connector

def getEventTypes():
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
    sql = "SELECT * FROM event_type"

    # Выполнение SQL запроса
    cursor.execute(sql)

    # Получение результатов запроса
    results = cursor.fetchall()

    eventTypes = []

    for result in results:
        eventType = EventType(id=result[0], nameEventType=result[1])
        eventTypes.append(eventType)

    # Закрытие соединения с базой данных
    cursor.close()
    db.close()

    # Возвращение списка проектов
    return eventTypes

def getEventsForUser(userId: int):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="eois"
    )
    cursor = db.cursor()
    sql = f"SELECT ue.user_id, u.name, u.surname, u.patronymic, e.date_time, ue.current_balance, e.description, CASE " \
          f"        WHEN e.event_type_id = 1 THEN -e.amount" \
          f"        WHEN e.event_type_id = 2 THEN e.amount" \
          f"    END AS amount FROM userevent ue " \
          f"JOIN event e ON ue.event_id = e.id_event " \
          f"JOIN user u ON e.initiator_id = u.id_user " \
          f"WHERE user_id = {userId};"
    cursor.execute(sql)
    results = cursor.fetchall()
    print(f'results {results}')
    events = []
    for result in results:
        event = UserEvent(  userId=result[0],
                            initiator=f'{result[2]} {result[1]} {result[3]}',
                            datetimeEvent=result[4],
                            currentBalance=result[5],
                            description=result[6] or "Без описание",
                            amount=result[7])
        events.append(event)
    cursor.close()
    db.close()
    return events

def createEvent(event: Event):
    print(f'{event}')
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="eois"
        )
        cursor = db.cursor()
        print(f'event {event}')
        sql = f"INSERT INTO event (event_type_id, target_user_id, initiator_id, date_time, amount, description) " \
              f"VALUES ({event.eventTypeId}, {event.targetUserId}, {event.initiatorId}, NOW(), {event.amount}, '{event.description}');"
        cursor.execute(sql)
        db.commit()
        sql2 = f"SELECT balance FROM user WHERE id_user = {event.targetUserId};"
        cursor.execute(sql2)
        results = cursor.fetchall()
        sql3 = ''
        if event.eventTypeId == 1:
            uvi = f'UPDATE user SET balance = {results[0][0] - event.amount} WHERE id_user = {event.targetUserId};'
        else:
            sql3 = f'UPDATE user SET balance = {results[0][0] + event.amount} WHERE id_user = {event.targetUserId};'
        cursor.execute(sql3)
        db.commit()
        cursor.close()
        db.close()
        return "Событие успешно создано"
    except mysql.connector.Error as error:
        print("Произошла ошибка при создании события:")
        print(error)
        return error

