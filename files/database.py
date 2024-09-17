import sqlite3

def __init__():
    global con
    global cur
    con = sqlite3.connect("language.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS data(id TEXT, language TEXT)") 
    con.commit()
def findlanguage(username):
    global lang
    lang = list(cur.execute("SELECT language FROM data WHERE id = ?", [username]).fetchall())
    print(type(lang))
    return lang


def addlanguage(username, language):
    print ("test-1")
    cur = con.cursor()
    cur.execute('SELECT * FROM data WHERE id = ?', [username])
    user = cur.fetchone()
    print("test0")
    
    if user:
        print("test1")
        # Update the user's information if they are already registered
        cur.execute('''
        UPDATE data
        SET language = ?
        WHERE id = ?
        ''', (language, username))
    else:
        print("test2")
        # Insert a new user if they are not registered
        cur.execute('''
        INSERT INTO data (id, language)
        VALUES (?, ?)
        ''', (username, language))
    con.commit()