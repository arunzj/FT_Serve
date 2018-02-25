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
app.config['MYSQL_DB'] = 'qserve'
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
            
            if dcode == code:
                session['table_no'] = tableno
                
                return redirect(url_for('customer',id=1))
            else:
                flash('wrong password', 'danger')
                return render_template('index.html')

        else:

            flash('Invalid username or password', 'danger')
            return render_template('index.html')


            

    return render_template('index.html')

'''@app.route('/customer',methods=['GET','POST'])
def customer():
    cur = mysql.connection.cursor()
    result=cur.execute("select * from items")
    items=cur.fetchall()
    return render_template('customer/category1.html',items=items)'''

#categories
@app.route('/customer/category/<string:id>',methods=['GET','POST'])
def customer(id):

    if int(id) == 3:
        
        return render_template('customer/category3.html')
        

    elif int(id) == 2:

        return render_template('customer/category2.html')

    else:
          
        cur = mysql.connection.cursor()
        result=cur.execute("select * from items")
        items=cur.fetchall()
        return render_template('customer/category1.html',items=items)
#main
if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
