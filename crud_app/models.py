import datetime

from pydantic import BaseModel


class Book(BaseModel):

    isbn: str
    name: str
    author: str
    pages: int
    year: int
    added_on: datetime.datetime
    deleted: bool
    status: dict

    def __repr__(self):
        return "<Book: {}>".format(self.name)
