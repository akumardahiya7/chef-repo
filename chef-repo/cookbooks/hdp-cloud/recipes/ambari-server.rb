#
# Cookbook:: hdp-cloud
# Recipe:: ambari-server

# Installs ambari-server
yum_package 'ambari-server' do
  action :install
end

# Runs basic setup for ambari-server with default options
bash 'ambari-server setup' do
  code <<-EOH
    ambari-server setup -s \
    --databasehost=localhost \
    --databaseport=5432 \
    --database=embedded \
    --databasename=ambari \
    --postgresschema=ambari \
    --databaseusername=ambari \
    --databasepassword=ambari
  EOH
  action :run
end

bash 'setup ambari-server https' do
  cwd '/etc/ambari-server/conf/'
  code <<-EOH
    openssl genrsa -out #{node['fqdn']}.key 2048
    openssl req -new -key #{node['fqdn']}.key -out #{node['fqdn']}.csr -subj '/CN=#{node['fqdn']}/O=self/C=US'
    openssl x509 -req -days 365 -in #{node['fqdn']}.csr -signkey #{node['fqdn']}.key -out #{node['fqdn']}.crt
    ambari-server setup-security \
    --security-option=setup-https \
    --api-ssl=true --api-ssl-port=8443 \
    --import-cert-path=#{node['fqdn']}.crt \
    --import-key-path=#{node['fqdn']}.key \
    --pem-password=
  EOH
  action :run
end

# Start ambari server
execute 'start-ambari-server' do
  command 'ambari-server start'
  not_if "ambari-server status | grep 'Ambari Server running'"
end
