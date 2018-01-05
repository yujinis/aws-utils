for i in $(seq 1 2000000); do
    mysql -h xxx.abcdefghij.ap-northeast-1.rds.amazonaws.com -u xxxx  -pxxxxxxxx < insert.sql
done
