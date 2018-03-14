CMD=$1

USERNAME=cddadmin
KEYFILE=./cluster-ssh-privkey
nodelist=( 	hdp-an01.clouddatadojo.com \
			hdp-en01.clouddatadojo.com \
			hdp-mn01.clouddatadojo.com \
			hdp-mn02.clouddatadojo.com \
			hdp-mn03.clouddatadojo.com \
			hdp-sn01.clouddatadojo.com \
			hdp-sn02.clouddatadojo.com \
			hdp-sn03.clouddatadojo.com )

for i in "${nodelist[@]}"
do
	CMD="ssh -i $KEYFILE $FILE $USERNAME@$i "$1""
	echo $CMD
	$CMD
done


