import psycopg2
import os

# Try to get from system enviroment variable
# Set your Postgres user, password, and database name as second arguments of these three next function calls
dbname   = os.environ.get('PGDATABASE', 'postgres')
user     = os.environ.get('PGUSER',     'Project')
password = os.environ.get('PGPASSWORD', 'Deez')
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
        DROP TABLE IF EXISTS Professors CASCADE;
        CREATE TABLE Professors(
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            grade_average FLOAT,
            pass_percentage FLOAT NOT NULL DEFAULT 0
        );
    """)

    cur.execute("""
        DROP TABLE IF EXISTS Courses CASCADE;
        CREATE TABLE Courses (
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
        DROP TABLE IF EXISTS CourseHasProfessor CASCADE;
        CREATE TABLE CourseHasProfessor (
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

def add_triggers():
    conn = db_connection()
    cur = conn.cursor()

    cur.execute(''' 
        CREATE OR REPLACE FUNCTION update_professor_stats()
        RETURNS TRIGGER AS $$
        BEGIN
            UPDATE Professors
            SET grade_average = ( 
                SELECT (
                    SUM(LOG( CASE WHEN CourseHasProfessor.is_course_responsible THEN Courses.num_students*2 ELSE Courses.num_students END) * Courses.grade_average) 
                    / 
                    SUM(LOG( CASE WHEN CourseHasProfessor.is_course_responsible THEN Courses.num_students*2 ELSE Courses.num_students END))
                    ) 
                    AS new_grade_average
                FROM Courses
                JOIN CourseHasProfessor ON Courses.id = CourseHasProfessor.course_id
                WHERE CourseHasProfessor.professor_id = NEW.professor_id
            ),
            pass_percentage = (
                SELECT (
                    SUM(LOG( CASE WHEN CourseHasProfessor.is_course_responsible THEN Courses.num_students*2 ELSE Courses.num_students END) * Courses.pass_percentage) 
                    / 
                    SUM(LOG( CASE WHEN CourseHasProfessor.is_course_responsible THEN Courses.num_students*2 ELSE Courses.num_students END))
                    ) 
                    AS new_pass_percentage
                FROM Courses
                JOIN CourseHasProfessor ON Courses.id = CourseHasProfessor.course_id
                WHERE CourseHasProfessor.professor_id = NEW.professor_id
            )
            WHERE id = NEW.professor_id;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    ''')

    conn.commit()

    cur.execute('''
        DROP TRIGGER IF EXISTS update_professor_stats_trigger ON CourseHasProfessor;
        CREATE TRIGGER update_professor_stats_trigger
        AFTER INSERT OR UPDATE ON CourseHasProfessor
        FOR EACH ROW
        EXECUTE FUNCTION update_professor_stats();
    ''')

    conn.commit()
    cur.close()
    conn.close()

def seed_db():
    conn = db_connection()
    cur = conn.cursor()

    professors = [
        "Dmitriy Traytel",
        "Panagiotis Karras",
        "Philippe Bonnet",
        "Mikkel Abrahamsen",
        "Boris Düdder",
        "Jacob Holm",
        "Mikkel Thorup"
    ]

    for name in professors:
        cur.execute(
            "INSERT INTO Professors (name) VALUES (%s) ON CONFLICT DO NOTHING;",
            (name,)
        )

    courses = [ 
        ("DIS", 276, "7-trinsskala", 4.4, 62.0, "ITX"),
        ("RAD", 90, "7-trinsskala", 7.3, 63.0, "Oral"),
        ("POP", 294, "Pass/fail", None, 79.0, "Continuous assessment"),
        ("DMA", 151, "Pass/fail", None, 80.0, "Continuous assessment"),
        ("SU", 186, "Pass/fail", 8.2, 67.0, "Oral")
    ]

    for course in courses:
        cur.execute("""
            INSERT INTO Courses
            (name, num_students, grade_format, grade_average, pass_percentage, exam_type)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, course)
    
    courseHasProfessorRelation = [
        (1, 1, True),  # Dmitriy Traytel is course responsible for DIS
        (1, 2, False), # Panagiotis Karras teaches DIS
        (2, 6, True),  # Jacob Holm is course responsible for RAD
        (2, 7, False), # Mikkel Thorup teaches RAD
        (3, 3, True),  # Philippe Bonnet is course responsible for POP
        (4, 4, True),  # Mikkel Abrahamsen is course responsible for DMA
        (5, 3, False), # Philippe Bonnet teaches SU
        (5, 5, True)   # Boris Düdder is course responsible for SU
    ]
    
    for (course_id, professor_id, is_course_responsible) in courseHasProfessorRelation:
        cur.execute('''
            INSERT INTO CourseHasProfessor 
            (course_id, professor_id, is_course_responsible) 
            VALUES (%s, %s, %s) 
            ON CONFLICT DO NOTHING
        ''', (course_id, professor_id, is_course_responsible))


    conn.commit()
    cur.close()
    conn.close()





