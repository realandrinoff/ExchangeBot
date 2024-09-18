import sqlite3

def __init__():
    global con
    global cur
    con = sqlite3.connect("language.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS data(id INTEGER, language TEXT)") 
    con.commit()
def findlanguage(username):
    lang = list(cur.execute("SELECT language FROM data WHERE id = ?", [username]).fetchall())
    return lang
def clientlist():
    users = cur.execute("SELECT id FROM data").fetchone()
    return users

def addlanguage(username, language):
    cur = con.cursor()
    cur.execute('SELECT * FROM data WHERE id = ?', [username])
    user = cur.fetchone()
    
    if user:
        # Update the user's information if they are already registered
        cur.execute('''
        UPDATE data
        SET language = ?
        WHERE id = ?
        ''', (language, username))
    else:
        # Insert a new user if they are not registered
        cur.execute('''
        INSERT INTO data (id, language)
        VALUES (?, ?)
        ''', (username, language))
    con.commit()