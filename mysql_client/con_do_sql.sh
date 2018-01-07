if [ $# -lt 4 ] ; then
	echo "$0 host user pass (concurs)"
	exit -1
fi

c=${5:-1}

for c in $(seq 1 $c); do 
    bash do_sql.sh $1 $2 $3 $4 &
done

