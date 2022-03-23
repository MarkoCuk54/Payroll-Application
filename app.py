from distutils.command.config import config
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from numpy import rint
from db import db, Feedback, placaTablica, app, con, cursor
import pandas as pd


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
            data1 = placaTablica(id, firstName, lastName,"0 ","0 ","0 ","0 ","0 ","0 ","0 ","0 ","0 ","0 ","0 ","0 ")
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

@app.route("/excelFile")
def excelFile():
    satiIndex = 0
    # Ovdje imam sve IDove:
    ids = []
    # Ovdje sve sate rasporedeno isto kao Idove:
    sati = []
    # Ovdje izracunatre place takodjer po Idove:
    place = []
    imena = []
    prezimena = []
    excelFile = pd.read_excel (r'C:\Users\Marko\Documents\test.xlsx')
    for index, row in excelFile.head(n = 50).iterrows():
        ids.append(row["id"])
        sati.append(row["sati"])
    for id in ids:
        cursor.execute("SELECT * FROM radnici where  id = " + str(id))
        result = cursor.fetchall()
        satnica = (result[0][3])
        ime = result[0][1]
        prezime = result[0][2]
        placa = (float(satnica) * int(sati[satiIndex]))
        placa = str(round(placa, 2))
        place.append(placa)
        imena.append(ime)
        prezimena.append(prezime)
        satiIndex += 1
   
    return render_template("excelFile.html")

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)