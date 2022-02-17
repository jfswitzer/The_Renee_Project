#!/usr/bin/env python3
"""
junkyard storage code
"""
import socket
import json
import sqlite3 as sl

#https://www.sqlitetutorial.net/sqlite-python/create-tables/
def create_connection(db_file):
    conn = None
    try:
        conn = sl.connect(db_file)
        return conn
    except:
        print('err connecting')
    return conn

def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except:
        print('err creating')
class jyd_db:
    def __init__(self):
        self.fname = 'jyd.db'
        self.conn = create_connection(self.fname)
        self.lid = 0
        sql_create = """ CREATE TABLE IF NOT EXISTS kvstore (
                                        id INTEGER PRIMARY KEY, key text, value text
                                    ); """
        create_table(self.conn,sql_create)
    def get(self,k):
        sqstring="SELECT * FROM kvstore WHERE key=?"
        #print(sqstring)
        cur = self.conn.cursor()
        cur.execute(sqstring,(k,))
        rows = cur.fetchall()
        return rows
    def put(self,kvs):
        #all puts are by nature appends
        sqstring = " INSERT INTO kvstore (id, key, value) VALUES "
        for k,v in kvs:
            sqstring=sqstring+"("+str(self.lid)+",\'"+k+"\', \'"+v+"\'), "
            self.lid += 1
        sqstring=sqstring[:-2]
        #print(sqstring)   
        self.conn.execute(sqstring)
        self.conn.commit()
    def print_me(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM kvstore")
        self.conn.commit()
        print(cur.fetchall())
    def act_on(request):
        """decode request string and implement in the kv"""
        # type : get, put
        # kvs
        resp = {'status': 1, 'ret': ''}
        req = json.loads(request)
        if req['type']=='put':
            self.put(req['kvs'])
        elif req['type']=='get':
            ret = self.get(req['key'])
            resp['ret']=ret
        return json.dumps(resp)
    def run_listener(self):
        HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
        PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    response = self.act_on(data)
                    conn.sendall(response)
# def main():
#     db = jyd_db()
#     db.put([('a','1'),('b','3')])
#     db.put([('a','2')])
#     db.print_me()
#     db.get('a')

# if __name__ == "__main__":
#     """ This is executed when run from the command line """
#     main()
