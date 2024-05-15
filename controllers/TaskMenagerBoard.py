from Models.models import CreateBoard, Board, TaskPriority, CreateBoardList, Task, CreateTask, UpdateTask
import mysql.connector

from controllers.users import getStudentsInFirms


def getTaskPriorities():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="eois"
        )
        cursor = db.cursor()
        sql = f"SELECT id, name, color FROM taskpriority"
        cursor.execute(sql)
        results = cursor.fetchall()
        priorities = []
        for result in results:
            priority = TaskPriority(id=result[0], name=result[1], color=result[2])
            priorities.append(priority)
        cursor.close()
        db.close()
        return priorities
    except mysql.connector.Error as error:
        print("Произошла ошибка при получении приоритетов задач:")
        print(error)
        return error


def getBoards(idFirm: list[int]):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="eois"
        )
        cursor = db.cursor()
        sql = f"SELECT b.id, b.name, b.description, b.coverColor " \
              f"FROM board b " \
              f"JOIN boardtofirm b1 ON b.id = b1.idBoard " \
              f"JOIN firm f ON b1.idFirm = f.id_firm " \
              f"WHERE f.id_firm IN ({','.join(map(str, idFirm))})"
        cursor.execute(sql)
        results = cursor.fetchall()
        boards = []
        for result in results:
            board = Board(id=result[0], name=result[1], description=result[2], coverColor=result[3])
            boards.append(board)
        cursor.close()
        db.close()
        return boards
    except mysql.connector.Error as error:
        print("Произошла ошибка при получении проектов:")
        print(error)
        return error


def createBoard(board: CreateBoard):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="eois"
        )
        # Создание объекта курсора
        cursor = db.cursor()
        # SQL запрос для вставки данных проекта в таблицу
        sql = f"INSERT INTO eois.board (name, description, coverColor) " \
              f"VALUES ('{board.name}', '{board.description}', '{board.coverColor}');"
        # Выполнение SQL запроса
        cursor.execute(sql)
        # Получение id созданного проекта
        board_id = cursor.lastrowid
        sql2 = f'INSERT INTO boardtofirm (idFirm, idBoard) VALUES ({board.firmId}, {board_id});'
        cursor.execute(sql2)
        # Подтверждение изменений в базе данных
        db.commit()
        # Закрытие соединения с базой данных
        cursor.close()
        db.close()
        return board_id
    except mysql.connector.Error as error:
        print("Произошла ошибка при создании доски:")
        print(error)
        return error


def editBoard(board: Board):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="eois"
        )
        # Создание объекта курсора
        cursor = db.cursor()
        # SQL запрос для вставки данных проекта в таблицу
        sql = f"UPDATE eois.board " \
              f"SET name = '{board.name}', description = '{board.description}', coverColor = '{board.coverColor}' " \
              f"WHERE id = {board.id};"
        # Выполнение SQL запроса
        cursor.execute(sql)
        # Подтверждение изменений в базе данных
        db.commit()
        # Закрытие соединения с базой данных
        cursor.close()
        db.close()
        return board.id
    except mysql.connector.Error as error:
        print("Произошла ошибка при редактировании доски:")
        print(error)
        return error


def createColumn(column: CreateBoardList):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="eois"
        )
        # Создание объекта курсора
        cursor = db.cursor()
        # SQL запрос для вставки данных проекта в таблицу
        sql = f"INSERT INTO eois.list ( name, idBoard, serialNumber) " \
              f"VALUES ('{column.name}', '{column.idBoard}', '{column.serialNumber}');"
        # Выполнение SQL запроса
        cursor.execute(sql)
        # Получение id созданного проекта
        column_id = cursor.lastrowid
        # Подтверждение изменений в базе данных
        db.commit()
        # Закрытие соединения с базой данных
        cursor.close()
        db.close()
        return column_id
    except mysql.connector.Error as error:
        print("Произошла ошибка при создании колонки:")
        print(error)
        return error


