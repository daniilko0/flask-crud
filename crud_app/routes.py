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
    Book(isbn="123", name="123", author="uiop", pages=256, year=2021, added_on="2021-03-21 12:00:00", deleted=False),
    Book(isbn="123", name="123", author="ghjk", pages=567, year=2021, added_on="2021-03-21 12:00:00", deleted=False),
    Book(isbn="123", name="123", author="xcvb", pages=3, year=2021, added_on="2021-03-21 12:00:00", deleted=False),
]


@app.route("/")
@app.route("/books")
def homepage():
    args = dict(request.args)
    data = books

    if "filter" in args:
        query = args.get("filter")
        data = [book for book in books if query in book.isbn or query in book.name or query in book.author]

    if "sort" in args:
        field = args.get("sort")

        if field[0] == "-":
            reverse = True
            field = field[1:]
        else:
            reverse = False

        data = sorted(data, key=lambda book: dict(book).get(field), reverse=reverse)

    if "limit" in args:
        value = int(args.get("limit"))

        data = data[:value]

    if "take" in args and "page" in args:
        page_size = int(args.get("take"))
        page_num = int(args.get("page"))

        data = [data[i:i + page_size] for i in range(0, len(data), page_size)][page_num]

    has_not_deleted = any(book for book in data if not book.deleted)
    return render_template("home.html", books=data, has_not_deleted=has_not_deleted)


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
