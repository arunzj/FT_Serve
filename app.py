from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '04812340484'
app.config['MYSQL_DB'] = 'ros'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        tableno=request.form['tableno']
        code=request.form['code']
        cur=mysql.connection.cursor()
        result = cur.execute("SELECT * FROM tables WHERE table_no= %s ",[tableno])
        

        if result > 0:
            record = cur.fetchone()
            dcode = record['code']
            code=long(code)
            if dcode == code:
                msg="<h1>success</h1>"
                return render_template('msg.html',msg=msg)
            else:
                msg = "<h1>Wrong Password...!</h1>"
                return render_template('msg.html',msg=msg)



            

    return render_template('index.html')



#main
if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
