import sqlite3
import bcrypt as bc
import pytest
import project


@pytest.fixture
def create_db():
    with sqlite3.connect(":memory:") as con:
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

        yield con

@pytest.fixture
def create_user(create_db):
    con = create_db
    username = "test"
    password = "secret"

    hashed = password.encode("utf-8")
    hashed = bc.hashpw(hashed, bc.gensalt())

    cur = con.cursor()
    cur.execute(
        "INSERT INTO users (user_name, user_password) VALUES (?, ?);",
        (username, hashed),
    )
    con.commit()


def test_login_user(create_user):
    assert project.login(username="test", password="secret") == 0
    assert project.login(username="test", password="worng") == 2
    assert project.login(username="not exist", password="secret") == 1


def test_register_user():