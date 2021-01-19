from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user
import psycopg2
import os


DATABASE_URL = os.environ['DATABASE_URL']

try:
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
except:
    print("Connection failed")
    
login_manager = LoginManager()
cur = conn.cursor()

app = Flask(__name__)
app.secret_key = "pHgF?W)_4m</8#OQ&J1JguQ%X6dOO*"
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, num, username, password, status):
        self.id = username
        self.password = password
        self.num = num
        self.adminship = status
        self.active = True
        def is_anonymous(self):
            return False
        def is_active(self):
            return True
        def is_authenticated(self):
            return True
        def get_id(self):
            return self.id
        
def get_user(given_username):
    if not isinstance(given_username, str):
        return None
    cur.execute("SELECT * FROM users WHERE username = %s", (given_username,))
    info = cur.fetchone()
    if info:
        return User(info[0], info[1], info[2], info[3])
    return None

@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id)

@app.route('/')
def index():
    return render_template('index.html')
    
# @app.route('/devtool', methods = ["POST"])
# def devtool():
    # try:
        # cur.execute("")
        # conn.commit()
    # except Exception as err:
        # print(err)
        # conn.rollback()
    # return redirect('/')
    
@app.route('/add_student', methods = ["POST"])
def add_student():
    try:
        newstudent_id = int(request.form['newstudent_id']) if request.form['newstudent_id'] else None
        newstudent_name = request.form['newstudent_name'] or None
        newstudent_surname = request.form['newstudent_surname'] or None
        newstudent_gpa = float(request.form['newstudent_gpa']) if request.form['newstudent_gpa'] else None
        newstudent_year = int(request.form['newstudent_year'])if request.form['newstudent_year'] else None
        newstudent_username = request.form["newstudent_username"] or None
        newstudent_password = request.form["newstudent_password"] or None
    except Exception as err:
        print(err)
        return redirect("/admin")
    if id == None:
        return redirect('/admin')
    if(request.form["student_radio"] == "add"):
        try:
            cur.execute("INSERT into users(ID, username, password, role) VALUES (%s, %s, %s, %s)", (newstudent_id, newstudent_username, newstudent_password, "FALSE",))
        except Exception as err:
            print(err)
        try:
            cur.execute("INSERT into students(ID, name, surname, gpa, year) VALUES (%s, %s, %s, %s, %s)", (newstudent_id, newstudent_name, newstudent_surname,newstudent_gpa, newstudent_year),)
            conn.commit()
        except Exception as err:
            print(err)
    else:
        try:
            cur.execute("UPDATE users SET username = COALESCE(%s, username), password = COALESCE(%s, password) WHERE id = %s ", (newstudent_username, newstudent_password, newstudent_id))
            conn.commit()
        except Exception as err:
            print(err)
            conn.rollback()
        try:
            cur.execute("UPDATE students SET name = COALESCE(%s, name), surname = COALESCE(%s, surname), gpa = COALESCE(%s, gpa), year =  COALESCE(%s, year) WHERE id = %s ", (newstudent_name, newstudent_surname, newstudent_gpa, newstudent_year, newstudent_id,))
            conn.commit()
        except Exception as err:
            print(err)
            conn.rollback()
    return redirect('/admin')
        
@app.route('/modify_student', methods = ["POST"])
def modify_student():
    id = request.form["student_mod_id"] or None
    if id == None:
        return redirect('/admin')
    name = request.form["student_mod_name"] or None
    surname = request.form["student_mod_surname"] or None
    gpa = request.form["student_mod_gpa"] or None
    year = request.form["student_mod_year"] or None
    try:
        cur.execute("UPDATE students SET name = COALESCE(%s, name), surname = COALESCE(%s, surname), gpa = COALESCE(%s, gpa), year =  COALESCE(%s, year) WHERE id = %s ", (name, surname, gpa, year, id,))
        conn.commit()
    except Exception as err:
        print(err)
        conn.rollback()
    return redirect('/admin')
    
