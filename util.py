import os
from os.path import join, dirname, realpath

from werkzeug.utils import secure_filename
from flask import url_for

import database_manager

UPLOADS_PATH = join(dirname(realpath(__file__)), "static", "images")


def upload_picture(file, owner_table):
    if file:
        filename = f"{owner_table}_id_{str(database_manager.get_question_seq_value().get('last_value') + 1) if owner_table == 'question' else str(database_manager.get_answer_seq_value().get('last_value') + 1)}.jpg"
        path_to_file = join(UPLOADS_PATH, filename)
        file.save(path_to_file)
        return os.path.join("images", filename)

    return ""


def add_answer_number(questions):
    for index in range(len(questions)):
        answer_number = len(database_manager.get_answers_for_question(questions[index]))
        questions[index].update({"answer_number": answer_number})
    return questions


def add_answers_to_question(question):
    answers = database_manager.get_answers_for_question(question)
    for index in range(len(answers)):
        answers[index] = add_comments_to_answer(answers[index])
    question.update({"answers": answers})
    return question


def add_comments_to_question(question):
    comments = database_manager.get_question_comments(question)
    print(comments)
    question.update({"comments": comments})
    return question


def add_comments_to_answer(answer):
    comments = database_manager.get_answer_comments(answer)
    print(comments)

    answer.update({"comments": comments})
    return answer


def keep_view_question_untouch(question_id):
    question = database_manager.get_question(question_id)
    question.update({"view_number": int(question.get("view_number")) - 1})
    database_manager.update_question(question)
    return question


def get_first_five_dicts(dicts):
    first_five = []
    for index in range(5):
        first_five.append(dicts[index])
    return first_five


def add_tag_to_question(question_id, tag_name):
    tag = database_manager.get_tag_by_name(tag_name)
