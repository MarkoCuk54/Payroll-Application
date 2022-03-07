from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import psycopg2



app = Flask(__name__)
con = psycopg2.connect(database="payroll", user="postgres", password="emerus2705", host="127.0.0.1", port="5432")
cursor = con.cursor()

app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:emerus2705@localhost/lexus'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
