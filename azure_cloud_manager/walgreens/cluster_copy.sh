FILE=$1
KEYFILE=./priv-akhanolk
USERNAME=cddadmin
nodelist=( hdp-an01.gombe.com hdp-mn01.gombe.com hdp-mn02.gombe.com hdp-mn03.gombe.com hdp-sn01.gombe.com hdp-sn02.gombe.com hdp-sn03.gombe.com )
for i in "${nodelist[@]}"
do
	echo "scp -i $KEYFILE $FILE $USERNAME@$i:~/."
	scp -i $KEYFILE $FILE $USERNAME@$i:~/.
done


