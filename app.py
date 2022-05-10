from flask import render_template, request
from db import db, Feedback, placaTablica, app, con, cursor
import pandas as pd
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage


# var for the koficijent:

smjena3 = 1.5
ned1i2 = 1.15
dan7i8 = 1.5
vikendPrekovremeni = 1.5
blagdan = 1.3
bolovanje = 0.8

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
        if request.form['username'] == 'admin' and request.form['password'] == 'emerus159':
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
        db.session.commit()        
        message='Uspješno ste izbrisali zaposlenika'
        return render_template('error.html', message=message)
    except:
        message = "ID ne postoji u Bazi"
        return render_template('error.html', message=message)



@app.route('/editUser', methods=["GET", "POST"])
def editUser():
        id = request.form["idEdit"]
        if(id != ""):
            cursor.execute("SELECT * FROM radnici where  id = " + str(id))
            result = cursor.fetchall()
            return render_template('editUser.html', data=result[0])
        else:
            message = "ID ne postoji u Bazi"
            return render_template('error.html', message=message)
            
 


@app.route('/submit_noviRadnik', methods=['POST'])
def submitNoviRadnik():
    if request.method == 'POST':
        id = request.form["id"]
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        Satnica = request.form['Satnica']
        Odjel = request.form["Odjel"]
        Opis = request.form["Opis"]
        JMBG = request.form["jmbg"]
        if id == '' or firstName == '' or lastName == "" or Satnica == "":
            return render_template('dodajRadnika.html', message='Molim vas popunite obavezna polja')
        try:
            data1 = placaTablica(id, firstName, lastName,"0 ","0 ","0 ","0 ","0 ","0 ","0 ","0 ","0 ","0 ","0 ","0 ")
            data = Feedback(id, firstName, lastName, Satnica,Odjel, Opis, JMBG)
            db.session.add(data)
            db.session.add(data1)
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
        cursor.execute("SELECT * FROM radnici where  id = " + str(id))
        result = cursor.fetchall()
        satnica = (result[0][3])
        placa = (float(satnica) * int(sati)) + (int(nocni) * (float(satnica)* smjena3)) + (int(prekovremeni) * float(satnica)) + (int(radNed) * float(satnica) * ned1i2 )  + (float(satnica) * int(prekovremeniVikend) * vikendPrekovremeni) + (float(satnica) * int(blagdanSati) * blagdan) + (float(satnica) * int(bolovanjeSati) * bolovanje) + int(bonus)
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
            for id in ids:
                cursor.execute("SELECT * FROM radnici where  id = " + str(id))
                result = cursor.fetchall()
                satnica = (result[0][3])
                ime = result[0][1]
                prezime = result[0][2]
                jmbg = result[0][6]
                placa = (float(satnica) * int(sati[satiIndex])) + (float(satnica) * int(smjena3list[satiIndex]) * smjena3) + (float(satnica) * int(prekovremeni1i2list[satiIndex])) + (float(satnica) * int(prvaIdruganedlist[satiIndex]) * ned1i2 ) + (float(satnica) * int(sedmiI8danlist[satiIndex]) * dan7i8) + (float(satnica) * int(prekovremeniVikendlist[satiIndex]) * vikendPrekovremeni) + (float(satnica) * int(blagdanlist[satiIndex]) * blagdan) + (float(satnica) * int(bolovanjeList[satiIndex]) * bolovanje) + int(bonusList[satiIndex])
                placa = str(round(placa, 2))
                place.append(placa)
                imena.append(ime)
                prezimena.append(prezime)
                jmbgs.append(jmbg)
                satiIndex += 1
            return render_template("excelFile.html", dataIme = imena, dataPrezime = prezimena, dataPlaca = place, dataId = ids, dataJmbg = jmbgs)
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
            for id in ids:
                cursor.execute("SELECT * FROM radnici where  id = " + str(id))
                result = cursor.fetchall()
                satnica = (result[0][3])
                placa = (float(satnica) * int(sati[satiIndex])) + (float(satnica) * int(smjena3list[satiIndex]) * smjena3) + (float(satnica) * int(prekovremeni1i2list[satiIndex])) + (float(satnica) * int(prvaIdruganedlist[satiIndex]) * ned1i2 ) + (float(satnica) * int(sedmiI8danlist[satiIndex]) * dan7i8) + (float(satnica) * int(prekovremeniVikendlist[satiIndex]) * vikendPrekovremeni) + (float(satnica) * int(blagdanlist[satiIndex]) * blagdan) + (float(satnica) * int(bolovanjeList[satiIndex]) * bolovanje) + int(bonusList[satiIndex])
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





if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)