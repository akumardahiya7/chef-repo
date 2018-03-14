FILE=$1
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
	echo "scp -i $KEYFILE $FILE $USERNAME@$i:~/."
	scp -i $KEYFILE $FILE $USERNAME@$i:~/.
done


