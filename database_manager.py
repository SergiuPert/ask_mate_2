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
            FROM question
            ;"""
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


@database_connection.connection_handler
def add_comment_question(cursor, message, question_id):
    query = """
            INSERT INTO comment(message, question_id) 
            VALUES (%(message)s, %(question_id)s);"""
    cursor.execute(query, {"message": message, "question_id": question_id})


@database_connection.connection_handler
def add_comment_answer(cursor, message, answer_id):
    query = """
            INSERT INTO comment(message, answer_id) 
            VALUES (%(message)s, %(answer_id)s);"""
    cursor.execute(query, {"message": message, "answer_id": answer_id})


@database_connection.connection_handler
def get_question_by_search(cursor, search_term):
    query = """
        SELECT submission_time, view_number, vote_number, title, message, image
        FROM question
        WHERE title=%(search_term)s
        OR message=%(search_term)s
        ORDER BY submission_time
            ;"""
    cursor.execute(query, {"search_term": search_term})
    return cursor.fetchall(), search_term


@database_connection.connection_handler
def delete_comment(cursor, comment):
    query = """
          DELETE FROM comment
          WHERE id = %(id)s
           ;"""
    cursor.execute(query, comment)


@database_connection.connection_handler
def update_comment(cursor, comment):
    query = """
            UPDATE comment
            SET 
            message = %(message)s,
            edited_count = %(edited_count)s
            WHERE id=%(id)s
            ;"""
    cursor.execute(query, comment)


@database_connection.connection_handler
def get_comment_by_id(cursor, comment_id):
    query = """
                    SELECT * 
                    FROM comment
                    WHERE id = %(id)s
                    ;"""
    cursor.execute(query, {"id": int(comment_id)})
    return cursor.fetchone()


@database_connection.connection_handler
def get_question_by_search(cursor, search_term):
    query = """
        SELECT submission_time, view_number, vote_number, title, message, image
        FROM question
        WHERE LOWER(title) LIKE LOWER(%(search_term)s)
        OR LOWER(message) LIKE LOWER(%(search_term)s)
        ORDER BY submission_time
            ;"""
    cursor.execute(query, {"search_term": ("%" + search_term + "%")})
    return cursor.fetchall(), search_term


@database_connection.connection_handler
def get_latest_five_questions(cursor):
    query = """
        SELECT *
        FROM question
        ORDER BY id DESC  
            ;"""
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def get_answer_comments(cursor, answer):
    query = """
            SELECT *
            FROM comment
            WHERE answer_id = %(id)s
            ;"""
    cursor.execute(query, answer)
    return cursor.fetchall()


@database_connection.connection_handler
def get_question_comments(cursor, question):
    query = """
            SELECT *
            FROM comment
            WHERE question_id = %(id)s
            ;"""
    cursor.execute(query, question)
    return cursor.fetchall()


@database_connection.connection_handler
def add_tag(cursor, name):
    query = """
        INSERT INTO tag (name)
        VALUES  (
                LOWER(%(name)s)
                )   
            ;"""
    cursor.execute(query, {"name": name})


@database_connection.connection_handler
def add_tag_relation(cursor, question_id, tag_id):
    query = """
        INSERT INTO question_tag
        VALUES  (
                %(question_id)s,
                %(tag_id)s
                )   
            ;"""
    cursor.execute(query, {"question_id": question_id, "tag_id": tag_id})


@database_connection.connection_handler
def get_tag_by_name(cursor, tag_name):
    query = """
            SELECT *
            FROM tag 
            WHERE name = LOWER(%(name)s) 
                ;"""
    cursor.execute(query, {"name": tag_name})
    return cursor.fetchone()


@database_connection.connection_handler
def get_tag_by_id(cursor, tag_id):
    query = """
            SELECT *
            FROM tag 
            WHERE id = %(id)s
                ;"""
    cursor.execute(query, {"id": tag_id})
    return cursor.fetchone()


@database_connection.connection_handler
def get_sorted_questions(cursor, sort_by, order_direction):
    query = f"""
                SELECT *
                FROM question 
                order by {sort_by} {order_direction}
                    ;"""
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def get_tag_relation(cursor, question_id):
    query = """
                SELECT *
                FROM question_tag 
                WHERE question_id = %(question_id)s 
                    ;"""
    cursor.execute(query, {"question_id": question_id})
    return cursor.fetchall()


@database_connection.connection_handler
def delete_tag_relation(cursor, question_id, tag_id):
    query = """
            DELETE FROM question_tag
            WHERE 
                question_id = %(question_id)s
            AND
                tag_id = %(tag_id)s
            ;"""
    cursor.execute(query, {"question_id": question_id, "tag_id": tag_id})
