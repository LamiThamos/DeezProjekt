from flask import Blueprint, render_template, request
from models.Courses import list_courses
from models.Professors import get_professor_by_id

bp = Blueprint('courseList', __name__, url_prefix='/')

@bp.route('/courseList', methods=['GET'])
def course_list():
    print("testing get")
    professor_id = request.args.get("professor_id")
    print(professor_id)
    courses = list_courses(professor_id)
    print(courses)
    professor = get_professor_by_id(professor_id)

    return render_template('courseList.html', courses=courses, professor=professor)
