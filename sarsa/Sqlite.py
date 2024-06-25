import sqlite3
from json import dumps


class YanSQLite:


    def __init__(self, db_name = "sarsa.db", ):


        # connecting to the database
        self.connection = sqlite3.connect(db_name)

        # cursor
        self.crsr = self.connection.cursor()

        self.table_name = "Q_VALUE"
        self.collumns = [("'state' ", "TEXT, "),
                         ("'n1' ", "REAL, "),
                         ("'n2' ", "REAL, "),
                         ("'n3' ", "REAL, "),
                         ("'n4' ", "REAL, "),
                         ("'n5' ", "REAL, "),
                         ("'n6' ", "REAL, "),
                         ("'q' ", "REAL, "),
                         ("'f' ", "REAL, "),
                         ("'s' ", "REAL, "),
                         ("'s_' ", "REAL, "),
                         ("'x' ", "REAL, "),
                         ("'x_' ", "REAL, "),
                         ("'y' ", "REAL")]

        # SQL command to create a table in the database
        sql_command = f"CREATE TABLE IF NOT EXISTS {self.table_name} ("
        for collumn in self.collumns:
            sql_command += collumn[0] + collumn[1]
        sql_command += ");"

        # execute the statement
        self.crsr.execute(sql_command)
        self.connection.commit()

        # print("Connected to the database")


    def insert_state(self, state, n1, n2, n3, n4, n5, n6, q, f, s, s_, x, x_, y):
        sql_command = f"""INSERT INTO {self.table_name} VALUES (
                        '{state}', 
                        '{n1}', 
                        '{n2}', 
                        '{n3}', 
                        '{n4}', 
                        '{n5}', 
                        '{n6}', 
                        '{q}', 
                        '{f}', 
                        '{s}', 
                        '{s_}', 
                        '{x}', 
                        '{x_}', 
                        '{y}')"""
        
        retorno = self.crsr.execute(sql_command)
        self.connection.commit()
        return retorno

    def save_state(self, state, actions):
        n1 = actions[0]
        n2 = actions[1]
        n3 = actions[2]
        n4 = actions[3]
        n5 = actions[4]
        n6 = actions[5]
        q = actions[6]
        f = actions[7]
        s = actions[8]
        s_ = actions[9]
        x = actions[10]
        x_ = actions[11]
        y = actions[12]
        sql_command = F"SELECT * FROM {self.table_name} WHERE state LIKE '{state}'"
        self.crsr.execute(sql_command)
        returned_state = self.crsr.fetchall()
        if len(returned_state) == 0:
            self.insert_state(state, n1, n2, n3, n4, n5, n6, q, f, s, s_, x, x_, y)
        else:
            self.update_state(state, n1, n2, n3, n4, n5, n6, q, f, s, s_, x, x_, y)
        return returned_state
    

    def update_state(self, state, n1, n2, n3, n4, n5, n6, q, f, s, s_, x, x_, y):
        sql_command = f"""UPDATE {self.table_name} SET 
                        n1 = {n1},
                        n2 = {n2},
                        n3 = {n3},
                        n4 = {n4},
                        n5 = {n5},
                        n6 = {n6},
                        q = {q},
                        f = {f},
                        s = {s},
                        s_ = {s_},
                        x = {x},
                        x_ = {x_},
                        y = {y}
                        WHERE state LIKE '{state}' """
        return self.crsr.execute(sql_command).connection.commit()


    def select_all(self):
        sql_command = f"SELECT * FROM {self.table_name}"
        self.crsr.execute(sql_command)
        all = self.crsr.fetchall()
        q_value = {}
        for row in all:
            q_value[row[0]] = [
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                row[7],
                row[8],
                row[9],
                row[10],
                row[11],
                row[12],
                row[13]
                ]
        return q_value

    def close_connection(self):
        # close the connection
        self.connection.close()

if __name__ == "__main__":
    database = YanSQLite()
    database.select_all()