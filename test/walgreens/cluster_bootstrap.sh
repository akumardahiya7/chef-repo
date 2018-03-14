KEYFILE=./priv-akhanolk
USERNAME=cddadmin

#CMD="knife bootstrap --sudo -i ./cluster-ssh-privkey -x cddadmin -r role['ambari-server'] -j '{ "ambari" : { "database" : { "type" : "mysql", "host" : "hdp-db01", "port" : "3306", "name" : "ambari", "username" : "ambari", "password": "bigdata" } } }' -N hdp-an01 hdp-an01.clouddatadojo.com"

#CMD="knife bootstrap --sudo  -i cluster-ssh-privkey -x cddadmin -r role['ambari-server'] -j '{"ambari": {"database": {"username": "ambari", "name":"ambari", "host": "hdp-db01", "password": "bigdata", "type": "mysql", "port":3306}}}' hdp-an01"

#CMD="knife bootstrap --sudo  -i $KEYFILE -x $USERNAME -r role['ambari-server']  hdp-an01.gombe.com"
#echo "$CMD"
#$CMD

nodelist=( hdp-an01  hdp-en01 hdp-mn01 hdp-mn02 hdp-mn03 hdp-sn01 hdp-sn02 hdp-sn03 )
#nodelist=( hdp-en01.gombe.com hdp-mn01.gombe.com hdp-mn02.gombe.com hdp-mn03.gombe.com hdp-sn01.gombe.com hdp-sn02.gombe.com hdp-sn03.gombe.com )
for i in "${nodelist[@]}"
do
	CMD="knife bootstrap --sudo  -i $KEYFILE -x $USERNAME -r role['ambari-agent'] $i"
	echo "$CMD"
	$CMD
done


