from flask import Flask, render_template, request, redirect, url_for

import database_manager
import util

app = Flask(__name__)


@app.route("/")
@app.route("/list")
def list_page():
    questions = database_manager.get_questions()
    questions = util.add_answer_number(questions)
    return render_template("list.html", questions=questions)


@app.route("/question/<question_id>")
def question_page(question_id):
    question = database_manager.get_question(question_id)
    question.update({"view_number": question["view_number"] + 1})
    database_manager.update_question(question)
    question = util.add_answer_to_question(question)
    answers = database_manager.get_answers_for_question(question)
    return render_template("question.html", question=question, answers=answers)


@app.route("/add-question", methods=["GET", "POST"])
def add_question_page():
    if request.method == "POST":
        print(request.files["image"])

        database_manager.add_question(
            title=request.form.get("question_title"),
            message=request.form.get("question_message"),
            image=util.upload_picture(request.files.get("image"), "question"),
        )
        return redirect(url_for("list_page"))
    return render_template("add_question.html")


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def add_answer_page(question_id):
    if request.method == "POST":
        database_manager.add_answer(
            question_id=question_id,
            message=request.form.get("answer"),
            image=util.upload_picture(request.files.get("image"),"answer"),
        )
        return redirect(url_for("question_page", question_id=question_id))
    return render_template("add_answer.html", question_id=question_id)


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def edit_question_page(question_id):
    question = database_manager.get_question(question_id)
    if request.method == "POST":
        question.update(
            {
                "title": request.form.get("title"),
                "message": request.form.get("message"),
            }
        )
        database_manager.update_question(question)
        return redirect(url_for("question_page", question_id=question_id))
    return render_template("edit_question.html", question=question)


@app.route("/answer/<answer_id>/edit-answer", methods=["GET", "POST"])
def edit_answer_page(answer_id):
    answer = database_manager.get_answer_by_id(answer_id)
    print(answer)
    if request.method == "POST":
        answer.update({"message": request.form.get("message")})
        database_manager.update_answer(answer)
        return redirect(
            url_for(
                "question_page",
                question_id=answer.get("question_id"),
            )
        )
    return render_template("edit_answer.html", answer=answer)


@app.route("/question/<question_id>/delete-question")
def delete_question(question_id):
    database_manager.delete_question(question_id)
    return redirect(url_for("list_page"))


@app.route("/question/<question_id>/vote-up")
def question_vote_up(question_id):
    question = database_manager.get_question(question_id)
    question.update(
        {
            "vote_number": int(question.get("vote_number")) + 1,
            "view_number": int(question.get("view_number")) - 1,
        }
    )
    database_manager.update_question(question)
    return redirect(url_for("question_page", question_id=question_id))


@app.route("/question/<question_id>/vote-down")
def question_vote_down(question_id):
    question = database_manager.get_question(question_id)
    question.update(
        {
            "vote_number": int(question.get("vote_number")) - 1,
            "view_number": int(question.get("view_number")) - 1,
        }
    )
    database_manager.update_question(question)
    return redirect(url_for("question_page", question_id=question_id))


@app.route("/answer/<answer_id>/delete-answer")
def delete_answer(answer_id):
    answer = database_manager.get_answer_by_id(answer_id)
    database_manager.delete_answer(answer_id)
    util.keep_view_question_untouch(answer.get("question_id"))
    return redirect(url_for("question_page", question_id=answer.get("question_id")))


@app.route("/answer/<answer_id>/vote-up")
def answer_vote_up(answer_id):
    answer = database_manager.get_answer_by_id(answer_id)
    answer.update({"vote_number": int(answer.get("vote_number")) + 1})
    database_manager.update_answer(answer)
    util.keep_view_question_untouch(answer.get("question_id"))
    return redirect(url_for("question_page", question_id=answer.get("question_id")))


@app.route("/answer/<answer_id>/vote-down")
def answer_vote_down(answer_id):
    answer = database_manager.get_answer_by_id(answer_id)
    answer.update({"vote_number": int(answer.get("vote_number")) - 1})
    database_manager.update_answer(answer)
    util.keep_view_question_untouch(answer.get("question_id"))
    return redirect(url_for("question_page", question_id=answer.get("question_id")))


if __name__ == "__main__":
    app.run(
        port=5000,
        debug=True,
    )
