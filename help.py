import psycopg2

try:
    conn = psycopg2.connect("dbname = postgres user = postgres host = localhost password = admin")
except:
    print("Connection failed")
cur = conn.cursor()

# users table
# cur.execute("CREATE TABLE if not exists users (ID INT PRIMARY KEY, username VARCHAR(50) UNIQUE NOT NULL, password VARCHAR(50) UNIQUE NOT NULL, role BOOLEAN;")

# students table
# cur.execute("ALTER TABLE students ADD PRIMARY KEY (ID)")
# cur.execute("ALTER TABLE students ALTER COLUMN gpa TYPE real")
# cur.execute("CREATE TABLE if not exists students (ID INT, name VARCHAR(50), surname VARCHAR(50), gpa NUMERIC(3,2), year INT, CONSTRAINT fk_st FOREIGN KEY(ID) REFERENCES users(ID));")

# courses table
#cur.execute("ALTER TABLE queries ADD PRIMARY KEY (ID)")
#cur.execute("CREATE TABLE courses(CRN INT PRIMARY KEY,name VARCHAR(50) NOT NULL,day VARCHAR(10) NOT NULL,num_enrolled INT,max_enrolled INT,year_req INT,hours VARCHAR(10), lecture_code VARCHAR(10));")

# queries table
#cur.execute("CREATE TABLE queries(CRN INT, ID INT, status INT, FOREIGN KEY(ID) REFERENCES students(ID), FOREIGN KEY(CRN) REFERENCES courses(CRN), PRIMARY KEY(CRN, ID));")

# cur.execute("INSERT into users(ID, username, password, role) VALUES ('120', 'ali', 'ree', '0')")
# cur.execute("INSERT into users(ID, username, password, role) VALUES ('121', 'fatma', 're', '0')")
# cur.execute("INSERT into users(ID, username, password, role) VALUES ('122', 'isimsiz kahraman', 'asd', '1')")
# cur.execute("INSERT into users(ID, username, password, role) VALUES ('123', 'burak', 'ddd', '0')")
# cur.execute("INSERT into users(ID, username, password, role) VALUES ('124', 'a', 'qwe', '0')")
# cur.execute("INSERT into users(ID, username, password, role) VALUES ('125', 'b', '1221313412124', '0')")
# cur.execute("INSERT into users(ID, username, password, role) VALUES ('126', 'c', 'zxcvzvx', '0')")
# cur.execute("INSERT into users(ID, username, password, role) VALUES ('127', 'd', 'dd', '0')")
# cur.execute("INSERT into users(ID, username, password, role) VALUES ('128', 'e', 'ee', '0')")
# cur.execute("INSERT into users(ID, username, password, role) VALUES ('129', 'f', 'ff', '0')")

# cur.execute("INSERT into students(ID, name, surname, gpa, year) VALUES ('120', 'Ali', 'Er', '4.0', '1')")
# cur.execute("INSERT into students(ID, name, surname, gpa, year) VALUES ('121', 'Fatma', 'Yıldırım', '3.8', '2')")
# cur.execute("INSERT into students(ID, name, surname, gpa, year) VALUES ('123', 'Burak', 'Yılmaz', '3.1', '3')")
# cur.execute("INSERT into students(ID, name, surname, gpa, year) VALUES ('124', 'a', 'x', '0', '4')")
# cur.execute("INSERT into students(ID, name, surname, gpa, year) VALUES ('125', 'b', 'y', '0', '4')")
# cur.execute("INSERT into students(ID, name, surname, gpa, year) VALUES ('126', 'c', 'z', '0', '4')")

# cur.execute("INSERT into courses(CRN, name, day, num_enrolled, max_enrolled, year_req, hours, lecture_code) VALUES ('0001', 'Beginner', 'Monday', 0, 100, 1, '0830-1130', 'BLG101')")
# cur.execute("INSERT into courses(CRN, name, day, num_enrolled, max_enrolled, year_req, hours, lecture_code) VALUES ('0002', 'Intermediate', 'Monday', 0, 100, 2, '1330-1630', 'BLG102')")
# cur.execute("INSERT into courses(CRN, name, day, num_enrolled, max_enrolled, year_req, hours, lecture_code) VALUES ('0003', 'Advanced', 'Monday', 0, 100, 1, '0830-1130', 'BLG103')")


# cur.execute("SELECT q.* FROM students s, queries q WHERE s.id = q.id")
# cur.execute("UPDATE queries SET status = 0")
# cur.execute("DELETE FROM queries")
# cur.execute("ALTER TABLE queries ADD COLUMN ord INTEGER")
# conn.commit()
# cur.execute("SELECT count(*) FROM students WHERE year = 4")
cur.execute("SELECT * from queries")

for i in cur.fetchall():
    print(i)

conn.commit()
cur.close()