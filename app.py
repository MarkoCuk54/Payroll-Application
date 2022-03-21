from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import pandas as pd

df = pd.read_excel (r'C:\Users\Marko\Documents\test.xlsx')
print (df)

app = Flask(__name__)
con = psycopg2.connect(database="payroll", user="postgres", password="emerus2705", host="127.0.0.1", port="5432")
cursor = con.cursor()

app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:emerus2705@localhost/payroll'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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

@app.route('/')
def index():
    return render_template('Login.html')

@app.route("/home")
def home():
    return render_template("home.html")

@app.route('/login', methods=['Get','POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'emerus159':
            return render_template("home.html")
        else:
            error = 'niste ovlašteni koristiti ovu značajku'
            return render_template('Login.html', error=error)


@app.route('/dodajRadnika')
def dodajRadnik():
    return render_template("dodajRadnika.html")


@app.route('/submit_noviRadnik', methods=['POST'])
def submitNoviRadnik():
    if request.method == 'POST':
        id = request.form["id"]
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        Satnica = request.form['Satnica']
        Odjel = request.form["Odjel"]
        Opis = request.form["Opis"]
        if id == '' or firstName == '' or lastName == "" or Satnica == "":
            return render_template('dodajRadnika.html', message='Molim vas popunite obavezna polja')
        try:
            data1 = placaTablica(id, firstName, lastName,"NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN","NaN")
            data = Feedback(id, firstName, lastName, Satnica,Odjel, Opis)
            db.session.add(data)
            db.session.add(data1)
            db.session.commit()
            return render_template('success.html')
        except:
            return render_template('dodajRadnika.html', message='Ovaj Radnik vec postoji u bazi')

        
@app.route('/sviRadnici', methods=['GET'])
def sviRadnici():
        cursor.execute("SELECT * FROM radnici ORDER BY id ")
        result = cursor.fetchall()
        return render_template("sviRadnici.html", data=result)
        

@app.route("/povijestPrimanja", methods=["GET"])
def povijestPrimanja():
        cursor.execute("SELECT * FROM placamjesecna ORDER BY id ")
        result = cursor.fetchall()
        return render_template("povijestPrimanja.html", data=result)


@app.route("/kalkulator", methods=["GET", "POST"])
def renderKalkulator():
        return render_template("kalkulator.html")

@app.route("/kalkulatorSubmit", methods=["GET", "POST"])
def kalkulator():
    try:
        id = request.form["id"]
        sati = request.form["sati"]
        nocni = request.form["nocni"]
        mjesec = request.form["mjesec"]
        cursor.execute("SELECT * FROM radnici where  id = " + str(id))
        result = cursor.fetchall()
        satnica = (result[0][3])
        placa = (float(satnica) * int(sati)) + int(nocni) * (float(satnica)* 1.3)
        placa = str(round(placa, 2))
        rezName = result[0][1]
        rezLastName = result[0][2]
        sql_update_query = "Update placamjesecna set " + mjesec +" = %s where id = %s"
        cursor.execute(sql_update_query, (placa, id))
        con.commit()
        return render_template("kalkulator.html", data = placa, firstName = rezName, lastName = rezLastName )
    except:
         return render_template('kalkulator.html', message='Ovaj Radnik ne postoji u bazi')

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)