from flask import Flask
from database import init_db, add_triggers, seed_db
from controllers import professorSearch, courseList

init_db()
add_triggers()
seed_db()

app = Flask(__name__)

app.register_blueprint(professorSearch.bp)
app.register_blueprint(courseList.bp)

@app.route("/")
def hello_world():
    return """
    <h1>Welcome to our DIS Project!</h1>
    <p>Our project is about searching for...</p>
    <p>Click the button below to go to the professor search page.</p>

    <a href="/professorSearch">
        <button>Search for KU professors</button>
    </a>
    """
