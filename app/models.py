import datetime


class Book(object):

    def __init__(self, isbn, name, author, pages, year, added_on, deleted):
        self.isbn: str = isbn
        self.name: str = name
        self.author: str = author
        self.pages: int = pages
        self.year: int = year
        self.added_on: datetime.datetime = added_on
        self.deleted: bool = deleted

    def __repr__(self):
        return '<Book: {}>'.format(self.name)
