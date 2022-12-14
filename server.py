from flask import Flask, render_template, request, redirect, url_for

import database_manager
import util

app = Flask(__name__)


@app.route("/")
def main_page():
    questions = database_manager.get_latest_five_questions()
    first_five = util.get_first_five_dicts(questions)
    first_five = util.add_answer_number(first_five)
    first_five = util.get_tag_for_questions(first_five)
    return render_template("list.html", questions=first_five)


@app.route("/list")
def list_page():
    questions = database_manager.get_questions()
    questions = util.add_answer_number(questions)
    questions = util.get_tag_for_questions(questions)
    return render_template("list.html", questions=questions)


@app.route("/question/<question_id>")
def question_page(question_id):
    question = database_manager.get_question(question_id)
    question.update({"view_number": question["view_number"] + 1})
    database_manager.update_question(question)
    question = util.add_answers_to_question(question)
    question = util.add_comments_to_question(question)
    question = util.get_tag_for_question(question)
    return render_template("question.html", question=question)


@app.route("/add-question", methods=["GET", "POST"])
def add_question_page():
    if request.method == "POST":
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
            image=util.upload_picture(request.files.get("image"), "answer"),
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


@app.route("/question/<question_id>/new-comment", methods=["GET", "POST"])
def add_question_comment_page(question_id):
    if request.method == "POST":
        database_manager.add_comment_question(
            question_id=question_id, message=request.form.get("comment_message")
        )
        return redirect(url_for("question_page", question_id=question_id))
    return render_template("add_question_comment.html", question_id=question_id)


@app.route("/answer/<answer_id>/new-comment", methods=["GET", "POST"])
def add_answer_comment_page(answer_id):
    answer = database_manager.get_answer_by_id(answer_id)
    if request.method == "POST":
        database_manager.add_comment_answer(
            answer_id=answer.get("id"), message=request.form.get("comment_message")
        )
        return redirect(url_for("question_page", question_id=answer.get("question_id")))
    return render_template("add_answer_comment.html", answer_id=answer_id)


@app.route("/search")
def search_question():
    questions, search_term = database_manager.get_question_by_search(request.args.get("q"))
    questions = util.add_answer_number(questions)
    questions = util.get_tag_for_questions(questions)
    return render_template("list.html", questions=questions, search_term=search_term)


@app.route("/comment/<comment_id>/edit", methods=["GET", "POST"])
def edit_comment_page(comment_id):
    comment = database_manager.get_comment_by_id(comment_id)
    if request.method == "POST":
        comment.update({"message": request.form.get("message")})
        comment.update({"edited_count": (comment.get("edited_count") + 1)})
        database_manager.update_comment(comment)
        return redirect(
            url_for(
                "question_page",
                question_id=comment.get("question_id"),
            )
        )
    return render_template("edit_comment.html", comment=comment)


@app.route("/comments/<comment_id>/delete")
def delete_comment_page(comment_id):
    comment = database_manager.get_comment_by_id(comment_id)
    database_manager.delete_comment(comment)
    if not comment.get("question_id"):
        answer = database_manager.get_answer_by_id(comment.get("answer_id"))
        comment.update({"question_id": answer.get("question_id")})
    util.keep_view_question_untouch(comment.get("question_id"))
    return redirect(url_for("question_page", question_id=comment.get("question_id")))


@app.route("/question/<question_id>/new-tag", methods=["GET", "POST"])
def add_tag_page(question_id):
    if request.method == "POST":
        util.add_tag_to_question(
            question_id=question_id,
            tag_name=request.form.get("tag")
        )
        return redirect(url_for("question_page", question_id=question_id))
    return render_template("add_tag.html", question_id=question_id)


@app.route("/question/<question_id>/tag/<tag_id>/delete-tag")
def delete_tag_page(question_id, tag_id):
    database_manager.delete_tag_relation(question_id, tag_id)
    return redirect(url_for('list_page'))


@app.route("/sort_by")
def sort_by():
    questions = database_manager.get_sorted_questions(request.args.get("sort_by"), request.args.get("order_direction"))
    return render_template('list.html', questions=questions)


if __name__ == "__main__":
    app.run(
        port=5000,
        debug=True,
    )
