import sqlite3

db = sqlite3.connect("statistics.db")

cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users
    (player_id integer,
    kills BIGINT,
    play_time BIGINT
    
)""")

db.close()


def add_player(player_id):
    db = sqlite3.connect("statistics.db")
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE player_id=?", (player_id,))
    existing_player = cursor.fetchone()

    if existing_player is None:
        cursor.execute("INSERT INTO users (player_id, kills, play_time) VALUES (?, 0, 0)", (player_id,))
        db.commit()

    db.close()


def update_kills(player_id):
    db = sqlite3.connect("statistics.db")
    cursor = db.cursor()

    cursor.execute("UPDATE users SET kills=kills+1 WHERE player_id=?", (player_id,))
    db.commit()

    db.close()

def reset_kills(player_id):
    db = sqlite3.connect("statistics.db")
    cursor = db.cursor()

    cursor.execute("UPDATE users SET kills=0 WHERE player_id=?", (player_id,))
    db.commit()

    db.close()


def get_kills(player_id):
    db = sqlite3.connect("statistics.db")
    cursor = db.cursor()

    cursor.execute("SELECT kills FROM users WHERE player_id=?", (player_id,))
    kills = cursor.fetchone()

    db.close()

    if kills:
        return kills[0]
    else:
        return 0


