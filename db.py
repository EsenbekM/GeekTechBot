import sqlite3

class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
    
    def user_exist(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM 'users' WHERE users.user_id = ?", (user_id,)).fetchmany(1)
            return bool(len(result))
    
    def add_admin(self, user_id, group, nickname, name, count, is_admin=1):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO 'users' ('user_id', 'group', 'nickname', 'name', 'count', 'is_admin') VALUES (?, ?, ?, ?, ?, ?)", 
                (user_id, group, nickname, name, count, is_admin)
                )

    def get_admin(self):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM 'users' WHERE users.is_admin = ?", (1, )).fetchall()
            return result

    def add_user(self, user_id, group, nickname, name, count, is_admin=0):
        with self.connection:
            return self.cursor.execute(
                "INSERT INTO 'users' ('user_id', 'group', 'nickname', 'name', 'count', 'is_admin') VALUES (?, ?, ?, ?, ?, ?)", 
                (user_id, group, nickname, name, count, is_admin)
                )

    def add_count(self, user_id, name):
        with self.connection:
            new = self.cursor.execute("SELECT users.count FROM 'users' WHERE users.user_id = ?", (user_id, )).fetchmany(1)
            newv2 = new[0][0] + 1
            return self.cursor.execute("UPDATE 'users' SET 'count' = ? WHERE users.user_id = ?", (newv2, user_id)),\
                self.cursor.execute("UPDATE 'users' SET 'name' = ? WHERE users.user_id = ?", (name, user_id))

    def set_active(self, user_id, active):
        with self.connection:
            return self.cursor.execute("UPDATE 'users' SET 'active' = ? WHERE users.user_id = ?", (active, user_id))

    def get_users(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM 'users' WHERE users.is_admin = ?", (0, )).fetchall()
        
    def clear_table(self):
        with self.connection:
            return self.cursor.execute("DELETE FROM 'users' WHERE users.is_admin = ?", (0, ))

    def clear_all(self):
        with self.connection:
            return self.cursor.execute("DELETE FROM 'users'")
    
    def all_amount(self):
        with self.connection:
            c = self.cursor.execute("SELECT users.count FROM 'users' WHERE users.is_admin = ?", (0, )).fetchall()
            res = 0
            for i in c:
                res += i[0]
            return res
    
    def group_amount(self):
        with self.connection:
            c = self.cursor.execute("SELECT * FROM 'users' WHERE users.is_admin = ?", (0, )).fetchall()
            dct = {}
            for i in c:
                if i[2] in dct.keys():
                    dct[i[2]] += i[5]
                elif i[2] not in dct.keys():
                    dct[i[2]] = i[5]
            return dct