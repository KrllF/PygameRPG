import sqlite3

db = sqlite3.connect("statistics.db")

cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users
    (player_id INTEGER PRIMARY KEY,
    kills BIGINT,
    play_time BIGINT,
    number_of_attempts BIGINT,
    max_kills BIGINT
)""")

db.close()


def add_player(player_id):
    db = sqlite3.connect("statistics.db")
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE player_id=?", (player_id,))
    existing_player = cursor.fetchone()

    if existing_player is None:
        cursor.execute(
            "INSERT INTO users (player_id, kills, play_time, number_of_attempts, max_kills) VALUES (?, 0, 0, 0, 0)",
            (player_id,))
        db.commit()

    db.close()


# kill
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


# time

def update_play_time(player_id, new_play_time):
    db = sqlite3.connect("statistics.db")
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE player_id=?", (player_id,))
    player_data = cursor.fetchone()
    new_play_time //= 1000
    if player_data:
        current_play_time = player_data[2]
        new_total_play_time = current_play_time + new_play_time

        cursor.execute("UPDATE users SET play_time=? WHERE player_id=?", (new_total_play_time, player_id))
        db.commit()

    db.close()


def reset_play_time(player_id):
    db = sqlite3.connect("statistics.db")
    cursor = db.cursor()

    cursor.execute("UPDATE users SET play_time=0 WHERE player_id=?", (player_id,))
    db.commit()

    db.close()


def get_play_time(player_id):
    db = sqlite3.connect("statistics.db")
    cursor = db.cursor()

    cursor.execute("SELECT play_time FROM users WHERE player_id=?", (player_id,))
    play_time = cursor.fetchone()

    db.close()

    if play_time:
        return play_time[0]
    else:
        return 0


# number of attempts

def update_number_of_attempts(player_id):
    db = sqlite3.connect("statistics.db")
    cursor = db.cursor()

    cursor.execute("UPDATE users SET number_of_attempts=number_of_attempts+1 WHERE player_id=?", (player_id,))
    db.commit()

    db.close()


def reset_number_of_attempts(player_id):
    db = sqlite3.connect("statistics.db")
    cursor = db.cursor()

    cursor.execute("UPDATE users SET number_of_attempts=0 WHERE player_id=?", (player_id,))
    db.commit()

    db.close()


def get_number_of_attempts(player_id):
    db = sqlite3.connect("statistics.db")
    cursor = db.cursor()

    cursor.execute("SELECT number_of_attempts FROM users WHERE player_id=?", (player_id,))
    number_of_attempts = cursor.fetchone()

    db.close()

    if number_of_attempts:
        return number_of_attempts[0]
    else:
        return 0


# max kills

def update_max_kills(player_id, new_kills):
    db = sqlite3.connect("statistics.db")
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE player_id=?", (player_id,))
    player_data = cursor.fetchone()

    if player_data:
        current_max_kills = player_data[3]
        if new_kills > current_max_kills:
            cursor.execute("UPDATE users SET max_kills=? WHERE player_id=?", (new_kills, player_id))
            db.commit()

    db.close()


def reset_max_kills(player_id):
    db = sqlite3.connect("statistics.db")
    cursor = db.cursor()

    cursor.execute("UPDATE users SET max_kills=0 WHERE player_id=?", (player_id,))
    db.commit()

    db.close()


def get_max_kills(player_id):
    db = sqlite3.connect("statistics.db")
    cursor = db.cursor()

    cursor.execute("SELECT max_kills FROM users WHERE player_id=?", (player_id,))
    max_kills = cursor.fetchone()

    db.close()

    if max_kills:
        return max_kills[0]
    else:
        return 0
