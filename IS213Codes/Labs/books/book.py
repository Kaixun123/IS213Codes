from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#'mysql+mysqlconnector://jason:mary@localhost:3306/asset' - jason:mary (username:password) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = 'book'


    isbn13 = db.Column(db.String(13), primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    availability = db.Column(db.Integer)


    def __init__(self, isbn13, title, price, availability):
        self.isbn13 = isbn13
        self.title = title
        self.price = price
        self.availability = availability


    def json(self):
        return {"isbn13": self.isbn13, "title": self.title, "price": self.price, "availability": self.availability}

# default method is GET

@app.route("/book")
def get_all():
    booklist = db.session.scalars(db.select(Book)).all()
    if len(booklist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "books": [book.json() for book in booklist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no books."
        }
    ), 404

@app.route("/book/<string:isbn13>")
def find_by_isbn13(isbn13):
    book = db.session.scalars(
    db.select(Book).filter_by(isbn13=isbn13).
    	limit(1)).first()

    if book:
        return jsonify(
            {
                "code": 200,
                "data": book.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Book not found."
        }
    ), 404

@app.route("/book/<string:isbn13>", methods=['POST'])
def create_book(isbn13):
    if (db.session.scalars(
      db.select(Book).filter_by(isbn13=isbn13).
      limit(1)
      ).first()
      ):
        return jsonify(
            {
                "code": 400,
                "data": {
                    "isbn13": isbn13
                },
                "message": "Book already exists."
            }
        ), 400

    data = request.get_json()
    book = Book(isbn13, **data)
    try:
        db.session.add(book)
        db.session.commit()
    except:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "isbn13": isbn13
                },
                "message": "An error occurred creating the book."
            }
        ), 500

    return jsonify( 
        {
         "code": 201,
        "data": book.json()
        }
    ), 201

@app.route("/book/outofstock")
def get_unavailable_books():
    book = db.session.scalars(db.select(Book).filter_by(availability=0)).first()
    if book:
        return jsonify(
            {
                "code": 200,
                "data": book.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Book not found."
        }
    ), 404

@app.route("/book/popularbooks")
def get_popular_books():
    book = db.session.query(Book).filter(Book.availability > 10).all()
    if book:
        return jsonify(
            {
                "code": 200,
                "data": [b.json() for b in book]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Book not found."
        }
    ), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)