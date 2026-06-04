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
    <p>For our project, we have created a simple web application to search for KU professors and find the courses that they teach.
    For each professor, we display their weighted overall grade average and pass percentage.</p>
    <p>It is just a proof of concept, since the database consists of just a sample of the data from the official KU website.
    Ideally, we would scrape the KU website to populate the database with much more data, but we did not quite have enough time to implement a scraper.</p>
    <p>Click the button below to go to the professor search page.</p>

    <a href="/professorSearch?professor_name=" class="nav-button">
        <button>Search for KU professors</button>
    </a>
    """
