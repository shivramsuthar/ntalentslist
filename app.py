from flask import Flask, render_template, flash, redirect, url_for, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app =Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'shivrfd'
app.config['MYSQL_DB'] = 'mydb'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# init MYSQL
mysql = MySQL(app)

# home page
@app.route('/')
def index():
        # jinja2 render lib
        return render_template('home.html')

# About page
@app.route('/about')
def about():
        return render_template('about.html')

# list page
@app.route('/list', methods =['GET'])
def list():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get lists
    result = cur.execute("select * from lists")
    lists = cur.fetchall()

    if result > 0:
        return render_template('lists.html', lists=lists)
    else:
        msg = 'No list Found'
        return render_template('lists.html', msg=msg)
    # Close connection
    cur.close()


#detail of specific list
@app.route('/list/<string:id>')
def Detail(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get list
    cur.execute("SELECT * FROM lists WHERE id = %s", [id])

    list = cur.fetchone()

    # Close connection
    cur.close()

    return render_template('list.html', list=list)

# Dashboard
@app.route('/dashboard')
def dashboard():
   # Create cursor
    cur = mysql.connection.cursor()

    # Get lists
    result = cur.execute("SELECT * FROM lists")

    # Show lists only from the user logged in 

    lists = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html', lists=lists)
    else:
        msg = 'No lists Found'
        return render_template('dashboard.html', msg=msg)
    # Close connection
    cur.close()

# list Form Class
class ListForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=200)])
    profession = StringField('Profession', [validators.Length(min=1, max=200)])
    aboutus = TextAreaField('About Us', [validators.Length(min=30)])
    mobile_number = StringField('Mobile Number', [validators.Length(min=10, max=10)])

# Add list
@app.route('/add_list', methods=['GET', 'POST'])
def add_list():
    form = ListForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        profession = form.profession.data
        aboutus = form.aboutus.data
        mobile_number = form.mobile_number.data

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute("INSERT INTO lists(name, profession, aboutus, mobile_number) VALUES(%s, %s, %s, %s)",(name, profession, aboutus, mobile_number))

        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('list Created', 'success')

        return redirect(url_for('dashboard'))
   
    return render_template('add_list.html', form=form)

# Delete list
@app.route('/delete_list/<string:id>', methods=['POST'])
def delete_list(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Execute
    cur.execute("DELETE FROM lists WHERE id = %s", [id])

    # Commit to DB
    mysql.connection.commit()

    #Close connection
    cur.close()

    flash('list Deleted', 'success')

    return redirect(url_for('dashboard'))

# Edit list
@app.route('/edit_list/<string:id>', methods=['GET', 'POST'])
def edit_list(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get list by id
    cur.execute("SELECT * FROM lists WHERE id = %s", [id])

    list = cur.fetchone()
    cur.close()
    # Get form
    form = ListForm(request.form)

    # Populate list form fields
    form.name.data = list['name']
    form.profession.data = list['profession']
    form.aboutus.data = list['aboutus']
    form.mobile_number.data = list['mobile_number']
    

    if request.method == 'POST' and form.validate():
        name = request.form['name']
        profession = request.form['profession']
        aboutus = request.form['aboutus']
        mobile_number = request.form['mobile_number']

        # Create Cursor
        cur = mysql.connection.cursor()
        # Execute
        cur.execute ("UPDATE lists SET name=%s,profession=%s, aboutus=%s, mobile_number=%s WHERE id=%s",(name,profession,aboutus,mobile_number, id))
        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('list Updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_list.html', form=form)

if __name__=='__main__':
    app.secret_key='shivrfd123'
    app.run(debug=True)