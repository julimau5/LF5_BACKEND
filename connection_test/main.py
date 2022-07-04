from flask import Flask 
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://dbeaver:dbeaver@172.16.5.15:3306/RECH_DB'
db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__="book"
    id=db.Column(db.Integer, primary_key=True)

    title=db.Column(db.String(50))
    autor = db.Column(db.String(30))
    date = db.Column(db.Date)
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    def convertToData(self):
        return {
                "title": self.title,
                "autor": self.autor,
                "date": self.date.strftime('%Y-%m-%d')
                }
db.create_all()

class GetBooks(Resource):
    def get(self):
        try:
            books = Book.query.all()
            result = db.engine.execute("SELECT * FROM book")
            for r in result:
                print(r[1])
            data = []
            for book in books:
                data.append(book.convertToData())
            return {"message" : "lets see", "data": data}
        except Exception as e:
            return {"error: ": e}


class HelloWorld(Resource):
    def get(self):
        return {"message": "Hello World"}

api.add_resource(HelloWorld, "/test")
api.add_resource(GetBooks, "/books")

if __name__ == "__main__":
    app.run(debug=True)
