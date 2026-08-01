import bcrypt as bc
import pytest
import project
import sqlite3


@pytest.fixture
def create_db():
    with sqlite3.connect("finance.db") as con:
        cur = con.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL UNIQUE,
                user_password TEXT NOT NULL
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS assets (
                asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                asset_ticker TEXT NOT NULL,
                asset_amount REAL NOT NULL,
                asset_price REAL NOT NULL,
                asset_date DATE DEFAULT CURRENT_DATE,
                created_at DATE DEFAULT CURRENT_DATE,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            );
        """)

        con.commit()

@pytest.fixture
def create_user():
    username = "test"
    password = "secret"

    hashed = password.encode("utf-8")
    hashed = bc.hashpw(hashed, bc.gensalt())

    with sqlite3.connect("finance.db") as con:
        cur = con.cursor()

        cur.execute("INSERT INTO users (user_name, user_password) VALUES (?, ?);", (username, hashed,))                           

        con.commit()

def test_login_user(create_db, create_user):
    assert project.login(username="test", password="secret") == 0
