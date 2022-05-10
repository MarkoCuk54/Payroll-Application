from flask import render_template, request
from db import db, Feedback, placaTablica, app, con, cursor
import pandas as pd
# var for the koficijent:

smjena3 = 1.5
ned1i2 = 1.15
dan7i8 = 1.5
vikendPrekovremeni = 1.5
blagdan = 1.3
bolovanje = 0.8

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