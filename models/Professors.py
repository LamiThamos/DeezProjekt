from database import db_connection
#from models.category import Category

class Professors:
    def __init__(self, id, name, grade_average, pass_percentage):
        self.id = id
        self.name = name
        self.grade_average = grade_average
        self.pass_percentage = pass_percentage

def list_professors(pattern):
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM professors WHERE name ~* %s', (pattern,))
    db_professors = cur.fetchall()
    professors = []
    for professor_entry in db_professors:
        professors.append(Professors(professor_entry[0], 
                                     professor_entry[1], 
                                     ("N/A" if professor_entry[2] is None else round(professor_entry[2], 2)), 
                                     round(professor_entry[3], 2)))

    conn.close()
    return professors

def get_professor_by_id(professor_id):
    conn = db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM professors WHERE id = %s', (professor_id,))
    db_professor = cur.fetchall()[0]
    professor = Professors(db_professor[0], 
                           db_professor[1], 
                           ("N/A" if db_professor[2] is None else round(db_professor[2], 2)), 
                           round(db_professor[3], 2))
    conn.close()
    return professor
