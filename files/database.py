import sqlite3

class LanguageDatabase:
    def __init__(self, filename="language.db"):
        self.con = sqlite3.connect(filename)
        self.cur = self.con.cursor()

        self.cur.execute("CREATE TABLE IF NOT EXISTS data(id INTEGER, language TEXT)")

    def close(self):
        self.cur.close()
        self.con.close()

    def get_user_language(self, username):
        lang = self.cur.execute("SELECT language FROM data WHERE id = ?", [username]).fetchone()

        return lang[0] if lang else None

    def client_list(self):
        users = self.cur.execute("SELECT id FROM data ORDER BY id").fetchall()

        return [user[0] for user in users]

    def set_user_language(self, username, language):
        self.cur.execute('SELECT * FROM data WHERE id = ?', [username])
        user = self.cur.fetchone()

        if user:
            # Update the user's information if they are already registered
            self.cur.execute('''
                UPDATE data
                SET language = ?
                WHERE id = ?
                ''', (language, username))
        else:
            # Insert a new user if they are not registered
            self.cur.execute('''
                INSERT INTO data (id, language)
                VALUES (?, ?)
                ''', (username, language))

        self.con.commit()
