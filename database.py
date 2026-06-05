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
                WHERE CourseHasProfessor.professor_id = NEW.professor_id AND Courses.grade_average IS NOT NULL
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
        "Dmitriy Traytel",      #1
        "Panagiotis Karras",    #2
        "Philippe Bonnet",      #3
        "Mikkel Abrahamsen",    #4
        "Boris Düdder",         #5
        "Jacob Holm",           #6
        "Mikkel Thorup",        #7
        "Rasmus Pagh",          #8
        "Amir Yehudayoff",      #9
        "Laura Mancinska",      #10
        "Kasper Hornbæk",       #11
        "Henrik Holm",          #12
        "Henrik Pedersen",      #13
        "Fritz Henglein",       #14
        "Jon Sporring",         #15
        "Morten Risager",       #16
        "Jesper Grodal",        #17
        "Bo Markussen",         #18
        "Helle Soerensen",      #19
        "Desmond Elliott",      #20
        "Tuukka Ruotsalo",      #21
        "Michael Thomsen",      #22
        "David Marchant",       #23
        "Finn Andersen",        #24
        "Pawel Winter",         #25
    ]

    for name in professors:
        cur.execute(
            "INSERT INTO Professors (name) VALUES (%s) ON CONFLICT DO NOTHING;",
            (name,)
        )

    courses = [ 
        ("DIS", 276, "7-trinsskala", 4.4, 62.0, "ITX"),                         #1
        ("RAD", 90, "7-trinsskala", 7.3, 63.0, "Oral"),                         #2
        ("POP", 294, "Pass/fail", None, 79.0, "Continuous assessment"),         #3
        ("DMA", 151, "Pass/fail", None, 80.0, "Continuous assessment"),         #4
        ("SU", 186, "Pass/fail", 8.2, 67.0, "Oral"),                            #5
        ("AD", 267, "7-trinsskala", 4.9, 73.0, "ITX"),                          #6
        ("Inter", 175, "7-trinsskala", 7.5, 84.0, "Write-at-home"),             #7
        ("LinAlgDat", 345, "7-trinsskala", 5.2, 71.0, "ITX"),                   #8
        ("MatDat", 203, "7-trinsskala", 5.4, 79.0, "ITX"),                      #9
        ("Alg2", 49, "7-trinsskala", 7.9, 67.0, "Oral"),                        #10
        ("MatIntroMat", 281, "7-trinsskala", 6.9, 88.0, "In-class test"),       #11
        ("SS", 138, "7-trinsskala", 6.1, 75.0, "ITX"),                          #12
        ("GDS", 126, "7-trinsskala", 9.6, 87.0, "Project submission"),          #13
        ("CompSys", 150, "7-trinsskala", 5.4, 60.0, "ITX"),                     #14
        ("IPA", 7, "7-trinsskala", 8.9, 100.0, "Oral"),                         #15
        ("CG", 39, "7-trinsskala", 8.2, 77.0, "Oral"),                          #16
    ]

    for course in courses:
        cur.execute("""
            INSERT INTO Courses
            (name, num_students, grade_format, grade_average, pass_percentage, exam_type)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING;
        """, course)
    
    courseHasProfessorRelation = [
        (1, 1, True),    # Dmitriy Traytel is course responsible for DIS
        (1, 2, False),   # Panagiotis Karras teaches DIS
        (2, 6, True),    # Jacob Holm is course responsible for RAD
        (2, 7, False),   # Mikkel Thorup teaches RAD
        (3, 3, True),    # Philippe Bonnet is course responsible for POP
        (3, 14, False),  # Fritz Henglein teaches POP
        (3, 15, False),  # Jon Sporring teaches POP
        (4, 4, True),    # Mikkel Abrahamsen is course responsible for DMA
        (4,8, False),    # Rasmus Pagh teaches DMA
        (4, 10, False),  # Laura Mancinska teaches DMA
        (5, 3, False),   # Philippe Bonnet teaches SU
        (5, 5, True),    # Boris Düdder is course responsible for SU
        (6, 8, True),    # Rasmus Pagh is course responsible for AD 
        (6, 4, False),   # Mikkel Abrahamsen teaches AD
        (6, 9, False),   # Amir Yehudayoff teaches AD
        (7, 11, True),   # Kasper Hornbæk is course responsible for Inter
        (8, 12, True),   # Henrik Holm is course responsible for LinAlgDat
        (8, 13, True),   # Henrik Pedersen is course responsible for LinAlgDat
        (9, 12, True),   # Henrik Holm is course responsible for MatDat
        (9, 13, True),   # Henrik Pedersen is course responsible for MatDat
        (10, 12, True),  # Henrik Holm is course responsible for Alg2
        (11, 16, True),  # Morten Risager is course responsible for MatIntroMat
        (11, 17, True),  # Jesper Grodal is course responsible for MatIntroMat
        (12, 18, True),  # Bo Markussen is course responsible for SS
        (12, 19, True),  # Helle Soerensen is course responsible for SS
        (13, 20, True),  # Desmond Elliott is course responsible for GDS
        (13, 21, False), # Tuukka Ruotsalo teaches GDS
        (14, 22, True),  # Michael Thomsen is course responsible for CompSys
        (14, 23, False), # David Marchant teaches CompSys
        (14, 24, False), # Finn Andersen teaches CompSys
        (15, 1, True),   # Dmitriy Traytel is course responsible for IPA
        (16, 4, True),   # Mikkel Abrahamsen is course responsible for CG
        (16, 25, False)  # Pawel Winter teaches CG
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





