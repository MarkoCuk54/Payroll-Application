from datetime import datetime
from datetime import date
from flask import render_template, request
from db import db, Feedback, placaTablica,izmjenaSatnice, app, con, cursor
import pandas as pd
from koficijenti import vikendPrekovremeni, smjena3, ned1i2, dan7i8, blagdan, bolovanje

#Home, Login, Edit, Delete and New Employyes routes :
@app.route('/')
def index():
    return render_template('Login.html')

@app.route("/home")
def home():
    return render_template("home.html")

@app.route('/login', methods=['Get','POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'maja' and request.form['password'] == 'emerus159':
            return render_template("home.html")
        else:
            error = 'niste ovlašteni koristiti ovu značajku'
            return render_template('Login.html', error=error)


@app.route('/dodajRadnika')
def dodajRadnik():
    return render_template("dodajRadnika.html")

@app.route('/deleteUser', methods=["POST"])
def deleteUser():
    try:
        id = request.form["id"]
        db.session.query(Feedback).filter(Feedback.id==id).delete()
        db.session.query(placaTablica).filter(placaTablica.id==id).delete()
        db.session.query(izmjenaSatnice).filter(izmjenaSatnice.id==id).delete()
        db.session.commit()
        message='Uspješno ste izbrisali zaposlenika'
        return render_template('error.html', message=message)
    except:
        message = "ID ne postoji u Bazi"
        return render_template('error.html', message=message)



@app.route('/editUser', methods=["GET", "POST"])
def editUser():
        editUser.id = request.form["idEdit"]
        if(id != ""):
            try:
                cursor.execute("SELECT * FROM radnici where  id = " + str(editUser.id))
                result = cursor.fetchall()
                return render_template('editUser.html', data=result[0])
            except:
                cursor.execute("ROLLBACK")
                con.commit()
                message = "ID ne postoji u Bazi"
                return render_template('error.html', message=message)
        else:
            cursor.execute("ROLLBACK")
            con.commit()
            message = "Id polje ne smije biti prazno"
            return render_template('error.html', message=message)

@app.route('/changeSatnica', methods=["POST"])
def changeSatnica():
        novaSatnica = request.form["satnica"]
        try:
            user = db.session.query(Feedback).filter(Feedback.id == editUser.id).one()
            user.Satnica = novaSatnica
            izmjena = db.session.query(izmjenaSatnice).filter(izmjenaSatnice.id == editUser.id).one()
            izmjena.izmjena = novaSatnica
            izmjena.datum =  datetime.today().strftime('%d-%m-%Y')
            db.session.commit()
            message = "Uspješno ste promijenili satnicu."
            return render_template('error.html', message=message)
        except:
            message = "Satnica je u pogrešnom formatu"
            return render_template('error.html', message=message)

@app.route('/changeOdjel', methods=["POST"])
def changeOdjel():
        noviOdjel = request.form["odjel"]
        try:
            user = db.session.query(Feedback).filter(Feedback.id == editUser.id).one()
            user.Odjel = noviOdjel
            db.session.commit()
            message = "Uspješno ste promijenili odjel."
            return render_template('error.html', message=message)
        except:
            message = "Satnica je u odjel formatu"
            return render_template('error.html', message=message)


@app.route('/povijestDizanje', methods=["POST"])
def povijestDizanje():
        try:
            id = request.form["idPovijest"]
            cursor.execute("SELECT radnici.id, radnici.firstname, radnici.lastname, izmjena.izmjena , izmjena.datum FROM radnici INNER JOIN izmjena ON radnici.id = izmjena.id where izmjena.id = " + str(id))
            result = cursor.fetchall()
            return render_template('povijestDizanje.html', data=result[0])
        except:
            cursor.execute("ROLLBACK")
            con.commit()
            return render_template('error.html', message='ID ne postoji')



@app.route('/submit_noviRadnik', methods=['POST'])
def submitNoviRadnik():
    if request.method == 'POST':
        id = request.form["id"]
        firstname = request.form['firstName']
        lastname = request.form['lastName']
        Satnica = request.form['Satnica']
        Odjel = request.form["Odjel"]
        Opis = request.form["Opis"]
        JMBG = request.form["jmbg"]
        kilometre = request.form["kilometre"]
        date = datetime.today().strftime('%d-%m-%Y')
        if id == '' or firstname == '' or lastname == "" or Satnica == "":
            return render_template('dodajRadnika.html', message='Molim vas popunite obavezna polja')
        try:
            data2 = izmjenaSatnice(id, Satnica, date)
            data1 = placaTablica(id, firstname, lastname,"0 ","0 ","0 ","0 ","0 ","0 ","0 ","0 ","0 ","0 ","0 ","0 ")
            data = Feedback(id, firstname, lastname, Satnica,Odjel, Opis, JMBG, kilometre)
            db.session.add(data)
            db.session.add(data1)
            db.session.add(data2)
            db.session.commit()
            return render_template('success.html')
        except:
            cursor.execute("ROLLBACK")
            con.commit()
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


#Calculator routes :

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
        prekovremeni = request.form["prekovremeni"]
        radNed = request.form["radNed"]
        prekovremeniVikend = request.form["prekovremeniVikendom"]
        blagdanSati = request.form["blagdan"]
        bolovanjeSati = request.form["bolovanje"]
        bonus = request.form["bonus"]
        gorivoCijena = request.form["gorivoCijena"]
        cursor.execute("SELECT * FROM radnici where  id = " + str(id))
        result = cursor.fetchall()
        satnica = (result[0][3])
        kilometre = (result[0][7])
        placa = (float(satnica) * int(sati)) + (int(nocni) * (float(satnica)* smjena3)) + (int(prekovremeni) * float(satnica)) + (int(radNed) * float(satnica) * ned1i2 )  + (float(satnica) * int(prekovremeniVikend) * vikendPrekovremeni) + (float(satnica) * int(blagdanSati) * blagdan) + (float(satnica) * int(bolovanjeSati) * bolovanje) + int(bonus) +  (((float(gorivoCijena) * 22 * 6.6) * (float[kilometre] / 100)))
        placa = str(round(placa, 2))
        rezName = result[0][1]
        rezLastName = result[0][2]
        sql_update_query = "Update placamjesecna set " + mjesec +" = %s where id = %s"
        cursor.execute(sql_update_query, (placa, id))
        con.commit()
        return render_template("kalkulator.html", data = placa, firstName = rezName, lastName = rezLastName )
    except:
        cursor.execute("ROLLBACK")
        con.commit()
        return render_template('error.html', message='Ovaj Radnik ne postoji u bazi')

#Excel file routes :

@app.route("/excelFile")
def excelFile():
        satiIndex = 0
        # Ovdje imam sve IDove:
        ids = []
        # Ovdje sve sate rasporedeno isto kao Idove:
        sati = []
        smjena3list = []
        prekovremeni1i2list = []
        prvaIdruganedlist = []
        sedmiI8danlist = []
        prekovremeniVikendlist = []
        blagdanlist = []
        bolovanjeList = []
        bonusList = []
        # Ovdje izracunatre place takodjer po Idove:
        place = []
        imena = []
        prezimena = []
        jmbgs= []
        cijenaGoriva = []
        try:
            excelFile = pd.read_excel (r'C:\Users\Marko\Documents\platnaLista.xlsx')
            for index, row in excelFile.head(n = 50).iterrows():
                    ids.append(row["id"])
                    sati.append(row["sati"])
                    smjena3list.append(row["3.smjena"])
                    prekovremeni1i2list.append(row["prekovremeni 1 i 2"])
                    prvaIdruganedlist.append(row["1 i 2 ned"])
                    sedmiI8danlist.append(row["7.8 dan"])
                    prekovremeniVikendlist.append(row["prekovremeni vikend"])
                    blagdanlist.append(row["blagdan"])
                    bolovanjeList.append(row["bolovanje"])
                    bonusList.append(row["bonus"])
                    cijenaGoriva.append(row["cijenaGoriva"])
            for id in ids:
                    cursor.execute("SELECT * FROM radnici where  id = " + str(id))
                    result = cursor.fetchall()
                    satnica = (result[0][3])
                    ime = result[0][1]
                    prezime = result[0][2]
                    jmbg = result[0][6]
                    kilometre = result[0][7]
                    danaZaGorivo = (sati[satiIndex] + smjena3list[satiIndex] + prekovremeni1i2list[satiIndex] + prvaIdruganedlist[satiIndex] + sedmiI8danlist[satiIndex] + prekovremeniVikendlist[satiIndex] + blagdanlist[satiIndex]) / 8
                    gorivo = float(cijenaGoriva[satiIndex]) * danaZaGorivo * 6.6 * float(kilometre) / 100
                    gorivo = round(gorivo,2)
                    placa = (float(satnica) * int(sati[satiIndex])) + (float(satnica) * int(smjena3list[satiIndex]) * smjena3) + (float(satnica) * int(prekovremeni1i2list[satiIndex])) + (float(satnica) * int(prvaIdruganedlist[satiIndex]) * ned1i2 ) + (float(satnica) * int(sedmiI8danlist[satiIndex]) * dan7i8) + (float(satnica) * int(prekovremeniVikendlist[satiIndex]) * vikendPrekovremeni) + (float(satnica) * int(blagdanlist[satiIndex]) * blagdan) + (float(satnica) * int(bolovanjeList[satiIndex]) * bolovanje) + int(bonusList[satiIndex]) + gorivo
                    placa = str(round(placa, 2))
                    place.append(placa)
                    imena.append(ime)
                    prezimena.append(prezime)
                    jmbgs.append(jmbg)
                    satiIndex += 1
            return render_template("excelFile.html", dataIme = imena, dataPrezime = prezimena, dataPlaca = place, dataId = ids, dataJmbg = jmbgs, dataGorivo = gorivo)
        except:
            cursor.execute("ROLLBACK")
            con.commit()
            return render_template("error.html", message = "Nest sa Excel Filom nije uredu!")

@app.route("/excelMjesec", methods=["GET", "POST"])
def excelMjesec():
        satiIndex = 0
        # Ovdje imam sve IDove:
        ids = []
        # Ovdje sve sate rasporedeno isto kao Idove:
        sati = []
        smjena3list = []
        prekovremeni1i2list = []
        prvaIdruganedlist = []
        sedmiI8danlist = []
        prekovremeniVikendlist = []
        blagdanlist = []
        bolovanjeList = []
        bonusList = []
        # Ovdje izracunatre place takodjer po Idove:
        place = []
        cijenaGoriva = []
        try:
            mjesec = request.form["mjesec"]
            excelFile = pd.read_excel (r'C:\Users\Marko\Documents\platnaLista.xlsx')
            for index, row in excelFile.head(n = 50).iterrows():
                ids.append(row["id"])
                sati.append(row["sati"])
                smjena3list.append(row["3.smjena"])
                prekovremeni1i2list.append(row["prekovremeni 1 i 2"])
                prvaIdruganedlist.append(row["1 i 2 ned"])
                sedmiI8danlist.append(row["7.8 dan"])
                prekovremeniVikendlist.append(row["prekovremeni vikend"])
                blagdanlist.append(row["blagdan"])
                bolovanjeList.append(row["bolovanje"])
                bonusList.append(row["bonus"])
                cijenaGoriva.append(row["cijenaGoriva"])
            for id in ids:
                cursor.execute("SELECT * FROM radnici where  id = " + str(id))
                result = cursor.fetchall()
                satnica = (result[0][3])
                kilometre = result[0][7]
                danaZaGorivo = (sati[satiIndex] + smjena3list[satiIndex] + prekovremeni1i2list[satiIndex] + prvaIdruganedlist[satiIndex] + sedmiI8danlist[satiIndex] + prekovremeniVikendlist[satiIndex] + blagdanlist[satiIndex]) / 8
                gorivo = float(cijenaGoriva[satiIndex]) * danaZaGorivo * 6.6 * float(kilometre) / 100
                gorivo = round(gorivo,2)
                placa = (float(satnica) * int(sati[satiIndex])) + (float(satnica) * int(smjena3list[satiIndex]) * smjena3) + (float(satnica) * int(prekovremeni1i2list[satiIndex])) + (float(satnica) * int(prvaIdruganedlist[satiIndex]) * ned1i2 ) + (float(satnica) * int(sedmiI8danlist[satiIndex]) * dan7i8) + (float(satnica) * int(prekovremeniVikendlist[satiIndex]) * vikendPrekovremeni) + (float(satnica) * int(blagdanlist[satiIndex]) * blagdan) + (float(satnica) * int(bolovanjeList[satiIndex]) * bolovanje) + int(bonusList[satiIndex]) + gorivo
                placa = str(round(placa, 2))
                place.append(placa)
                sql_update_query = "Update placamjesecna set " + mjesec +" = %s where id = %s"
                cursor.execute(sql_update_query, (placa, id))
                con.commit()
                satiIndex += 1
            return render_template("error.html", message = "Uspješno spremljeno u povijest primanja.")
        except:
            cursor.execute("ROLLBACK")
            con.commit()
            return render_template("error.html", message = "Molim vas odaberite mjesec!")

#Upload routes :

@app.route('/upload')
def upload_file():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_files():
   if request.method == 'POST':
# if statement to see if the user upload a valid file ( not empty submit)
      if request.files["file"]:
        f = request.files['file']
        f.filename = "platnalista.xlsx"  #some custom file name that you want
        f.save("./Uploads/"+f.filename) # path where to save the file
        return render_template("error.html", message = "Sada možete koristiti Excel datoteku.")
      else:
        return render_template("error.html", message = "Ovo nije valjana Excel datoteka")

@app.route('/toexcel')
def to_excel():
    webpage_url = "http://192.168.0.113:5000/povijestPrimanja?"
# Create a Pandas dataframe using the table data.
    table_data = pd.read_html(webpage_url)[0]
# Store the above-created dataframe as an excel file using the to_excel() function 
    table_data.to_excel("table_data.xlsx", index=False)
    return render_template("error.html", message = "Excel spreman.")




if __name__ == '__main__':
   app.run(host='0.0.0.0', port = 5000 )
