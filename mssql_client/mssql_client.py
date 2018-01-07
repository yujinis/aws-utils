# encoding:utf-8

#import pymssql
import pyodbc
import sys,time
import multiprocessing as mp

iter_count = 100000

c64 = "aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggg"

rc64 = c64[::-1]

c256 = "aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffggggaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffggggaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffggggaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggg"

rc256 = c256[::-1]

text = "ああああああああああいいいいいいいいいいううううううううううええええええええええおおおおおおおおおおああああああああああいいいいいいいいいいううううううううううええええええええええおおおおおおおおおお"

rtext = text[::-1]

class PyComm:
    def __init__(self,t1=0,t2=0):
        self.mode = "test"
        self.insert_sleep = t1
        self.inserts_sleep = t2

    def sleep_each_insert(self):
        time.sleep(self.insert_sleep)

    def sleep_each_inserts(self):
        time.sleep(self.inserts_sleep)

    def get_iter_count(self):
        if self.mode == "test":
            return 2
        else:
            return iter_count

class PyMSSQL(PyComm):

    def __init__(self,t1=0,t2=0):
        super().__init__(t1,t2)

    def create_connection(self,h,u,w,d):
        return db.create(host=h,port=p,user=u,password=w,database=d)
    
    def create_databsase(self,conn):
        conn.execute("CREATE DATABASE test_db IF NOT EXIST");


class PyODBC(PyComm):

    def __init__(self,t1=0,t2=0):
        super().__init__(t1,t2)

    def create_connection(self,dsn,u,w,d):
        print("create_connection")
        return pyodbc.connect("DSN={0};UID={1};PWD={2};DATABASE={3}".format(dsn,u,w,d), timeout=10)
    
    def create_databsase(self,conn):
        conn.execute("CREATE DATABASE test_db IF NOT EXIST");
 
    def drop_table(self,conn):
        print("drop_table")
        try:
            cur = conn.cursor()
            cur.execute("DROP TABLE test_table")
            conn.commit()
        except:
            pass

    def create_table(self,conn):
        print("create_table")
        cur = conn.cursor()
        try:
            cur.execute("""
            CREATE TABLE test_table (
                a_int INT NOT NULL,
                b_char CHAR(64),
                c_char CHAR(256),
                d_nvarchar NVARCHAR(256),
                PRIMARY KEY (a_int)
            )
            """)
        except pyodbc.ProgrammingError as e:
            print(e)
            if "There is already an object" in e.args[1]:
                pass
            else:
                sys.exit(-1)
        else:
            conn.commit()

    def insert_data(self,conn):
        print("insert_data : {0}".format(self.get_iter_count()))
        for i in range(self.get_iter_count()):
            self.insert_data_unit(conn,i)

    def insert_data_unit(self,conn,i):
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO test_table (
            a_int,
            b_char,
            c_char,
            d_nvarchar) VALUES (
            {0},'{1}','{2}','{3}'
        )
        """.format(i,c64,c256,text))
        conn.commit()

    def update_data(self,conn):
        print("update_data : {0}".format(self.get_iter_count()))
        for i in range(self.get_iter_count()):
            self.update_data_unit(conn,i)
            self.sleep_each_insert()

        self.sleep_each_inserts()

        for i in range(self.get_iter_count()):
            self.update_data_unit(conn,i,rev=True)
            self.sleep_each_insert()

    def update_data_unit(self,conn,i,rev=False):
        if rev:
            _c64  = rc64
            _c256 = rc256
            _text = rtext
        else:
            _c64  = c64
            _c256 = c256
            _text = text

        cur = conn.cursor()
        conn.execute("""
        UPDATE test_table SET
        b_char='{0}',
        c_char='(1)',
        d_nvarchar='(2)'
        WHERE a_int = {3}
        """.format(_c64,_c256,_text,i))
        conn.commit()


def job_db():
    #db = PyMSSQL()
    db = PyODBC()
    #db.mode = "real"
    conn = db.create_connection(*sys.argv[1:])
    #db.create_database()
    db.drop_table(conn)
    db.create_table(conn)
    db.insert_data(conn)
    db.update_data(conn)

if __name__ == "__main__":

    #print(len(c64))
    #print(len(c256))
    #print(len(rtext))

    if 4 < len(sys.argv):
        if 5 < len(sys.argv):
            # Multi processes
            jobs = []
            for i in range(sys.argv[5]):
                job = mp.Process(target=job_db)
                jobs.append(job)
                job.start()

            # Will wait until all jobs end.
            for job in jobs:
                job.join()

        else:
            # Single process
            job_db()

    else:
        print("(For pyodbc) python "+sys.argv[0]+" DSN root pass database")


