import sqlite3
con = sqlite3.connect("tutorial.db", check_same_thread=False)

cur = con.cursor()


def start(user_id):
    cur.execute(f"CREATE TABLE IF NOT EXISTS users_{user_id} (user_id INTEGER, message TEXT, message_index TEXT)")

def quit_msg(user_id):
    cur.execute(f"DROP TABLE IF EXISTS users_{user_id}")

def save(info):
    cur.execute(f"INSERT INTO users_{info['user_id']} VALUES (?, ?, ?)",(str(info["user_id"]), str(info['message_text']), int(info["index"])))
    con.commit()


def delete_info_msg(info):
    cur.execute(f"DELETE FROM users_{info['user_id']} WHERE message_index = ?", (str(info["index"]),))
    con.commit()


def get_info(info):
    # We use WHERE message_index = ? to filter the rows
    cur.execute(f"SELECT message FROM users_{info['user_id']} WHERE message_index = ?", (str(info["index"]),))
    
    # fetchall() gets every row that matched the index
    results = cur.fetchall() 
    
    # We turn the list of tuples [(msg1,), (msg2,)] into a simple list ['msg1', 'msg2']
    return [row[0] for row in results]