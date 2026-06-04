from database import db_connection

class Courses:
     def __init__(self, id, name, number_of_students, grade_format, grade_average, pass_percentage, exam_type):
         self.id = id
         self.name = name
         self.number_of_students = number_of_students
         self.grade_format = grade_format
         self.grade_average = grade_average
         self.pass_percentage = pass_percentage
         self.exam_type = exam_type


def list_courses(professor):
     print("another test")
     conn = db_connection()
     cur = conn.cursor()
     cur.execute('''SELECT * 
                    FROM Courses 
                    JOIN CourseHasProfessor ON Courses.id = CourseHasProfessor.course_id
                    WHERE professor_id=%s''', professor)
     db_professor_courses = cur.fetchall()

     professor_courses = []
     for db_professor_course in db_professor_courses:
         professor_courses.append(Courses(
                                    db_professor_course[0], 
                                    db_professor_course[1], 
                                    db_professor_course[2],
                                    db_professor_course[3],
                                    db_professor_course[4],
                                    db_professor_course[5], 
                                    db_professor_course[6])
                                )
     conn.close()
     print(professor_courses[0].name)
     return professor_courses
     

