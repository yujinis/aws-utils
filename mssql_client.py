import pymssql
import pyodbc

c64 = """
aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggg
"""

rc64 = c64.reverse()

c256 = """
aaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffggggaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffggggaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffggggaaaaaaaaaabbbbbbbbbbccccccccccddddddddddeeeeeeeeeeffffffffffgggg
"""

rc256 = c256.reverse()

text = """
ああああああああああいいいいいいいいいいううううううううううええええええええええおおおおおおおおおおああああああああああいいいいいいいいいいううううううううううええええええええええおおおおおおおおおお
"""

rtext = text.reverse()

class PyComm:
    def __init__(self,t1=0,t2=0):
        self.insert_sleep = t1
        self.inserts_sleep = t2

    def sleep_each_insert(self):
        sleep(self.insert_sleep)

    def sleep_each_inserts(self):
        sleep(self.inserts_sleep)

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
        return pyodbc.connect("DRIVER={SQL Server};SERVER={0};UID={2};PWD={3};DATABASE={4}".format(h,p,u,w,d))
    
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
            self.insert_data_unit(self,cnn,i):

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
            self,update_data_unit(rev=True,cnn,i)
            self.sleep_each_insert()

    def update_data_unit(self,rev=False,,cnn,i):
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

#db = PyMSSQL()
db = PyODBC()
cnn = db.create_connection()
#db.create_database()
db.create_table(cnn)
db.insert_data(cnn)
db.update_data(cnn)

