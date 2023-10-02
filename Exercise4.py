from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Assuming you have already created the database and tables

engine = create_engine('sqlite:///Library.db')  # Change this to your database URL
Session = sessionmaker(bind=engine)


def add_book(session):
    book = Books(Title=input("Enter the book title: "), Author=input("Enter the book author: "),
                 ISBN=input("Enter the book ISBN: "), Status='Available')  # Default status is Available
    session.add(book)
    session.commit()
    print("Book added successfully!")


def find_book_by_id(session):
    book_id = input("Enter the BookID: ")
    book = session.query(Books).filter_by(BookID=book_id).first()
    if book is None:
        print("Book not found!")
        return
    print("Book Title: ", book.Title)
    print("Book Author: ", book.Author)
    print("Book ISBN: ", book.ISBN)
    print("Book Status: ", book.Status)
    if book.Reservations:  # Check if the book has reservations
        print("User who has reserved this book: ", book.Reservations[0].UserID)  # Only showing the first reservation


def find_book_status(session):
    book_id = input("Enter the BookID, Title, UserID, or ReservationID: ")
    if book_id.lower()[:2] == 'lb':  # Check if the input is a BookID
        book = session.query(Books).filter_by(BookID=book_id[2:]).first()
    elif book_id.lower()[:2] == 'lu':  # Check if the input is a UserID
        book = session.query(Reservations).filter_by(UserID=book_id[2:]).first()
    elif book_id.lower()[:2] == 'lr':  # Check if the input is a ReservationID
        book = session.query(Reservations).filter_by(ReservationID=book_id[2:]).first()
    else:  # Assume the input is a Title
        book = session.query(Books).filter_by(Title=book_id).first()
    if book is None:
        print("Book or reservation not found!")
        return
    if isinstance(book, Books):  # Check if the result is a book or a reservation
        print("Book Title: ", book.Title)
        print("Book Author: ", book.Author)
        print("Book ISBN: ", book.ISBN)
        print("Book Status: ", book.Status)
        if isinstance(book, Reservations):  # Check if the result is a reservation
            print("User who has reserved this book: ", book.UserID)
        else:  # Assume the result is a book
            print("This book is not reserved.")
    else:  # Assume the result is a reservation
        print("Reservation ID: ", book.ReservationID)
        print("User who has reserved this book: ", book.UserID)
        print("Date of reservation: ", book.ReservationDate)