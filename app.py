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
        result = cur.execute("SELECT * FROM users WHERE user_name= %s ",[username])
        
        if result > 0:
            record = cur.fetchone()
            passwordx = record['password']
            #if password correct
            if passwordx == password:
                #if it is service
                if record['type'] == 'service':
                    session['type'] = record['type']
                    session['user_name']=username
                    return redirect(url_for('table'))
                elif record['type'] == 'chef':
                    session['type'] = record['type']
                    session['user_name']=username
                    return redirect(url_for('chef'))
                elif record['type'] == 'accounts':
                    session['type'] = record['type']
                    session['user_name']=username
                    return redirect(url_for('accounts'))
                elif record['type'] == 'admin':
                    session['type'] = record['type']
                    session['user_name']=username
                    return redirect(url_for('admin'))
                else:
                    return 'Under Construction'
        #if password incorrect   
            else:
                msg='wrong password'
                return render_template('msg.html',msg=msg)
    #if username wrong
        else:

            return 'no user'
 

    return render_template('index.html')

#Logout
@app.route('/logout',methods=['GET','POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))



#category root
@app.route('/customer',methods=['GET','POST'])
def table():
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

                cur.execute("INSERT INTO customers(table_no) VALUE(%s)",[tableno])
                mysql.connection.commit()
                cur.execute("SELECT LAST_INSERT_ID()")
                cusid=cur.fetchone()
                
                session['cusid'] = cusid['LAST_INSERT_ID()']
                msg = session['cusid']
                return redirect(url_for('customer',id='starter'))
            else:
                flash('wrong password',category='danger')
                return render_template('customer/index.html')

        else:

            flash('Invalid username or password',category='danger')
            return render_template('customer/index.html')

    return render_template('customer/index.html')


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
    return render_template('accounts/accounts.html')

#Add Item
@app.route('/customer/category/additem',methods=['GET','POST'])
def additem():
    if request.method == 'POST':
        quan=float(request.form['quan'])
        item_ID=request.form['item_added']
        cat=request.form['category']
        customer_ID = session['cusid']
        item_price = float(request.form['item_price'])
        amt = item_price * quan
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO item_ordered(item_ID,quantity,customer_ID) VALUES(%s,%s,%s)",[item_ID,quan,customer_ID])
        cur.execute("UPDATE customers set bill_amount = bill_amount + %s WHERE customer_ID = %s",[amt,customer_ID])
        mysql.connection.commit()
        flash("Successfully Added",category='success')
        return redirect(url_for('customer',id=cat))
    else:
        return "HEllO"

#Order Status
@app.route('/customer/orderstatus')
def orderstatus():
    cur = mysql.connection.cursor()
    cusid = session['cusid']

    result = cur.execute("SELECT items.name,item_ordered.quantity,item_ordered.status,items.price FROM item_ordered,items WHERE items.item_ID = item_ordered.item_ID AND item_ordered.customer_ID = %s",[cusid])
    if result>0:
        total=0
        records = cur.fetchall()
        
        return render_template('customer/order_status.html',records=records,total= total)

    else:
        error="No Orders Yet"
        return render_template('customer/order_status.html',error = error)
#admin Sesssion
@app.route('/admin',methods=['GET','POST'])
def admin():
    return render_template('admin/dashboard.html')


# Chef Session
#Preparing
@app.route('/chef',methods=['GET','POST'])
def chef():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT items.name,item_ordered.quantity,item_ordered.time,item_ordered.status,item_ordered.order_ID,item_ordered.customer_ID FROM items,item_ordered WHERE item_ordered.item_ID = items.item_ID AND item_ordered.status = 'preparing'" )
    records=cur.fetchall()
    
    return render_template('chef/chef.html',records=records)

#Ready
@app.route('/chef/ready',methods=['GET','POST'])
def chefr():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT items.name,item_ordered.quantity,item_ordered.time,item_ordered.status,item_ordered.order_ID,item_ordered.customer_ID FROM items,item_ordered WHERE item_ordered.item_ID = items.item_ID AND item_ordered.status = 'ready' " )
    records=cur.fetchall()
    
    return render_template('chef/chef.html',records=records)

#Served
@app.route('/chef/served',methods=['GET','POST'])
def chefs():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT items.name,item_ordered.quantity,item_ordered.time,item_ordered.status,item_ordered.order_ID,item_ordered.customer_ID FROM items,item_ordered WHERE item_ordered.item_ID = items.item_ID AND item_ordered.status = 'served'" )
    records=cur.fetchall()
    
    return render_template('chef/chef.html',records=records)


#update status by chef
@app.route('/chef/update_prep/<string:id>',methods=['POST'])
def update_prep(id):
    cur=mysql.connection.cursor()
    cur.execute("UPDATE item_ordered SET status = 'ready' WHERE order_ID = %s ",[id])
    mysql.connection.commit()
    return redirect(url_for('chef'))

#update staus by chef
#update status by chef
@app.route('/chef/update_ready/<string:id>',methods=['POST'])
def update_ready(id):
    cur=mysql.connection.cursor()
    cur.execute("UPDATE item_ordered SET status = 'served' WHERE order_ID = %s ",[id])
    mysql.connection.commit()
    return redirect(url_for('chefr'))
#Accounts
@app.route('/accounts',methods=['GET','POST'])
def accounts():
    if request.method == 'POST':
        cus_ID=request.form['cus_ID']
        cur=mysql.connection.cursor()
        result=cur.execute('SELECT customer_ID,name,bill_amount FROM customers WHERE customer_ID=%s',[cus_ID])
        record=cur.fetchone()
        cur.execute('SELECT items.name,item_ordered.quantity,item_ordered.status,items.price FROM items,item_ordered WHERE customer_ID=%s AND item_ordered.item_ID = items.item_ID',[cus_ID])
        xrecord=cur.fetchall()

        return render_template('accounts/accounts.html',record=record,xrecord=xrecord)

    return render_template('accounts/accounts.html')




#main
if __name__ == '__main__':

    app.secret_key='secret123'
    app.run(debug=True)
