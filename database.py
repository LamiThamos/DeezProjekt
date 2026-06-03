import psycopg2
import os

# Try to get from system enviroment variable
# Set your Postgres user, password, and database name as second arguments of these three next function calls
dbname   = os.environ.get('PGDATABASE', 'DIS Project')
user     = os.environ.get('PGUSER',     'dis project')
password = os.environ.get('PGPASSWORD', '123')
host     = os.environ.get('HOST',       '127.0.0.1')

def db_connection():
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host
    )
    return conn

def init_db():
    conn = db_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Professors(
            id SERIAL PRIMARY KEY,
            Name TEXT NOT NULL,
            grade_average FLOAT NOT NULL DEFAULT 0,
            pass_percentage FLOAT NOT NULL DEFAULT 0
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Courses (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            num_students INT NOT NULL,
            grade_format TEXT NOT NULL,
            grade_average FLOAT,
            pass_percentage FLOAT NOT NULL,
            exam_type TEXT NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS CourseHasProfessor (
            course_id INT NOT NULL,
            professor_id INT NOT NULL,
            is_course_responsible BOOLEAN NOT NULL DEFAULT FALSE,

            PRIMARY KEY (course_id, professor_id),

            FOREIGN KEY (course_id)
                REFERENCES Courses(id)
                ON DELETE CASCADE,

            FOREIGN KEY (professor_id)
                REFERENCES Professors(id)
                ON DELETE CASCADE
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

def seed_db():
    conn = db_connection()
    cur = conn.cursor()

    professors = [
        "Dmitriy",
        "Panos",
        "Philippe Bonnet",
        "Mikkel Abrahamsen",
        "Boris Düdder",
        "Jacob"
    ]

    for name in professors:
        cur.execute(
            "INSERT INTO Professors (name) VALUES (%s) ON CONFLICT DO NOTHING;",
            (name)
        )

    courses = [
        ("DIS", 100, "7-trinsskala", 3.5, 85.0, "ITX"),
        ("RAD", 80, "7-trinsskala", 3.0, 80.0, "Oral"),
        ("POP", 60, "Pass/fail", 2.5, 75.0, "Continuous assessment"),
        ("DMA", 50, "Pass/fail", 3.8, 90.0, "Continuous assessment"),
        ("SU", 40, "Pass/fail", 2.0, 70.0, "Oral")
    ]

    for course in courses:
        cur.execute("""
            INSERT INTO Courses
            (name, num_students, grade_format, grade_average, pass_percentage, exam_type)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, course)

    conn.commit()
    cur.close()
    conn.close()

#def add_triggers():


if __name__ == "__main__":
    init_db()
    seed_db()
    #add_triggers()




