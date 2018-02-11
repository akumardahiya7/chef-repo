service  ambari-server stop
service  ambari-agent stop
service ranger-admin stop
service ranger-usersync stop
su -l knox -c "/usr/hdp/current/knox-server/bin/gateway.sh stop"
su -l oozie -c "/usr/hdp/current/oozie-server/bin/oozied.sh stop"
su -l hcat -c "/usr/hdp/current/hive-webhcat/sbin/webhcat_server.sh stop"
ps aux | awk '{print $1,$2}' | grep hive | awk '{print $2}' | xargs kill >/dev/null 2>&1
su -l hbase -c "/usr/hdp/current/hbase-regionserver/bin/hbase-daemon.sh stop regionserver"
su -l hbase -c "/usr/hdp/current/hbase-master/bin/hbase-daemon.sh stop master"
su -l yarn -c "/usr/hdp/current/hadoop-yarn-nodemanager/sbin/yarn-daemon.sh stop nodemanager"
su -l mapred -c "/usr/hdp/current/hadoop-mapreduce-historyserver/sbin/mr-jobhistory-daemon.sh stop historyserver"
su -l yarn -c "/usr/hdp/current/hadoop-yarn-timelineserver/sbin/yarn-daemon.sh stop timelineserver"
su -l yarn -c "/usr/hdp/current/hadoop-yarn-resourcemanager/sbin/yarn-daemon.sh stop resourcemanager"
su -l hdfs -c "/usr/hdp/current/hadoop-hdfs-datanode/../hadoop/sbin/hadoop-daemon.sh stop datanode"
su -l hdfs -c "/usr/hdp/current/hadoop-hdfs-namenode/../hadoop/sbin/hadoop-daemon.sh stop secondarynamenode"
su -l hdfs -c "/usr/hdp/current/hadoop-hdfs-namenode/../hadoop/sbin/hadoop-daemon.sh stop namenode"
su -l hdfs -c "/usr/hdp/current/hadoop-hdfs-namenode/../hadoop/sbin/hadoop-daemon.sh stop zkfc"
su -l hdfs -c "/usr/hdp/current/hadoop-hdfs-journalnode/../hadoop/sbin/hadoop-daemon.sh stop journalnode"
su - zookeeper -c "export ZOOCFGDIR=/usr/hdp/current/zookeeper-server/conf ; export ZOOCFG=zoo.cfg; source /usr/hdp/current/zookeeper-server/conf/zookeeper-env.sh ; /usr/hdp/current/zookeeper-server/bin/zkServer.sh stop"
/etc/init.d/hue stop
su kafka /usr/hdp/current/kafka-broker/bin/kafka stop
su atlas python /usr/hdp/current/atlas-server/bin/atlas_stop.py
yum -y remove knox*
yum -y remove ranger\*
yum -y remove kafka\*
yum -y remove storm\*
yum -y remove hive\*
yum -y remove hbase\*
yum -y remove phoenix\*
yum -y remove accumulo\*
yum -y remove tez\*
yum -y remove zookeeper\*
yum -y remove oozie\*
yum -y remove pig\*
yum -y remove snappy\* 
yum -y remove hadooplzo\*
yum -y remove knox\*
yum -y remove hadoop\*
yum -y remove extjs-2.2-1 
yum -y remove mysql-connector-java-5.0.8-1\*
