from flask import Flask, render_template, redirect, url_for, jsonify, request
from peewee import *
import datetime, io, csv

app = Flask(__name__)
db = SqliteDatabase('books.db')

@app.route('/')
def hello():
    return "Hello world!"

@app.route('/book/new')
def new_book():
    return render_template('new_book.html')

@app.route('/book', methods=['POST', 'GET'])
def submit_book():
    if request.method == 'GET':
        return redirect(url_for('new_book'))

    book_title = request.form['form-title']
    book_cover_image_url = request.form['form-cover-image']
    book_description = request.form['form-description']
    book_reason = request.form['form-reason']
    book_timestamp = datetime.datetime.now()

    new_book = Book(title=book_title, cover=book_cover_image_url, description=book_description, reason=book_reason, created_at=book_timestamp)
    new_book.save()

    return redirect(url_for('get_book', book_id = new_book.id))

@app.route('/book/<book_id>')
def get_book(book_id):
    selected_book = Book.get(Book.id == book_id)

    return render_template('book.html', book=selected_book)

@app.route('/books')
def books():
    all_books = Book.select().order_by(Book.id.desc())

    return render_template('books.html', books=all_books)

@app.route('/books_csv')
def book_csv():
    si = io.StringIO()
    cw = csv.writer(si)

    all_books = Book.select().order_by(Book.id.desc())
    cw.writerows(all_books.tuples())
    return si.getvalue()


class Book(Model):
    title = CharField()
    description = CharField()
    reason = CharField()
    cover = CharField()
    created_at = DateField()

    class Meta:
        database = db

if __name__ == '__main__':
    app.run(debug=True, port=3000)
