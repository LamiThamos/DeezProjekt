from database import db_connection
#from models.category import Category

class professors:
    def __init__(self, id, text, category):
        self.id = id
        self.text = text
        self.category = category

def listProfessors():
    conn = db_connection()
    cur = conn.cursor()
    #cur.execute('SELECT todos.id as tid, todo_text, categories.id as cid, category_name FROM todos JOIN categories ON todos.category_id = categories.id')
    cur.execute('SELECT name FROM professors')
    db_professors = cur.fetchall()
    professors = []
    for professor_entry in db_professors:
        professors.append(db_professors[0])

    conn.close()
    return professors



#def insert_todo(text, category_id):
#    conn = db_connection()
#    cur = conn.cursor()
#    cur.execute('INSERT INTO todos (todo_text, category_id) VALUES (%s, %s) ON CONFLICT DO NOTHING', (text, category_id))
#    cur.close()
#    conn.commit()
#    conn.close()
