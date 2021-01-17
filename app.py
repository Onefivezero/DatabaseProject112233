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
    
@app.route('/devtool', methods = ["POST"])
def devtool():
    try:
        cur.execute("CREATE TABLE if not exists users (ID INT PRIMARY KEY, username VARCHAR(50) UNIQUE NOT NULL, password VARCHAR(50) UNIQUE NOT NULL, role BOOLEAN)")
        cur.execute("CREATE TABLE if not exists students (ID INT PRIMARY KEY, name VARCHAR(50), surname VARCHAR(50), gpa float, year INT, CONSTRAINT fk_st FOREIGN KEY(ID) REFERENCES users(ID))")
        cur.execute("CREATE TABLE courses(CRN INT PRIMARY KEY,name VARCHAR(50) NOT NULL,day VARCHAR(10) NOT NULL,num_enrolled INT,max_enrolled INT,year_req INT,hours VARCHAR(10), lecture_code VARCHAR(10))")
        cur.execute("CREATE TABLE queries(CRN INT, ID INT, status INT, ord INT, FOREIGN KEY(ID) REFERENCES students(ID), FOREIGN KEY(CRN) REFERENCES courses(CRN), PRIMARY KEY(CRN, ID))")
        cur.execute("INSERT into users(ID, username, password, role) VALUES (%s, %s, %s, %s)" , (request.form['id'),request.form['username'),request.form['password'),request.form['role'))
        conn.commit()
    except Exception as err:
        print(err)
        conn.rollback()
    return redirect('/')
    
@app.route('/add_student', methods = ["POST"])
def add_student():
    newstudent_id = int(request.form['newstudent_id'])
    newstudent_name = str(request.form['newstudent_name'])
    newstudent_surname = str(request.form['newstudent_surname'])
    newstudent_gpa = float(request.form['newstudent_gpa'])
    newstudent_year = int(request.form['newstudent_year'])
    cur.execute("INSERT into students(ID, name, surname, gpa, year) VALUES (%s, %s, %s, %s, %s)", (newstudent_id, newstudent_name, newstudent_surname,newstudent_gpa, newstudent_year))
    conn.commit()
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
    
@app.route('/reset', methods = ["POST"])
def reset():    
    cur.execute("UPDATE courses SET num_enrolled = 0")
    cur.execute("UPDATE queries SET status = 0")
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
        year = i[3]
        cur.execute("SELECT year_req FROM courses WHERE crn = %s", (crn,))
        year_req = cur.fetchone()[0]
        condition1 = year >= year_req
        cur.execute("SELECT num_enrolled, max_enrolled FROM courses WHERE crn = %s", (crn,))
        numandmax = cur.fetchone()
        condition2 = numandmax[0] < numandmax[1]
        cur.execute("SELECT hours, day FROM courses WHERE crn = %s", (crn,))
        time = cur.fetchone()
        condition3 = time not in time_arr
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
        return render_template('admin.html', data = [student_data])

@app.route('/register')
def register():
    if current_user.is_anonymous or current_user.adminship:
        return render_template('error.html')
    else:
        cur.execute("SELECT * FROM students WHERE ID = %s", (current_user.num,))
        data = cur.fetchall()
        return render_template('register.html', data = data)
        
@app.route('/addq', methods = ["POST"])
def addq():
    try:
        cur.execute("SELECT count(*) FROM queries WHERE id = %s", (current_user.num,))
        num = cur.fetchone()[0] + 1
        cur.execute("INSERT into queries (crn, id, status, ord) VALUES (%s, %s, %s, %s)", (request.form['crn'], current_user.num, 0, num))
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
    app.run()