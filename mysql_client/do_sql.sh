[ $# -ne 4 ] && exit -1

loop=$4
outer=10
inner=$((loop/outer))

for j in $(seq 1 $outer); do
	for i in $(seq 1 $inner); do
	    mysql -h $1 -u $2 -p${3} < insert.sql
	done
	echo "$j : $((j*inner))"
done

