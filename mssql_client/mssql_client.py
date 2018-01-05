import pymssql
import pyodbc
import sys

ite_number = 100000

c64 = """
aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggg
"""

rc64 = c64[::-1]

c256 = """
aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffggggaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffggggaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffggggaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggg
"""

rc256 = c256[::-1]

text = """
ああああああああああいいいいいいいいいいううううううううううええええええええええおおおおおおおおおおああああああああああいいいいいいいいいいううううううううううええええええええええおおおおおおおおおお
"""

rtext = text[::-1]

class PyComm:
    def __init__(self,t1=0,t2=0):
        self.mode = "test"
        self.insert_sleep = t1
        self.inserts_sleep = t2

    def sleep_each_insert(self):
        sleep(self.insert_sleep)

    def sleep_each_inserts(self):
        sleep(self.inserts_sleep)

    def get_itarative_number(self):
        if self.mode == "test":
            return 2
        else:
            return ite_number

class PyMSSQL(PyComm):

    def __init__(self,t1=0,t2=0):
        super().__init__(t1,t2)

    def create_connection(self,h,p,u,w,d):
        return db.create(host=h,port=p,user=u,password=w,database=d)
    
    def create_databsase(self,cnn):
        cnn.execute("CREATE DATABASE test_db IF NOT EXIST");


class PyODBC(PyComm):

    def __init__(self,t1=0,t2=0):
        super().__init__(t1,t2)

    def create_connection(self,h,_,u,w,d):
        return pyodbc.connect("DSN={0};UID={1};PWD={2};DATABASE={3}".format(h,u,w,d))
    
    def create_databsase(self,cnn):
        cnn.execute("CREATE DATABASE test_db IF NOT EXIST");
 
    def create_table(self,cnn):
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE test_table IF NOT EXIST (
            a_int INT(10),
            b_varchar VARCHAR(64),
            c_varchar VARCHAR(256),
            d_text    TEXT,
            PRIMARY   KEY (a_int)
        )
        """)
        cnn.commit()

    def insert_data(self,cnn):
        for i in range(100000):
            self.insert_data_unit(self,cnn,i)

    def insert_data_unit(self,cnn,i):
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO test_table (
            a_int,
            b_varchar,
            c_varchar,
            d_text
        ) VALUES (
            {0},'{1}','{2}','{3}'
        )
        """.format(i,c64,c256,text))
        cnn.commit()

    def update_data(self,cnn):
        for i in range(100000):
            self,update_data_unit(cnn,i)
            self.sleep_each_insert()

        self.sleep_each_inserts()

        for i in range(100000):
            self,update_data_unit(cnn,i,rev=True)
            self.sleep_each_insert()

    def update_data_unit(self,cnn,i,rev=False):
        if rev:
            _c64  = rc64
            _c256 = rc256
            _text = rtext
        else:
            _c64  = c64
            _c256 = c256
            _text = text

        cur = conn.cursor()
        cnn.execute("""
        UPDATE test_table SET
        b_varchar='{0}',
        c_varchar='(1)',
        d_text='(2)'
        WHERE a_int = {3}
        """.format(_c64,_c256,_text,i))
        cnn.commit()

####################

if __name__ == "__main__":

    if 5 < len(sys.argv):

        #db = PyMSSQL()
        db = PyODBC()
        #db.mode = "real"
        cnn = db.create_connection(*sys.argv[1:])
        #db.create_database()
        db.create_table(cnn)
        db.insert_data(cnn)
        db.update_data(cnn)

    else:
        print("python "+sys.argv[0]+" xxx.abcdefg.ap-northeast-1.rds.amazonaws.com 1433 root pass database")
