from flask import Flask
from flask import request, url_for, redirect, render_template

from crud_app.config import Config
from crud_app.models import Book

app = Flask(__name__)
app.config.from_object(Config)

books = [Book(isbn="123", name="123", author="qwerty", pages=123, year=2021, added_on="2021-03-21 12:00:00", deleted=False)]


@app.route("/create")
def create_route():
    return render_template("crud/create.html")


@app.route("/create", methods=["POST"])
def create():
    if request.method == "POST":
        form = dict(request.form)

        books.append(Book(**form))

    return redirect(url_for("create"))


@app.route("/update/<int:isbn>")
def update_route(isbn):
    try:
        entry = books[isbn]
    except IndexError:
        return render_template('404.html'), 404

    return render_template("crud/update.html", entry=entry)


@app.route("/update/<int:isbn>", methods=["POST"])
def update(isbn):
    try:
        books.pop(isbn)
    except IndexError:
        return render_template('404.html'), 404

    form = request.form
    books.append(Book(**form))


@app.route("/delete/<int:isbn>", methods=["POST"])
def delete(isbn):
    try:
        for index, book in enumerate(books):
            if book.isbn == isbn:
                books.pop(index)

        return redirect(url_for("create_route"))

    except IndexError:
        return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
