# Import all of the libraries our application depend on
from flask import Flask, render_template, redirect, url_for, jsonify, request
from peewee import *
import datetime, io, csv

# create a new Flask application
app = Flask(__name__)

# # make a connection to our database
db = SqliteDatabase('books.db')

# This is your standard "Hello World"
@app.route('/')
def hello():
    # return the text "Hello world!" to the browser
    return "Hello world!"

# # Show the form to create new book
@app.route('/book/new')
def new_book():
    return render_template('new_book.html')

# # Create a new book with the data submitted from the web form, and save it in the database
# # If a form is not submitted (ie, it is a GET request), redirect user to the new book form
@app.route('/book', methods=['POST', 'GET'])
def submit_book():
    # If the HTTP request method is GET, redirect to the new book form
    if request.method == 'GET':
        return redirect(url_for('new_book'))

    # Gather the book data from the submitted form
    book_title = request.form['form-title']
    book_cover_image_url = request.form['form-cover-image']
    book_description = request.form['form-description']
    book_reason = request.form['form-reason']
    # Record the time the form was submitted using datetime.now() method
    book_timestamp = datetime.datetime.now()

    # Create a new "Book" object using the submitted data
    new_book = Book(title=book_title, cover=book_cover_image_url, description=book_description, reason=book_reason, created_at=book_timestamp)
    # Save the new "Book" object to the database
    new_book.save()

    # Redirect to the details page for the newly submitted book
    return redirect(url_for('show_book', book_id = new_book.id))


# # Retrieve a given book (by ID) from the database, and show a "full record" page for that book.
@app.route('/book/<book_id>')
def show_book(book_id):
    # Query the database for the book by its ID
    selected_book = Book.get(Book.id == book_id)

    # Render a page using the data from that book
    return render_template('book.html', book=selected_book)


# # Retrieve all books in descending order by submission time, and show a list view of them.
@app.route('/books')
def books():
    # Query the database for all books, ordering by the book ID in descending order
    all_books = Book.select().order_by(Book.id.desc())

    # Using that data, render a page that shows the books in a list
    return render_template('books.html', books=all_books)


# # Retrieve all books similarly to the above route, but return as a CSV list instead of HTML page.
@app.route('/books_csv')
def book_csv():
    # Instantiate a StringIO object to capture the data we'll pass to the CSV writer.
    si = io.StringIO()

    # Write the header lines
    si.writelines(['# of Years on Top 10 List,Title,Reason,Link,Cover\n', 'number,string,string,string,string\n'])

    # Instantiate a CSV writer that uses the above StringIO object
    cw = csv.writer(si)

    # Query the database for all books, ordering by the book ID in descending order
    all_books = Book.select().order_by(Book.id.desc())
    # The CSV writer knows how to write Python "tuples", so pass the data we got from the database in tuples format.
    # The resulting data from the CSVWriter will end up in our StringIO object called "si"
    cw.writerows(all_books.tuples())
    # Return the value of "si", which will be the database data converted into CSV format
    return si.getvalue()


# # This class represents a book, and tells our application about the structure of our database, including what types of data to expect from each field.
class Book(Model):
    title = CharField()
    description = CharField()
    reason = CharField()
    cover = CharField()
    created_at = DateField()

    # This is metadata tying this class to the database we defined earlier in this file
    class Meta:
        database = db

# This if statement is Python boilerplate saying "if this script is run from the command line, and not imported as a library"
if __name__ == '__main__':
    # run the application in debug mode, and on port 3000
    app.run(debug=True, port=3000)
