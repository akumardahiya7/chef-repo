KEYFILE=./priv-akhanolk
USERNAME=cddadmin

CMD="knife bootstrap --sudo  -i $KEYFILE -x $USERNAME -r role['ambari-server']  hdp-an01.gombe.com"
echo "$CMD"
$CMD

nodelist=( hdp-en01.gombe.com hdp-mn01.gombe.com hdp-mn02.gombe.com hdp-mn03.gombe.com hdp-sn01.gombe.com hdp-sn02.gombe.com hdp-sn03.gombe.com )
for i in "${nodelist[@]}"
do
	CMD="knife bootstrap --sudo  -i $KEYFILE -x $USERNAME -r role['ambari-agent'] $i"
	echo "$CMD"
	$CMD
done


