from flask import Blueprint, render_template, request
from models.Professors import list_professors

bp = Blueprint('professorSearch', __name__, url_prefix='/')

@bp.route('/professorSearch', methods=['GET'])
def professor_search():
  
    professor_name = request.args.get("professor_name")
    print(professor_name)
    professors = list_professors(professor_name)
    print(professors)

    return render_template('professorSearch.html', professors=professors)


