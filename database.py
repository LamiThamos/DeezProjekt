import psycopg2
import os

# Try to get from system enviroment variable
# Set your Postgres user, password, and database name as second arguments of these three next function calls
user = os.environ.get('PGUSER', 'postgres')
password = os.environ.get('PGPASSWORD', '102mater')
dbname = os.environ.get('PGDATABASE', 'postgres')
host = os.environ.get('HOST', '127.0.0.1')

def db_connection():
    db = "dbname=" + dbname + " user=" + user + " host=" + host + " password =" + password
    conn = psycopg2.connect(db)

    return conn

def init_db():
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS Professors (id SERIAL PRIMARY KEY, Name TEXT NOT NULL)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS Courses (id SERIAL PRIMARY KEY, name TEXT NOT NULL, NumStudents INT NOT NULL, GradeFormat TEXT NOT NULL, GradeAverage FLOAT, PassPercentage FLOAT NOT NULL, ExamType TEXT NOT NULL)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS CourseHasProfessor (CourseID INT NOT NULL, ProfessorID INT NOT NULL, IsCourseResposible BOOLEAN NOT NULL DEFAULT FALSE, (CourseID, ProfessorID) PRIMARY KEY NOT NULL, CourseID FOREIGN KEY REFERENCES Courses(ID), ProfessorID FOREIGN KEY REFERENCES Professors(ID))''')
    conn.commit()

    professors = ['Dmitriy', 'Panos', 'Philippe Bonnet', 'Mikkel Abrahamsen', 'Boris Düdder', 'Jacob']
    for professorName in professors:
        cur.execute('INSERT INTO Professors (professorName) VALUES (%s) ON CONFLICT DO NOTHING', professorName)


    courses = [('DIS', 100, '7-trinsskala', 3.5, 85.0, 'ITX'),
                ('RAD', 80, '7-trinsskala', 3.0, 80.0, 'Oral'),
                ('POP', 60, 'Pass/fail', 2.5, 75.0, 'Continuous assessment'),
                ('DMA', 50, 'Pass/fail', 3.8, 90.0, 'Continuous assessment'),
                ('SU', 40, 'Pass/fail', 2.0, 70.0, 'Oral') 
               ]
    for (name, NumStudents, GradeFormat, GradeAverage, PassPercentage, ExamType) in courses:
        cur.execute('INSERT INTO Courses (name, NumStudents, GradeFormat, GradeAverage, PassPercentage, ExamType) VALUES (%s) ON CONFLICT DO NOTHING', (name, NumStudents, GradeFormat, GradeAverage, PassPercentage, ExamType))

    courseHasProfessorRelation = [(1, 1, True), (1, 2, False), (2, 6, True), (3, 3, True), (4, 4, True), (5, 5, True), (3, 5, False)]
    for (CourseID, ProfessorID, IsCourseResposible) in courseHasProfessorRelation:
        cur.execute('INSERT INTO CourseHasProfessor (CourseID, ProfessorID, IsCourseResposible) VALUES (%s) ON CONFLICT DO NOTHING', (CourseID, ProfessorID, IsCourseResposible))


    conn.commit()
    conn.close()
