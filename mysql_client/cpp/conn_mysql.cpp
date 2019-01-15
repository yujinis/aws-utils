#include <iostream>
#include <sstream>
#include <vector>
#include <thread>
#include <mutex>
#include <condition_variable>

#include <driver/mysql_driver.h>
#include <driver/mysql_connection.h>

#include <cppconn/driver.h>
#include <cppconn/exception.h>
#include <cppconn/statement.h>
#include <cppconn/resultset.h>

#include <stdlib.h>
#include <time.h>
#include <math.h>

#include "mysql_config.hpp"

using namespace std;

const int ROW = 1*1000*1000;
const int THR = 10;
const int BAR = 50;

int GRA = (int)sqrt(sqrt(ROW));

mutex mtx;
condition_variable cv;

string rs(int n){
	ostringstream o;
	for(int i=0;i<n;i++){
		int r = rand()%26+65;
		o << (char)r;
	}
	return o.str();
}

void do_query(sql::Driver *driver, int s, int e, int* c){

	sql::Connection *con;
	sql::Statement *stmt;

	con = driver->connect(HOST, USER, PASSWORD);
	con->setSchema(DB);

	stmt = con->createStatement();

	int t = 0;
	for(int i=s;i<e;i++){
		ostringstream sql;
		sql << "INSERT INTO t2 (col2, col3) VALUES (" << i << ", '" << rs(32) << "')";
		stmt->execute(sql.str());
		if(i%GRA == 0){
			mtx.lock();
			*c += i-s-t;
			cv.notify_all();
			mtx.unlock();
			t = i-s;
		}
	}

	if(t<(e-s)){
		mtx.lock();
		*c += e-s-t;
		cv.notify_all();
		mtx.unlock();
	}

	delete stmt;
	delete con;

}

void do_count(int* c, time_t start){

	unique_lock<mutex> lk(mtx);
	time_t end;

	while(1){
		cv.wait(lk);
		cout << "[";

		for(int i=0; i< ((*c)*100/ROW)/(100/BAR); i++ ){
			cout << "#";
		}

		for(int i=0; i< BAR-((*c)*100/ROW)/(100/BAR); i++ ){
			cout << " ";
		}

		end = time(NULL);
		cout << "] " << *c << " [" << (*c)*100/ROW << "%] (/" << ROW << ") : " << end-start << "s " << *c/(end-start==0?1:end-start) << "qps\r" << flush;

		if(ROW<=*c) break;
	}

	cout << endl;
}

int main() {
	cout << HOST << ", " << USER << ", " << PASSWORD << ", " << DB << endl;

	//sql::ResultSet *res;

	srand(time(NULL));

	try {
		sql::Driver *driver;
		sql::Connection *con;

		driver = sql::mysql::get_driver_instance();
		con = driver->connect(HOST, USER, PASSWORD);
		con->setSchema(DB);

		sql::Statement *stmt;

		stmt = con->createStatement();
		stmt->execute("DROP TABLE IF EXISTS t2");
		stmt->execute("CREATE TABLE t2 (col1 integer NOT NULL PRIMARY KEY AUTO_INCREMENT, col2 integer, col3 varchar(256))");

		delete stmt;

		time_t start = time(NULL);
		vector<thread> threads;

		int c = 0;
		for(int i=0;i<THR;i++){
			int s = ROW/THR*i;
			int e = ROW/THR*(i+1);
			threads.push_back(thread(do_query,driver,s,e,&c));
		}

		threads.push_back(thread(do_count,&c,start));

		for(int i=0;i<THR+1;i++){
			threads[i].join();
		}

		delete con;

	} catch (sql::SQLException &e) {
		cout << e.what() << endl;
	} catch (runtime_error &e) {
		cout << e.what() << endl;
	}

	return 0;
}

