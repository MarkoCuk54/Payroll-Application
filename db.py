from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)


app.debug = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:emerus2705@localhost/payroll'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gfqguxbciigqcd:b0ca30af9ed1d2deacff97ed20ed11aa4f7e361ca898f8799095dff254de11e3@ec2-3-231-82-226.compute-1.amazonaws.com:5432/d27il8v0ile7d'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



con = psycopg2.connect(database="d27il8v0ile7d", user="gfqguxbciigqcd", password="b0ca30af9ed1d2deacff97ed20ed11aa4f7e361ca898f8799095dff254de11e3", host="ec2-3-231-82-226.compute-1.amazonaws.com", port="5432")
cursor = con.cursor()
db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'radnici'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30))
    lastname = db.Column(db.String(30))
    Satnica = db.Column(db.Float)
    Odjel = db.Column(db.String(30))
    Opis = db.Column(db.Text())
    JMBG   = db.Column(db.String(30))

    def __init__(self, id, firstname, lastname,  Satnica, Odjel, Opis, JMBG):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.JMBG = JMBG
        self.Satnica = Satnica
        self.Odjel = Odjel
        self.Opis = Opis

class izmjenaSatnice(db.Model):
    __tablename__ = 'izmjena'
    id = db.Column(db.Integer, primary_key=True)
    izmjena = db.Column(db.String(30))
    datum = db.Column(db.String(30))
    def __init__(self, id, izmjena,datum):
        self.id = id
        self.izmjena = izmjena
        self.datum = datum

class placaTablica(db.Model):
    __tablename__ = 'placamjesecna'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30))
    lastname = db.Column(db.String(30))
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

    def __init__(self, id, firstname, lastname, siječanj, veljača, ožujak, travanj, svibanj, lipanj, srpanj, kolovoz, rujan, listopad, studeni, prosinac):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
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
