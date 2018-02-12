#ambar-server
ambari-server stop

#Run python script on all cluster nodes
touch /var/lib/ambari-agent/data/hostcheck_custom_actions.result
python /usr/lib/python2.6/site-packages/ambari_agent/HostCleanup.py --silent



#ambari-agent
service ambari-agent stop
yum -y erase ambari-agent

rm -rf /var/lib/ambari-agent
rm -rf /var/run/ambari-agent
rm -rf /usr/lib/amrbari-agent

rm -rf /etc/ambari-agent
rm -rf /var/log/ambari-agent
rm -rf /usr/lib/python2.6/site-packages/ambari*


#ambar-server
#ambari-server stop
ambari-server reset
yum -y erase ambari-server

rm -rf /var/lib/ambari-server
rm -rf /var/run/ambari-server
rm -rf /usr/lib/ambari-server

rm -rf /etc/ambari-server
rm -rf /var/log/ambari-server
rm -rf /usr/lib/python2.6/site-packages/ambari*


service postgresql stop
yum -y erase postgresql -y
rm -rf /var/lib/pgsql


