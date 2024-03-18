from Models.models import Role, Task, CreateBoard, Board
import mysql.connector


def getBoards(idFirm: int):
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
              f"WHERE f.id_firm = {idFirm}"
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
        print("Произошла ошибка при получении досок:")
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
