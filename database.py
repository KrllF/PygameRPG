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

    if player_data:
        current_play_time = player_data[2]  # Индекс 2 соответствует столбцу play_time
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


