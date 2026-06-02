from flask import Flask
from database import init_db
from controllers import professorSearch, courseList

init_db()

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

app.register_blueprint(professorSearch.bp)
app.register_blueprint(courseList.bp)
