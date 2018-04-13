from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from send_email import send_email
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:trishtrish@localhost/Book_Collector'
db = SQLAlchemy(app)

class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(120))
    book=db.Column(db.String(120))
    category=db.Column(db.String(40))

    def __init__(self, email, book, category):
        self.email=email
        self.book=book
        self.category=category

@app.route("/") # by not specifying type of REST API method (i.e. get, put, delete, etc) we automatically get a "get" method
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method=='POST':
        emailvar=request.form["email_name"]
        bookvar=request.form["book_name"]
        entryCategory=request.form["dropdown1"]
        exitCategory=request.form["dropdown2"]
        if db.session.query(Data).filter(Data.book == bookvar).count()== 0:
            #selecting random book from requested category to reccommend.
            list = []
            for book in db.session.query(Data.book).filter_by(category = exitCategory):
                list.append(book)
            book_reccomendation = random.choice(list)
            print(book_reccomendation)

            data=Data(emailvar,bookvar,entryCategory)
            db.session.add(data)
            db.session.commit()
            book_reccomendation = str(book_reccomendation)[2:-3]
            send_email(emailvar, book_reccomendation, exitCategory)
            return render_template("success.html")
        return render_template('index.html', text="Seems like we have that book reccomendation already!")

if __name__== '__main__':
    app.debug = True
    app.run()