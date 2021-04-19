import datetime


class Book(object):
    isbn: str
    name: str
    author: str
    pages: int
    year: int
    added_on: datetime.datetime
    deleted: bool

    def __repr__(self):
        return '<Book: {}>'.format(self.name)
