from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import psycopg2



app = Flask(__name__)
con = psycopg2.connect(database="payroll", user="postgres", password="emerus2705", host="127.0.0.1", port="5432")
cursor = con.cursor()

app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:emerus2705@localhost/payroll'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'Radnici'
    id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(30))
    LastName = db.Column(db.String(30))
    Satnica = db.Column(db.Float)
   

    def __init__(self, id, FirstName, LastName, Satnica):
        self.id = id
        self.FirstName = FirstName
        self.LastName = LastName
        self.Satnica = Satnica
       


@app.route('/')
def index():
    return render_template('Login.html')


@app.route('/login', methods=['Get','POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'emerus159':
            return render_template("dodajRadnika.html")
        else:
            error = 'niste ovlašteni koristiti ovu značajku'
            return render_template('Login.html', error=error)


@app.route('/submit_noviRadnik', methods=['POST'])
def submitOdrzavanje():
    if request.method == 'POST':
        id = request.form["id"]
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        Satnica = request.form['Satnica']
        # print(customer, dealer, rating, comments)
        # adding here an if statement to see is it it or odrzavanje
        # when "it" make a query to see just it stuff and vica versa
        if id == '' or firstName == '' or lastName == "" or Satnica == "":
            return render_template('dodajRadnika.html', message='Molim vas popunite obavezna polja')
        data = Feedback(id, firstName, lastName, Satnica)
        db.session.add(data)
        db.session.commit()
        # send_mail(customer, dealer, rating, comments)
        return render_template('success.html')




if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)