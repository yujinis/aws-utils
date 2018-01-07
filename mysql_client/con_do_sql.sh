if [ $# -lt 4 ] ; then
	echo "$0 host user pass (concurs)"
	exit -1
fi

c=$(4:-1}

for c in $(seq 1 $4); do 
    do_sql.sh $1 $2 $3 &
done