def getTasksOnBoard(boardId: int):
    try:

        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="eois"
        )

        cursor = db.cursor(dictionary=True)

        # Получаем информацию о доске
        cursor.execute("SELECT * FROM eois.board WHERE id = %s", (boardId,))
        board_info = cursor.fetchone()

        # Получаем все списки для данной доски
        cursor.execute("SELECT * FROM eois.list WHERE idBoard = %s", (boardId,))
        lists = cursor.fetchall()

        # Для каждого списка получаем задачи без сортировки по параметру serialNumber
        for l in lists:
            cursor.execute("SELECT * FROM eois.task WHERE idList = %s", (l["id"],))
            tasks = cursor.fetchall()
            l["tasksOnList"] = tasks

        cursor.close()
        db.close()

        return {"board_info": board_info, "lists": lists}
    except mysql.connector.Error as error:
        print("Произошла ошибка при получении задач:")
        print(error)
        return error


def getExecutors(firmId: int):
    students = getStudentsInFirms([firmId])
    return students


def moveTask(task_id: int, new_list_id: int, new_serial_number: int):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="eois"
        )
        cursor = db.cursor()

        try:
            # Получаем текущий порядковый номер задачи
            sql_select_current_serial = f"SELECT serialNumber FROM eois.task WHERE id = {task_id};"
            cursor.execute(sql_select_current_serial)
            current_serial_number = cursor.fetchone()[0]
        except Exception as e:
            print("Произошла ошибка при выполнении sql 1:")
            print(e)

        try:
            # Получаем idList перемещаемой задачи
            sql_select_list_id = f"SELECT idList FROM eois.task WHERE id = {task_id};"
            cursor.execute(sql_select_list_id)
            list_id = cursor.fetchone()[0]

            # Обновляем порядковый номер у задач в текущем списке, которые имеют больший порядковый номер,
            # чем перемещаемая задача, чтобы освободить место для перемещаемой задачи
            sql_update_higher_serial_numbers = f"UPDATE eois.task " \
                                               f"SET serialNumber = serialNumber - 1 " \
                                               f"WHERE idList = {list_id} " \
                                               f"AND serialNumber > {current_serial_number};"
            cursor.execute(sql_update_higher_serial_numbers)
        except Exception as e:
            print("Произошла ошибка при выполнении sql 2:")
            print(e)

        try:
            # Обновляем порядковый номер у задачи, которую перемещаем
            sql_update_moved_task = f"UPDATE eois.task SET idList = {new_list_id}, " \
                                    f"serialNumber = {new_serial_number} " \
                                    f"WHERE id = {task_id};"
            cursor.execute(sql_update_moved_task)
        except Exception as e:
            print("Произошла ошибка при выполнении sql 3:")
            print(e)

        try:
            # Обновляем порядковый номер у задач в новом списке, которые имеют порядковый номер больше
            # или равный новому порядковому номеру перемещаемой задачи
            sql_update_higher_serial_numbers_new_list = f"UPDATE eois.task SET serialNumber = serialNumber + 1 " \
                                                        f"WHERE idList = {new_list_id} " \
                                                        f"AND serialNumber >= {new_serial_number} " \
                                                        f"AND id != {task_id};"
            cursor.execute(sql_update_higher_serial_numbers_new_list)
        except Exception as e:
            print("Произошла ошибка при выполнении sql 4:")
            print(e)

        db.commit()
        cursor.close()
        db.close()
        return True
    except mysql.connector.Error as error:
        print("Произошла ошибка при перемещении задачи:")
        print(error)
        return False


