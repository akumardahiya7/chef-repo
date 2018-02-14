CMD=$1
KEYFILE=./priv-akhanolk
USERNAME=cddadmin
nodelist=( hdp-an01.gombe.com hdp-en01.gombe.com hdp-mn01.gombe.com hdp-mn02.gombe.com hdp-mn03.gombe.com hdp-sn01.gombe.com hdp-sn02.gombe.com hdp-sn03.gombe.com )
#nodelist=( hdp-an01.gombe.com hdp-mn01.gombe.com hdp-mn02.gombe.com hdp-mn03.gombe.com hdp-sn01.gombe.com )
for i in "${nodelist[@]}"
do
	CMD="ssh -i $KEYFILE $FILE $USERNAME@$i "$1""
	echo $CMD
	$CMD
done


