[ $# -ne 3 ] && exit -1
mysql -h $1 -u $2 -p${3} < create.sql

