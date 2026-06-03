from database import db_connection, init_db

def test_can_connect_to_database():
    conn = db_connection()
    cur = conn.cursor()

    cur.execute("SELECT 1;")

    cur.close()
    conn.close()


def test_init_db():
    init_db()