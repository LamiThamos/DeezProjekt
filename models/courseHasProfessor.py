# from database import db_connection

# class CourseHasProfessor:
#     def __init__(self, id, name):
#         self.id = id
#         self.name = name

# def list_categories():
#     conn = db_connection()
#     cur = conn.cursor()
#     cur.execute('SELECT id, category_name FROM categories')
#     db_categories = cur.fetchall()

#     categories = []
#     for db_category in db_categories:
#         categories.append(Category(db_category[0], db_category[1]))
#     conn.close()
#     return categories

# def insert_relation(course_id, professor_id, is_course_responsible):
#     conn = db_connection()
#     cur = conn.cursor()

#     cur.execute('INSERT INTO CourseHasProfessor (CourseID, ProfessorID, IsCourseResposible) VALUES (%s, %s, %b) ON CONFLICT DO NOTHING', (course_id, professor_id, is_course_responsible))
#     conn.commit()
#     conn.close()


#from database import db_connection
#from models.category import Category
#
#class Todo:
#    def __init__(self, id, text, category):
#        self.id = id
#        self.text = text
#        self.category = category
#
#def list_todos():
#    conn = db_connection()
#    cur = conn.cursor()
#    cur.execute('SELECT todos.id as tid, todo_text, categories.id as cid, category_name FROM todos JOIN categories ON todos.category_id = categories.id')
#    db_todos = cur.fetchall()
#    todos = []
#    for db_todo in db_todos:
#        todos.append(Todo(db_todo[0], db_todo[1], Category(db_todo[2], db_todo[3])))
#
#    conn.close()
#    return todos
#
#def insert_todo(text, category_id):
#    conn = db_connection()
#    cur = conn.cursor()
#    cur.execute('INSERT INTO todos (todo_text, category_id) VALUES (%s, %s) ON CONFLICT DO NOTHING', (text, category_id))
#    cur.close()
#    conn.commit()
#    conn.close()


