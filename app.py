from flask import render_template
from db import db, Feedback, placaTablica, app, con, cursor
import views

app.add_url_rule('/', view_func=views.index)




if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)