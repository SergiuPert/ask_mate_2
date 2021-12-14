import database_connection


@database_connection.connection_handler
def add_question(cursor, title, message, image):
    query = """
            INSERT INTO question(title, message, image) 
            VALUES (%(title)s, %(message)s, %(image)s );"""
    cursor.execute(query, {"title": title, "message": message, "image": image})


@database_connection.connection_handler
def add_answer(cursor, question_id, message, image):
    query = """
            INSERT INTO answer(question_id, message, image) 
            VALUES (%(question_id)s, %(message)s, %(image)s );"""
    cursor.execute(
        query, {"question_id": question_id, "message": message, "image": image}
    )


@database_connection.connection_handler
def get_questions(cursor):
    query = """
            SELECT * 
            FROM question;
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def get_question(cursor, id):
    query = """
            SELECT * 
            FROM question
            WHERE id = %(id)s;
            """
    cursor.execute(query, {"id": int(id)})
    return cursor.fetchone()


@database_connection.connection_handler
def update_question(cursor, question):
    query = """
               UPDATE question
               SET vote_number = %(vote_number)s,
                   view_number = %(view_number)s, 
                   message = %(message)s, 
                   title = %(title)s
               WHERE id = %(id)s
               ;"""
    cursor.execute(query, question)


@database_connection.connection_handler
def get_answers_for_question(cursor, question):
    query = """
            SELECT * 
            FROM answer
            WHERE question_id = %(id)s
            ;"""
    cursor.execute(query, {"id": int(question["id"])})
    return cursor.fetchall()


@database_connection.connection_handler
def get_answer_by_id(cursor, answer_id):
    query = """
                SELECT * 
                FROM answer
                WHERE id = %(id)s
                ;"""
    cursor.execute(query, {"id": int(answer_id)})
    return cursor.fetchone()


@database_connection.connection_handler
def update_answer(cursor, answer):
    query = """
               UPDATE answer
               SET message = %(message)s,
                vote_number = %(vote_number)s
               WHERE id=%(id)s;"""
    cursor.execute(query, answer)


@database_connection.connection_handler
def delete_question(cursor, question_id):
    delete_answers_for_question(question_id)
    query = """
                   DELETE FROM question
                   WHERE id=%(id)s
                   ;"""
    cursor.execute(query, {"id": int(question_id)})


@database_connection.connection_handler
def delete_answers_for_question(cursor, question_id):
    query = """
                   DELETE FROM answer
                   WHERE question_id=%(id)s
                   ;"""
    cursor.execute(query, {"id": int(question_id)})


@database_connection.connection_handler
def delete_answer(cursor, answer_id):
    query = """
                   DELETE FROM answer
                   WHERE id=%(id)s
                   ;"""
    cursor.execute(query, {"id": int(answer_id)})


@database_connection.connection_handler
def get_question_seq_value(cursor):
    query = """
            SELECT last_value 
            FROM question_id_seq
            ;"""
    cursor.execute(query)
    return cursor.fetchone()


@database_connection.connection_handler
def get_answer_seq_value(cursor):
    query = """
            SELECT last_value 
            FROM answer_id_seq
            ;"""
    cursor.execute(query)
    return cursor.fetchone()

