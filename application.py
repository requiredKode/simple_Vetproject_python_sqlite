from flask import Flask, render_template, request, redirect, session, url_for
from flask_session import Session
import sqlite3

app = Flask(__name__)

##SESSION##
app.config["SESSION_PERMANENT"]= False
app.config["SESSION_TYPE"]= "filesystem"
Session(app)

##SQLITE CONNECTION##
conn = sqlite3.connect('vet_project.db', check_same_thread=False)
cursor = conn.cursor()


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form.get("username")
        password = request.form.get("password")
        cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (username, password))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[3]

            return redirect(url_for('index_appointment'))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect("/")


@app.route("/")
def index():
    if 'loggedin' in session:
        return render_template('index_appointment.html', username=session['username'])
    return redirect(url_for('login'))

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/user_reg",methods=["GET","POST"])
def user_reg():
    if request.method == "POST":
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")
        cursor.execute("INSERT INTO Users (name, lastname, username, password, email) VALUES (?,?,?,?,?)", (name, lastname, username, password, email))
        conn.commit()
        return redirect(url_for('login'))
    return render_template("user_reg.html")

@app.route("/settings/<id>",methods=["POST","GET"])
def settings(id):
    cursor.execute("SELECT * FROM Users WHERE id = ?", (id, ))
    data = cursor.fetchall()

    return render_template('settings.html', user = data[0])

@app.route("/update/<id>", methods=["POST"])
def update_user(id):
    if request.method == 'POST':
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Users
            SET name = ?,
                lastname = ?,
                username = ?,
                password = ?,
                email = ?
            WHERE id = ?
        """, (name, lastname, username, password, email, id))
        conn.commit()
        return redirect(url_for('index_appointment'))


@app.route("/index_owner",methods=["GET","POST"])
def index_owner():
    cursor.execute('SELECT * FROM Owner')
    data = cursor.fetchall()
    return render_template("index_owner.html", owner = data)

@app.route("/add_owner",methods=["GET","POST"])
def add_owner():
    if request.method == "POST":
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        address = request.form.get("address")
        email = request.form.get("email")
        start_date = request.form.get("start_date")
        cursor.execute("INSERT INTO Owner (name, lastname, address, email, start_date) VALUES (?,?,?,?,?)", (name, lastname, address, email, start_date))
        conn.commit()
        return redirect(url_for('index_owner'))
    return render_template("add_owner.html")

@app.route('/edit_owner/<id>', methods = ["POST", "GET"])
def edit_owner(id):
    cursor.execute("SELECT * FROM Owner WHERE id = ?", (id, ))
    data = cursor.fetchall()
    return render_template("edit_owner.html", owner = data[0])

@app.route('/update_owner/<id>', methods=["POST"])
def update_owner(id):
    if request.method == 'POST':
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        address = request.form.get("address")
        email = request.form.get("email")
        start_date = request.form.get("start_date")

        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Owner
            SET name = ?,
                lastname = ?,
                address = ?,
                email = ?,
                start_date = ?
            WHERE id = ?
        """, (name, lastname, address, email, start_date, id))
        conn.commit()
        return redirect(url_for("index_owner"))

@app.route('/delete_owner/<string:id>', methods = ["POST","GET"])
def delete_owner(id):
    cursor.execute("DELETE FROM Owner WHERE id = {0}".format(id))
    conn.commit()
    return redirect(url_for("index_owner"))


@app.route("/index_pet",methods=["GET","POST"])
def index_pet():
    cursor.execute('SELECT * FROM Pet')
    data = cursor.fetchall()
    return render_template("index_pet.html", pet = data)

@app.route("/add_pet",methods=["GET","POST"])
def add_pet():
    if request.method == "POST":
        petname = request.form.get("petname")
        years = request.form.get("years")
        sex = request.form.get("sex")
        type_pet = request.form.get("type_pet")
        race = request.form.get("race")
        size = request.form.get("size")
        color = request.form.get("color")
        cursor.execute("INSERT INTO Pet (petname, years, sex, type_pet, race, size, color) VALUES (?,?,?,?,?,?,?)", (petname, years, sex, type_pet, race, size, color))
        conn.commit()
        return redirect(url_for('index_pet'))
    return render_template("add_pet.html")

@app.route('/edit_pet/<id>', methods = ["POST", "GET"])
def edit_pet(id):
    cursor.execute("SELECT * FROM Pet WHERE id = ?", (id, ))
    data = cursor.fetchall()
    return render_template("edit_pet.html", pet = data[0])

@app.route('/update_pet/<id>', methods=["POST"])
def update_pet(id):
    if request.method == 'POST':
        petname = request.form.get("petname")
        years = request.form.get("years")
        sex = request.form.get("sex")
        type_pet = request.form.get("type_pet")
        race = request.form.get("race")
        size = request.form.get("size")
        color = request.form.get("color")

        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Pet
            SET petname = ?,
                years = ?,
                sex = ?,
                type_pet = ?,
                race = ?,
                size = ?,
                color = ?
            WHERE id = ?
        """, (petname, years, sex, type_pet, race, size, color, id))
        conn.commit()
        return redirect(url_for("index_pet"))

@app.route('/delete_pet/<string:id>', methods = ["POST","GET"])
def delete_pet(id):
    cursor.execute("DELETE FROM Pet WHERE id = {0}".format(id))
    conn.commit()
    return redirect(url_for("index_pet"))


@app.route("/index_appointment",methods=["GET","POST"])
def index_appointment():
    cursor.execute('SELECT * FROM Appointment')
    data = cursor.fetchall()
    return render_template("index_appointment.html", appointment = data)

@app.route("/add_appointment",methods=["GET","POST"])
def add_appointment():
    if request.method == "POST":
        owner = request.form.get("owner")
        petname = request.form.get("petname")
        description = request.form.get("description")
        ap_date = request.form.get("ap_date")
        cursor.execute("INSERT INTO Appointment (owner, petname, description, ap_date) VALUES (?,?,?,?)", (owner, petname, description, ap_date))
        conn.commit()
        return redirect(url_for('index_appointment'))
    return render_template("add_appointment.html")

@app.route('/edit_appointment/<id>', methods = ["POST", "GET"])
def edit_appointment(id):
    cursor.execute("SELECT * FROM Appointment WHERE id = ?", (id, ))
    data = cursor.fetchall()
    return render_template("edit_appointment.html", appointment = data[0])

@app.route('/update_appointment/<id>', methods=["POST"])
def update_appointment(id):
    if request.method == 'POST':
        owner = request.form.get("owner")
        petname = request.form.get("petname")
        description = request.form.get("description")
        ap_date = request.form.get("ap_date")

        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Appointment
            SET owner = ?,
                petname = ?,
                description = ?,
                ap_date = ?
            WHERE id = ?
        """, (owner, petname, description, ap_date, id))
        conn.commit()
        return redirect(url_for("index_appointment"))

@app.route('/delete_appointment/<string:id>', methods = ["POST","GET"])
def delete_appointment(id):
    cursor.execute("DELETE FROM Appointment WHERE id = {0}".format(id))
    conn.commit()
    return redirect(url_for("index_appointment"))

