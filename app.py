from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from send_email import send_email
import random
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgres://xayfvicmejgdbs:32d7ba9e5145a2c9f244690efeb8111c3c9b85e5a9bcc11633ddebca60fc824d@ec2-54-163-240-54.compute-1.amazonaws.com:5432/da0pjh6v6g070?sslmode=require' #sslmode = require is to access database
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
            data=Data(emailvar,bookvar,entryCategory)
            db.session.add(data)
            db.session.commit()
            book_reccomendation = str(book_reccomendation)[2:-3]
            send_email(emailvar, book_reccomendation, exitCategory)
            return render_template("success.html")
        return render_template('index.html', text="Seems like we have that book reccomendation already!")

if __name__== '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
