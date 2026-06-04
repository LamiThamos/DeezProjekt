from database import db_connection
#from models.category import Category

class Professors:
    def __init__(self, id, name, gradeAverage, passPercentage):
        self.id = id
        self.name = name
        self.gradeAverage = gradeAverage
        self.passPercentage = passPercentage

def listProfessors(pattern):
    conn = db_connection()
    cur = conn.cursor()
    #cur.execute('SELECT todos.id as tid, todo_text, categories.id as cid, category_name FROM todos JOIN categories ON todos.category_id = categories.id')
    cur.execute('SELECT * FROM professors WHERE name ~* %s', (pattern,))
    db_professors = cur.fetchall()
    professors = []
    for professor_entry in db_professors:
        professors.append(professor_entry)

    conn.close()
    return professors