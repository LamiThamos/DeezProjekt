from database import db_connection, init_db

init_db()

conn = db_connection()
cur = conn.cursor()

cur.execute("SELECT * FROM Courses")
courses = cur.fetchall()

print(courses)

cur.close()
conn.close()