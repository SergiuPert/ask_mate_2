import os
from os.path import join, dirname, realpath

from werkzeug.utils import secure_filename
from flask import url_for

import database_manager

UPLOADS_PATH = join(dirname(realpath(__file__)), "static\\img")


def upload_picture(file, owner_table):
    if file:
        file_name = file.filename
        filename = owner_table + "_id_" + str(database_manager.get_question_seq_value().get("last_value")) \
            if owner_table == 'question' else str(database_manager.get_answer_seq_value().get("last_value")) + \
            '.' + file_name.split('.')[1]
        path_to_file = "/images/" + filename
        file.save(os.path.join("static/images/", filename))
        return path_to_file

    return ""


def add_answer_number(questions):
    for index in range(len(questions)):
        answer_number = len(database_manager.get_answers_for_question(questions[index]))
        questions[index].update({"answer_number": answer_number})
    return questions


def add_answer_to_question(question):
    answers = database_manager.get_answers_for_question(question)
    question.update({"answers": answers})

    return question


def keep_view_question_untouch(question_id):
    question = database_manager.get_question(question_id)[0]
    question.update({"view_number": int(question.get("view_number")) - 1})
    database_manager.update_question(question)
    return question
