#
# Cookbook:: hdp_knox
# Recipe:: default
#
# Copyright:: 2018, The Authors, All Rights Reserved.
#
#
#

cookbook_file "/etc/knox/conf/topologies/walgreens.xml" do
  source 'walgreens.xml'
  owner 'knox'
  group 'hadoop'
  mode '0644'
end



execute 'setup_keystore' do 
  command 'sudo $JAVA_HOME/bin/keytool -importkeystore -srckeystore /usr/jdk64/jdk1.8.0_112/jre/lib/security/cacerts -destkeystore /usr/hdp/current/knox-server/data/security/keystores/gateway.jks -deststorepass bigdata -srcstorepass changeit -noprompt'
  ignore_failure true
end

#execute 'command_2' do 
# command 'chmod 0022'
#end


