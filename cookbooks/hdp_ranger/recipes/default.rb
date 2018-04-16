#
# Cookbook:: hdp_ranger
# Recipe:: default
#
# Copyright:: 2018, The Authors, All Rights Reserved.
#

execute 'import_pem_file' do 
  command 'sudo $JAVA_HOME/bin/keytool -import -trustcacerts -alias root -file /etc/pki/ca-trust/source/anchors/rootca.pem -keystore /usr/hdp/current/ranger-usersync/conf/mytruststore.jks -storepass Hashmap@123 -noprompt'
  #ignore_failure true
end


#execute 'import_ranger_cert' do 
# command '$JAVA_HOME/bin/keytool -import -trustcacerts -alias root -file /etc/pki/ca-trust/source/anchors/rootca.pem  -keystore /usr/hdp/current/ranger-usersync/conf/mytruststore.jks'
#end
