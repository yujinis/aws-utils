package main

import (
	"database/sql"
	"fmt"
	"math/rand"
	"math"
	"time"

	_ "github.com/go-sql-driver/mysql"
	_ "github.com/lib/pq"


	. "./config"
)

const (
	ROW = 1*1000*1000
	THR = 10
	BAR = 50
	TBL = "t2"
)

var (
	GRA = int(math.Sqrt(ROW)*10)
)

func main() {

	dsn := USER+":"+PASS+"@tcp("+HOST+":3306)/"+DB

	db, err := sql.Open("mysql", dsn)
	if err != nil {
		panic(err.Error())
	}

	fmt.Println(dsn,TBL)

	_, _ = db.Exec("DROP TABLE "+TBL)

	_, err = db.Exec("CREATE TABLE "+TBL+" (col1 integer NOT NULL PRIMARY KEY AUTO_INCREMENT, col2 integer, col3 varchar(256))")
	if err != nil {
		panic(err.Error())
	}

	db.Close()

	finalize := make(chan string)
	report := make(chan int)
	for i:=0; i < THR; i++ {
		go exec(dsn,ROW/THR*i,ROW/THR*(i+1),i,finalize,report)
	}

	go do_report(finalize,report)

	m := 0 
	for {
		_ = <- finalize
		m += 1
		if m == THR+1 { break }
	}
	fmt.Println("\nFinished.")

}

func exec(dsn string, s,e,id int, finalize chan string, report chan int){

	db, err := sql.Open("mysql", dsn)
	if err != nil {
		panic(err.Error())
	}
	defer db.Close()

	t := 0
	for i:=s; i < e; i++ {
		_, err := db.Exec(fmt.Sprintf("INSERT INTO "+TBL+" (col2, col3) VALUES (%d, '%s')",i,rsa(32)))
		if err != nil {
			panic(err.Error())
		}
		if i % ((e-s)/GRA) == 0 {
			report <- i-s-t
			t = i-s
		}
	}
	if (e-s)%GRA != 0 {
		report <- e-s-t
	}
	finalize <- "Finished."

}

func rs() string {
	rand.Seed(time.Now().UnixNano())
	return string(rand.Int63()%26+65)
}

func rsa(w int) string {
	s := ""
	for i:=0; i<w; i++ {
		s += rs()
	}
	return s
}

func do_report(finalize chan string, report chan int){
	s := time.Now()

	n := 0
	pn := 0
	for {
		n += <- report

		if ROW/GRA <= n {
			pn += n
			n = 0
			disp(pn,s)

		}

		if ROW <= pn+n {
			disp(pn+n,s)
			break
		}
	}
	finalize <- "Finished."
}

func disp(pn int, s time.Time){
	e := int(time.Since(s)/(1000*1000*1000))

	fmt.Printf("\033[2K\033[G[");
	for i:=0; i< (pn*100/ROW)/(100/BAR); i++ {
		fmt.Printf("#");
	}
	for i:=0; i< BAR-(pn*100/ROW)/(100/BAR); i++ {
		fmt.Printf(" ");
	}
	if(0<e){
		fmt.Printf("] %d [%d%%] (/%d) : %ds : %d qps",pn,(pn*100/ROW),ROW,e,pn/e)
	}

}
