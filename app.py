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


#Login Form (Main)
@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        username=request.form['text1']
        password=request.form['password']
        cur=mysql.connection.cursor()
        result = cur.execute("SELECT * FROM tables WHERE table_no= %s ",[])
        

        if result > 0:
            record = cur.fetchone()
            dcode = record['code']
            
            if dcode == code:
                session['table_no'] = tableno
                session['customer_ID'] = 333

                return redirect(url_for('customer',id='starter'))
            else:
                flash('wrong password',category='danger')
                return render_template('customer/index.html')

        else:

            flash('Invalid username or password',category='danger')
            return render_template('customer/index.html')


            

    return render_template('index.html')


#category root
'''@app.route('/',methods=['GET','POST'])
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
                session['customer_ID'] = 333

                return redirect(url_for('customer',id='starter'))
            else:
                flash('wrong password',category='danger')
                return render_template('customer/index.html')

        else:

            flash('Invalid username or password',category='danger')
            return render_template('customer/index.html')

    return render_template('customer/index.html')'''


#categories
@app.route('/customer/category/<string:id>',methods=['GET','POST'])
def customer(id,msg=None):

    cur = mysql.connection.cursor()
    result=cur.execute("select * from items where category=%s",[id])
    items=cur.fetchall()
    return render_template('customer/category.html',items=items,msg=msg)

#test
@app.route('/test',methods=['GET','POST'])
def test():
    return render_template('index.html')

#Add Item
@app.route('/customer/category/additem',methods=['GET','POST'])
def additem():
    if request.method == 'POST':
        quan=request.form['quan']
        item_ID=request.form['item_added']
        cat=request.form['category']
        customer_ID = session['customer_ID']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO item_ordered(item_ID,quantity,customer_ID) VALUES(%s,%s,%s)",[item_ID,quan,customer_ID])
        mysql.connection.commit()
        flash("Successfully Added",category='success')
        return redirect(url_for('customer',id=cat))
    else:
        return "HEllO"
#main
if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