def moveList(column_id: int, new_serial_number: int):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="eois"
        )
        cursor = db.cursor()

        try:
            # Получаем текущий порядковый номер колонки и идентификатор доски
            sql_select_current_serial = f"SELECT idBoard, serialNumber FROM eois.list WHERE id = {column_id};"
            cursor.execute(sql_select_current_serial)
            result = cursor.fetchone()
            if result:
                current_board_id, current_serial_number = result
            else:
                raise Exception("Не удалось получить текущий порядковый номер колонки")
        except Exception as e:
            print("Произошла ошибка при выполнении sql 1:")
            print(e)

        try:
            # Если новый порядковый номер меньше текущего, обновляем порядковые номера между ними в порядке возрастания
            if new_serial_number < current_serial_number:
                sql_update_serial_numbers = f"UPDATE eois.list " \
                                            f"SET serialNumber = serialNumber + 1 " \
                                            f"WHERE serialNumber >= {new_serial_number} " \
                                            f"AND serialNumber < {current_serial_number} " \
                                            f"AND idBoard = {current_board_id};"
            # Если новый порядковый номер больше текущего, обновляем порядковые номера между ними в порядке убывания
            else:
                sql_update_serial_numbers = f"UPDATE eois.list " \
                                            f"SET serialNumber = serialNumber - 1 " \
                                            f"WHERE serialNumber <= {new_serial_number} " \
                                            f"AND serialNumber > {current_serial_number} " \
                                            f"AND idBoard = {current_board_id};"
            cursor.execute(sql_update_serial_numbers)
        except Exception as e:
            print(e)

        try:
            # Обновляем порядковый номер перемещаемой колонки
            sql_update_moved_column = f"UPDATE eois.list SET serialNumber = {new_serial_number} " \
                                      f"WHERE id = {column_id};"
            cursor.execute(sql_update_moved_column)
        except Exception as e:
            print(e)

        db.commit()
        cursor.close()
        db.close()
        return True
    except mysql.connector.Error as error:
        print("Произошла ошибка при перемещении колонки:(")
        print(error)
        return False


def deleteBoard(boardID: int):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="eois"
        )
        cursor = db.cursor()
        print(f'-----------\n{boardID}\n-----------')
        # Удаление самой доски
        cursor.execute("DELETE FROM board WHERE id = %s", (boardID,))

        db.commit()

        return True
    except mysql.connector.Error as error:
        print("Произошла ошибка при удалении доски:")
        print(error)
        return False
    finally:
        cursor.close()
        db.close()


def createTask(task: CreateTask):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="eois"
        )
        # Создание объекта курсора
        cursor = db.cursor(dictionary=True)

        # Получение последнего serialNumber для idList
        sql = "SELECT serialNumber FROM eois.task WHERE idList = %s ORDER BY serialNumber DESC LIMIT 1;"
        cursor.execute(sql, (task.idList,))
        lastTask = cursor.fetchone()

        lastTaskSerialNumber = lastTask['serialNumber'] if lastTask else 0

        newTaskSerialNumber = lastTaskSerialNumber + 1

        # SQL запрос для вставки данных задачи в таблицу
        sql = (
            "INSERT INTO eois.task (name, discription, idList, creationDateTime, priority, deadLine, isDone, serialNumber) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s);")
        task_data = (task.name, task.description, task.idList, task.creationDateTime, task.priority, task.deadline, 0,
                     newTaskSerialNumber)

        # Выполнение SQL запроса
        cursor.execute(sql, task_data)

        # Получение id созданной задачи
        task_id = cursor.lastrowid

        for e in task.executors:
            sql = (
                "INSERT INTO eois.executor (idUser, idTask) VALUES (%s, %s);")
            task_data = (e, task_id)
            cursor.execute(sql, task_data)

        # Подтверждение изменений в базе данных
        db.commit()

        # Закрытие соединения с базой данных
        cursor.close()
        db.close()

        return task_id

    except mysql.connector.Error as error:
        print("Произошла ошибка при создании задачи:")
        print(error)
        return None


def updateTask(task: UpdateTask):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="eois"
        )

        # Создание объекта курсора
        cursor = db.cursor()

        # SQL запрос для обновления данных задачи в таблице
        sql = ("UPDATE eois.task "
               "SET name = %s, discription = %s, "
               "priority = %s, deadLine = %s "
               "WHERE id = %s;")
        task_data = (task.name, task.description, task.priority, task.deadline, task.id)

        # Выполнение SQL запроса
        cursor.execute(sql, task_data)

        # Получение id созданной задачи
        task_id = cursor.lastrowid

        for e in task.executors:
            sql = ("INSERT INTO eois.executor (idUser, idTask) VALUES (%s, %s);")
            task_data = (e, task_id)
            cursor.execute(sql, task_data)

        # Подтверждение изменений в базе данных
        db.commit()

        # Закрытие соединения с базой данных
        cursor.close()
        db.close()

        return task.id

    except mysql.connector.Error as error:
        print("Произошла ошибка при редактировании задачи:")
        print(error)
        return None
