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
    Siječanj = db.Column(db.Float)
    Veljača  = db.Column(db.Float)
    Ožujak  = db.Column(db.Float)
    Travanj  = db.Column(db.Float)
    Svibanj  = db.Column(db.Float)
    Lipanj  = db.Column(db.Float)
    Srpanj  = db.Column(db.Float)
    Kolovoz  = db.Column(db.Float)
    Rujan  = db.Column(db.Float)
    Listopad  = db.Column(db.Float)
    Studeni  = db.Column(db.Float)
    Prosinac  = db.Column(db.Float)

    def __init__(self, id, FirstName, LastName, Siječanj, Veljača, Ožujak, Travanj, Svibanj, Lipanj, Srpanj, Kolovoz, Rujan, Listopad, Studeni, Prosinac):
        self.id = id
        self.FirstName = FirstName
        self.LastName = LastName
        self.Siječanj = Siječanj
        self.Veljača = Veljača
        self.Ožujak = Ožujak
        self.Travanj = Travanj
        self.Svibanj = Svibanj
        self.Lipanj = Lipanj
        self.Srpanj = Srpanj
        self.Kolovoz = Kolovoz
        self.Rujan = Rujan
        self.Listopad = Listopad
        self.Studeni = Studeni
        self.Prosinac = Prosinac

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
            return render_template("dodajRadnika.html")
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
            data = Feedback(id, firstName, lastName, Satnica,Odjel, Opis)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')
        except:
            return render_template('dodajRadnika.html', message='Ovaj Radnik vec postoji u bazi')

        
@app.route('/sviRadnici', methods=['GET', 'POST'])
def sviRadnici():
        cursor.execute("SELECT * FROM radnici ORDER BY id ")
        result = cursor.fetchall()
        return render_template("sviRadnici.html", data=result)
        

@app.route("/povijestPrimanja", methods=["GET", "POST"])
def povijestPrimanja():
        cursor.execute("SELECT * FROM placaMjesecna ORDER BY id ")
        result = cursor.fetchall()
        return render_template("povijestPrimanja.html", data=result)




if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)