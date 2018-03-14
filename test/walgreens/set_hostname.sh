CMD=$1
KEYFILE=./cluster-ssh-privkey
USERNAME=cddadmin
nodelist=(  hdp-db01.clouddatadojo.com \
		 	hdp-an01.clouddatadojo.com \
			hdp-en01.clouddatadojo.com \
			hdp-mn01.clouddatadojo.com \
			hdp-mn02.clouddatadojo.com \
			hdp-mn03.clouddatadojo.com \
			hdp-sn01.clouddatadojo.com \
			hdp-sn02.clouddatadojo.com \
			hdp-sn03.clouddatadojo.com )

for i in "${nodelist[@]}"
do
	CMD="ssh -i $KEYFILE $FILE $USERNAME@$i 'sudo cp hosts /etc/hosts ;  cat /etc/hosts; sudo hostnamectl set-hostname $i --static ; hostname -f '"
	echo $CMD
	#$CMD
done


