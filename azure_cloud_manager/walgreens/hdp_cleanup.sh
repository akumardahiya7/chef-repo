#ambar-server
ambari-server stop

#Run python script on all cluster nodes
touch /var/lib/ambari-agent/data/hostcheck_custom_actions.result
python /usr/lib/python2.6/site-packages/ambari_agent/HostCleanup.py --silent



#ambari-agent
service ambari-agent stop
yum -y erase ambari-agent

rm -rf /etc/ambari-agent
rm -rf /usr/lib/python2.6/site-packages/ambari*
rm -rf /usr/lib/amrbari-agent
rm -rf /var/lib/ambari-agent
rm -rf /var/run/ambari-agent
rm -rf /var/log/ambari-agent

rm -rf /etc/chef

#ambar-server
#ambari-server stop
ambari-server reset
yum -y erase ambari-server

rm -rf /etc/ambari-server
rm -rf /usr/lib/python2.6/site-packages/ambari*
rm -rf /usr/lib/ambari-server-backups
rm -rf /usr/lib/ambari-server
rm -rf /var/lib/ambari-server
rm -rf /var/run/ambari-server
rm -rf /var/log/ambari-server

#postgresql
service postgresql stop
yum -y erase postgresql -y
rm -rf /var/lib/pgsql

#Remove Hadoop packages on all nodes


#falcon
yum -y remove "falcon*"
rm -rf /etc/falcon
rm -rf /var/run/falcon
rm -rf /var/log/falcon
rm -f /usr/bin/falcon
userdel -r falcon

#ganglia
yum -y remove "ganglia*"

#hbase
yum -y remove "hbase*"
rm -rf /etc/hbase
rm -rf /var/run/hbase
rm -rf /var/log/hbase
rm -f /usr/bin/hbase
userdel -r hbase

#hdfs
yum -y remove "hdfs*"
rm -rf /etc/hadoop
rm -rf /etc/hadoop-httpfs

rm -rf /var/lib/hadoop-hdfs
rm -rf /var/run/hadoop 
rm -rf /var/log/hadoop
rm -f /usr/bin/hdfs
userdel -r hdfs

#hive & hive2
yum -y remove "hive*"
rm -rf /etc/hive
rm -rf /etc/hive2
rm -rf /etc/hive-hcatalog
rm -rf /etc/hive-webhcat


rm -rf /var/lib/hive
rm -rf /var/lib/hive2

rm -rf /var/run/hive
rm -rf /var/run/hive2
rm -rf /var/run/hive-hcatalog
rm -rf /var/run/webhcat

rm -rf /var/log/hive
rm -rf /var/log/hive2
rm -rf /var/log/hive-hcatalog
rm -rf /var/log/webhcat

rm -f /usr/bin/hive
rm -f /usr/bin/hiveserver2
rm -f /usr/bin/hcat

userdel -r hcat
userdel -r hive

#kafka
yum -y remove kafka\*
rm -f /usr/bin/kafka
userdel -r kafka

#knox
yum -y remove knox\*
rm -rf /etc/knox
rm -rf /var/lib/knox
rm -rf /var/run/knox
rm -rf /var/log/knox
userdel -r knox

##mapred
yum -y remove "mapreduce2*"
rm -rf /var/lib/hadoop-mapreduce
rm -rf /var/run/hadoop-mapreduce
rm -rf /var/log/hadoop-mapreduce
rm -f /usr/bin/mapred
userdel -r mapred

#hst
rm -rf /var/log/hst
rm -rf /etc/hst
rm -rf /var/run/hst


#nagios
yum -y remove nagios\*

#oozie
yum -y remove oozie\*
rm -rf /etc/oozie
rm -rf /var/run/oozie 
rm -rf /var/log/oozie
rm -f /usr/bin/oozie
rm -f /usr/bin/oozied.sh
userdel -r oozie

#pig
yum -y remove pig\*
rm -rf /etc/pig
rm -rf /var/log/pig
rm -f /usr/bin/pig

#ranger
yum -y remove ranger\*
rm -rf /etc/ranger-admin
rm -rf /etc/ranger-usersync
rm -f /usr/bin/ranger-admin
rm -f /usr/bin/ranger-admin-start
rm -f /usr/bin/ranger-admin-stop
rm -f /usr/bin/ranger-kms
rm -f /usr/bin/ranger-usersync
rm -f /usr/bin/ranger-usersync-start
rm -f /usr/bin/ranger-usersync-stop
userdel -r ranger

#spark2
yum -y remove "spark2*"
rm -rf /etc/spark2
rm -rf /var/log/spark2
rm -rf /var/run/spark2
userdel -r spark

#storm
yum -y remove storm\*
rm -rf /var/lib/storm
rm -f /usr/bin/storm
rm -f /usr/bin/storm-slider
userdel -r storm

#tez
yum -y remove tez\*
rm -rf /etc/tez
rm -rf /etc/tez_hive2
rm -rf /var/run/tez
rm -rf /var/log/tez
userdel -r tez

#yarn
yum -y remove yarn\*
rm -rf /var/lib/hadoop-yarn 
rm -rf /var/run/hadoop-yarn
rm -rf /var/log/hadoop-yarn
rm -f /usr/bin/yarn
userdel -r yarn

