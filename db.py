from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)
con = psycopg2.connect(database="payroll", user="postgres", password="emerus2705", host="127.0.0.1", port="5432")
cursor = con.cursor()
db = SQLAlchemy(app)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:emerus2705@localhost/payroll'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Feedback(db.Model):
    __tablename__ = 'radnici'
    id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(30))
    LastName = db.Column(db.String(30))
    Satnica = db.Column(db.Float)
    Odjel = db.Column(db.String(30))
    Opis = db.Column(db.Text())

    def __init__(self, id, FirstName, LastName, Satnica, Odjel, Opis):
        self.id = id
        self.FirstName = FirstName
        self.LastName = LastName
        self.Satnica = Satnica
        self.Odjel = Odjel
        self.Opis = Opis


class placaTablica(db.Model):
    __tablename__ = 'placamjesecna'
    id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(30))
    LastName = db.Column(db.String(30))
    siječanj = db.Column(db.String(30))
    veljača  = db.Column(db.String(30))
    ožujak  = db.Column(db.String(30))
    travanj  = db.Column(db.String(30))
    svibanj  = db.Column(db.String(30))
    lipanj  = db.Column(db.String(30))
    srpanj  = db.Column(db.String(30))
    kolovoz  = db.Column(db.String(30))
    rujan  = db.Column(db.String(30))
    listopad  = db.Column(db.String(30))
    studeni  = db.Column(db.String(30))
    prosinac  = db.Column(db.String(30))

    def __init__(self, id, FirstName, LastName, siječanj, veljača, ožujak, travanj, svibanj, lipanj, srpanj, kolovoz, rujan, listopad, studeni, prosinac):
        self.id = id
        self.FirstName = FirstName
        self.LastName = LastName
        self.siječanj = siječanj
        self.veljača = veljača
        self.ožujak = ožujak
        self.travanj = travanj
        self.svibanj = svibanj
        self.lipanj = lipanj
        self.srpanj = srpanj
        self.kolovoz = kolovoz
        self.rujan = rujan
        self.listopad = listopad
        self.studeni = studeni
        self.prosinac = prosinac