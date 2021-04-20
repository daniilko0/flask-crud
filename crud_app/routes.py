from datetime import datetime

from flask import Flask
from flask import json, request, url_for, redirect, render_template
from werkzeug.exceptions import HTTPException

from crud_app.config import Config
from crud_app.models import Book

app = Flask(__name__)
app.config.from_object(Config)

books = [
    Book(isbn="123", name="123", author="qwerty", pages=123, year=2021, added_on="2021-03-21 12:00:00", deleted=False),
]


@app.route("/")
@app.route("/books")
def homepage():
    has_not_deleted = any(book for book in books if not book.deleted)
    return render_template("home.html", books=books, has_not_deleted=has_not_deleted)


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        form = dict(request.form)
        form.update({"added_on": datetime.strptime(form.get("added_on"), "%d-%m-%Y %H:%M"), "deleted": False})
        books.append(Book(**form))
        return redirect(url_for("homepage"))
    return render_template("crud/create.html")


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    try:
        entry = books[id]
    except IndexError:
        return render_template('404.html'), 404

    if request.method == "GET":
        return render_template("crud/update.html", entry=entry, entry_id=id)

    form = dict(request.form)
    for key, _ in entry:
        setattr(books[id], key, form.get(key))

    return redirect(url_for("homepage"))


@app.route("/delete/<int:id>")
def delete(id):
    for index, book in enumerate(books):
        if index == id:
            book.deleted = True

    return redirect(url_for("homepage"))


@app.errorhandler(HTTPException)
def handle_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "type": e.code,
        "message": e.name,
        "data": {
            "description": e.description,
        },
    })
    response.content_type = "application/json"
    return response


if __name__ == '__main__':
    app.run(debug=True)