#zookeeper
yum -y remove zookeeper\*
rm -rf /etc/zookeeper
rm -rf /var/run/zookeeper
rm -rf /var/log/zookeeper
rm -f /usr/bin/zookeeper-client
rm -f /usr/bin/zookeeper-server
rm -f /usr/bin/zookeeper-server-cleanup
userdel -r zookeeper

#smartsense
yum -y remove smartsense\*
rm -rf /var/lib/smartsense
rm -rf "/var/log/smartsense*"

# accumulo
yum -y remove accumulo\*
rm -f /usr/bin/accumulo
userdel -r accumulo

#slider
yum -y remove slider\*
rm -rf /var/log/slider
rm -f /usr/bin/slider

## ambari 

#ams
yum -y remove ams\*
rm -rf /etc/ams-hbase
rm -rf /usr/lib/ams-hbase

yum -y remove ambari-metrics\*
rm -rf /etc/ambari-metrics-grafana

rm -rf /usr/lib/ambari-metrics-hadoop-sink
rm -rf /usr/lib/ambari-metrics-kafka-sink
rm -rf /var/lib/ambari-metrics-grafana

rm -rf /var/run/ambari-metrics-grafana
rm -rf /var/log/ambari-metrics-monitor
rm -rf /var/log/ambari-metrics-grafana
userdel -r ams


#ambari-infra-solr
yum -y remove ambari-infra-solr\*
rm -rf /usr/lib/ambari-infra-solr-client
rm -rf "/var/log/ambari-infra-solr*"
rm -rf /var/log/solr


userdel -r ambari-qa


#livy
yum -y remove livy\*
rm -rf /etc/livy
rm -rf /var/log/livy

#livy2
yum -y remove livy2\*
rm -rf /etc/livy2
rm -rf /var/log/livy2

#zeppelin
yum -y remove zeppelin\*
rm -rf /var/log/zeppelin
rm -rf /etc/phoenix
rm -f /usr/bin/phoenix-psql
rm -f /usr/bin/phoenix-queryserver
rm -f /usr/bin/phoenix-sqlline
rm -f /usr/bin/phoenix-sqlline-thin
userdel -r zeppelin



#flume
rm -rf /etc/flume
rm -rf /var/lib/flume
rm -rf /var/run/flume
rm -rf /var/log/flume
rm -f /usr/bin/flume-ng
userdel -r flume

#sqoop
rm -f /usr/bin/sqoop
rm -f /usr/bin/sqoop-codegen
rm -f /usr/bin/sqoop-create-hive-table
rm -f /usr/bin/sqoop-eval
rm -f /usr/bin/sqoop-export
rm -f /usr/bin/sqoop-help
rm -f /usr/bin/sqoop-import
rm -f /usr/bin/sqoop-import-all-tables
rm -f /usr/bin/sqoop-job
rm -f /usr/bin/sqoop-list-databases
rm -f /usr/bin/sqoop-list-tables
rm -f /usr/bin/sqoop-merge
rm -f /usr/bin/sqoop-metastore
rm -f /usr/bin/sqoop-version
userdel -r sqoop


#Remove repositories on all nodes
rm -rf /etc/yum.repos.d/ambari.repo /etc/yum.repos.d/HDP*
yum clean all


#Remove log folders on all nodes

#

#Remove Hadoop folders including HDFS data on all nodes

rm -rf /hadoop/*
rm -rf /hdfs/hadoop
rm -rf /hdfs/lost+found
rm -rf /hdfs/var
rm -rf /local/opt/hadoop
rm -rf /tmp/hadoop
rm -rf /usr/bin/hadoop
rm -rf /usr/hdp
rm -rf /var/hadoop

#Remove config folders on all nodes
rm -rf /etc/mahout

#Remove PIDs on all nodes

#Remove library folders on all nodes

# Clean folder /var/tmp/* on all nodes
rm -rf /var/tmp/*

# Remove databases
yum -y remove mysql mysql-server
yum -y erase postgresql
rm -rf /var/lib/pgsql
rm -rf /var/lib/mysql

#Remove symlinks on all nodes. Especially check folders /usr/sbin and /usr/lib/python2.6/site-packages

rm -f /usr/bin/atlas-start
rm -f /usr/bin/atlas-stop

rm -f /usr/bin/beeline

rm -f /usr/bin/mahout

rm -f /usr/bin/python-wrap

rm -f /usr/bin/worker-lanucher


# find / -name ** on all nodes. You will definitely find several more files/folders. Remove them.
find / -name *ambari*
find / -name *accumulo*
find / -name *atlas*
find / -name *beeline*
find / -name *falcon*
find / -name *flume*
find / -name *hadoop*
find / -name *hbase*
find / -name *hcat*
find / -name *hdfs*
find / -name *hdp*
find / -name *hive*
find / -name *hiveserver2*
find / -name *kafka*
find / -name *mahout*
find / -name *mapred*
find / -name *oozie*
find / -name *phoenix*
find / -name *pig*
find / -name *ranger*
find / -name *slider*
find / -name *sqoop*
find / -name *storm*
find / -name *yarn*
find / -name *zookeeper*