@app.route('/delete_student', methods = ["POST"])
def delete_student():
    try:
        cur.execute("DELETE FROM queries WHERE id = %s", (request.form["student_del_id"],))
        cur.execute("DELETE FROM students WHERE id = %s", (request.form["student_del_id"],))
        cur.execute("DELETE FROM users WHERE id = %s AND role = FALSE", (request.form["student_del_id"],))
        conn.commit()
    except Exception as err:
        print(err)
        conn.rollback()
    return redirect('/admin')
    
@app.route('/add_course', methods = ["POST"])
def add_course():
    try:
        cur.execute("INSERT into courses(CRN, name, day, num_enrolled, max_enrolled, year_req, hours, lecture_code) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (request.form["course_crn"], request.form["course_name"],request.form["course_day"], 0, request.form["course_max"], request.form["course_yearreq"],request.form["course_hours"],request.form["course_code"],))
        conn.commit()
    except Exception as err:
        print(err)
        conn.rollback()
    return redirect('/admin')
    
@app.route('/modify_course', methods = ["POST"])
def modify_course():
    crn = request.form["course_mod_crn"] or None
    if crn == None:
        return redirect('/admin')
    name = request.form["course_mod_name"] or None
    day = request.form["course_mod_day"] or None
    max_enrolled = request.form["course_mod_max"] or None
    year_req = request.form["course_mod_yearreq"] or None
    hours = request.form["course_mod_hours"] or None
    code = request.form["course_mod_code"] or None
    try:
        cur.execute("UPDATE courses SET name = COALESCE(%s, name), day = COALESCE(%s, day), max_enrolled = COALESCE(%s, max_enrolled), year_req =  COALESCE(%s, year_req), hours = COALESCE(%s, hours), lecture_code = COALESCE(%s, lecture_code) WHERE crn = %s ", (name, day, max_enrolled, year_req, hours, code, crn,))
        conn.commit()
    except Exception as err:
        print(err)
        conn.rollback()
    return redirect('/admin')
    
@app.route('/delete_course', methods = ["POST"])
def delete_course():
    try:
        cur.execute("DELETE FROM courses WHERE crn = %s", (request.form["course_del_crn"],))
        conn.commit()
    except Exception as err:
        print(err)
        conn.rollback()
    return redirect('/admin')

@app.route('/reset', methods = ["POST"])
def reset():    
    cur.execute("UPDATE courses SET num_enrolled = 0")
    cur.execute("DELETE FROM queries")
    conn.commit()
    return redirect('/admin')
    
@app.route('/finalize', methods = ["POST"])
def finalize():
    data = []
    try:
        cur.execute("SELECT q.*, s.year, s.gpa FROM students s, queries q WHERE s.id = q.id ORDER BY s.year DESC, s.gpa DESC, q.id ASC, q.ord")
        data = cur.fetchall()
    except Exception as err:
        print(err)
        conn.rollback()
    last_id = 0
    time_arr = []
    for i in data:
        crn = i[0]
        id = i[1]
        if(last_id != id):
            last_id = id
            time_arr = []
        year = i[4]
        cur.execute("SELECT year_req FROM courses WHERE crn = %s", (crn,))
        year_req = cur.fetchone()[0]
        condition1 = year >= year_req
        cur.execute("SELECT num_enrolled, max_enrolled FROM courses WHERE crn = %s", (crn,))
        numandmax = cur.fetchone()
        condition2 = numandmax[0] < numandmax[1]
        cur.execute("SELECT hours, day FROM courses WHERE crn = %s", (crn,))
        time = cur.fetchone()[0]
        time_start = int(time.split("-")[0])
        time_end = int(time.split("-")[1])
        condition3 = True
        for x in time_arr:
            time2_start = int(x.split("-")[0])
            time2_end = int(x.split("-")[1])
            if not (time_start > time2_end or time_end < time2_start):
                condition3 = False
        if(condition1 and condition2 and condition3):
            time_arr.append(time)
            try:
                cur.execute("UPDATE courses SET num_enrolled = num_enrolled + 1 WHERE crn = %s", (crn,))
                cur.execute("UPDATE queries SET status = 1 WHERE crn = %s AND id = %s", (crn, id))
                conn.commit()
            except Exception as err:
                print(err)
                conn.rollback()
    return redirect('/admin')
    
@app.route('/admin')
def admin():
    if current_user.is_anonymous or not current_user.adminship:
        return render_template('error.html')
    else:
        cur.execute("SELECT * FROM students")
        student_data = cur.fetchall()
        cur.execute("SELECT * FROM courses")
        courses_data = cur.fetchall()
        cur.execute("SELECT * FROM users")
        users_data = cur.fetchall()
        return render_template('admin.html', data = student_data, data2 = courses_data, data3 = users_data)

@app.route('/register')
def register():
    if current_user.is_anonymous or current_user.adminship:
        return render_template('error.html')
    else:
        cur.execute("SELECT * FROM queries WHERE ID = %s AND status = 1", (current_user.num,))
        protodata = cur.fetchall()
        data = []
        for i in protodata:
            try:
                cur.execute("SELECT name, day, hours FROM courses WHERE crn = %s", (i[0],))
                data.append(cur.fetchone())
            except Exception as err:
                print(err)
        cur.execute("SELECT * FROM queries WHERE ID = %s", (current_user.num,))
        query_data = cur.fetchall()
        return render_template('register.html', data = data, data2 = query_data)
        
@app.route('/addquery', methods = ["POST"])
def addquery():
    try:
        cur.execute("SELECT count(*) FROM queries WHERE id = %s", (current_user.num,))
        num = cur.fetchone()[0] + 1
        cur.execute("INSERT into queries (crn, id, status, ord) VALUES (%s, %s, %s, %s)", (request.form['crn_add'], current_user.num, 0, num))
        conn.commit()
    except Exception as err:
        print(err)
        conn.rollback()
    return redirect('register')

@app.route('/deletequery', methods = ["POST"])
def deletequery():
    try:
        cur.execute("SELECT ord FROM queries WHERE crn = %s AND id = %s", (request.form['crn_del'], current_user.num))
        temp = cur.fetchone()
        cur.execute("DELETE FROM queries WHERE crn = %s AND id = %s", (request.form['crn_del'], current_user.num))
        cur.execute("UPDATE queries SET ord = ord - 1 WHERE ord > %s AND id = %s", (temp, current_user.num))
        conn.commit()
    except Exception as err:
        print(err)
        conn.rollback()
    return redirect('register')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        user = load_user(request.form['givenu'])
        if user:
            if user.password == request.form['givenp']:
                login_user(user)
                next_page = request.args.get("next", url_for("index"))
                return redirect(next_page)
        return redirect('/')
    return render_template("login.html")

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')
    
    
if __name__ == "__main__":
    cur.execute("CREATE TABLE if not exists users (ID INT PRIMARY KEY, username VARCHAR(50) UNIQUE NOT NULL, password VARCHAR(50) UNIQUE NOT NULL, role BOOLEAN;")
    cur.execute("CREATE TABLE if not exists courses(CRN INT PRIMARY KEY,name VARCHAR(50) NOT NULL,day VARCHAR(10) NOT NULL,num_enrolled INT NOT NULL,max_enrolled INT NOT NULL,year_req INT NOT NULL,hours VARCHAR(10) NOT NULL, lecture_code VARCHAR(10) NOT NULL);")
    cur.execute("CREATE TABLE if not exists students (ID INT PRIMARY KEY, name VARCHAR(50) NOT NULL, surname VARCHAR(50) NOT NULL, gpa float NOT NULL, year INT NOT NULL, FOREIGN KEY(ID) REFERENCES users(ID));")
    cur.execute("CREATE TABLE if not exists queries(CRN INT, ID INT, status INT NOT NULL, ord INT NOT NULL, FOREIGN KEY(ID) REFERENCES students(ID), FOREIGN KEY(CRN) REFERENCES courses(CRN), PRIMARY KEY(CRN, ID));")
    app.run()