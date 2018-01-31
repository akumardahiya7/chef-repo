#
# Cookbook:: hdp-cloud
# Recipe:: kerberos-server

yum_package 'krb5-server' do
  action :install
end

################ SETUP KDC ##################

# Edit realm in kdc.conf
execute 'change kdc.conf realms' do
  command "sed -i 's/EXAMPLE.COM/#{node['kerberos_realm']}/g' /var/kerberos/krb5kdc/kdc.conf"
  action :run
  not_if "grep '#{node['kerberos_realm']}' /var/kerberos/krb5kdc/kdc.conf"
end

# Edit realm in kadm5.acl
execute 'change kadm5.acl realms' do
  command "sed -i 's/EXAMPLE.COM/#{node['kerberos_realm']}/g' /var/kerberos/krb5kdc/kadm5.acl"
  action :run
  not_if "grep '#{node['kerberos_realm']}' /var/kerberos/krb5kdc/kadm5.acl"
end

execute 'setup the kdc' do
  command '/usr/sbin/kdb5_util create -s -P redstack'
  action :run
  not_if { ::File.exist?('/var/kerberos/krb5kdc/principal.ok') }
end

################ START KDC/KADMIN ###############

execute 'start kadmin' do
  command 'service kadmin start; chkconfig kadmin on'
  action :run
  not_if 'service kadmin status | grep "is running"'
end

execute 'start krb5kdc' do
  command 'service krb5kdc start; chkconfig krb5kdc on'
  action :run
  not_if 'service krb5kdc status | grep "is running"'
end

################# SETUP KDC ADMIN ##################

execute 'Add KDC Admin if not exists' do
  command "/usr/sbin/kadmin.local -q 'addprinc -pw #{node['kerberos_password']} admin/admin@#{node['kerberos_realm']}'"
  action :run
  not_if "/usr/sbin/kadmin.local -q listprincs | grep \"^admin/admin@#{node['kerberos_realm']}\""
end

### Update ticket granter renewal lifetiem
execute 'Add KDC Admin if not exists' do
  command "kadmin.local -r #{node['kerberos_realm']} -q 'modprinc -maxrenewlife 7days +allow_renewable krbtgt/#{node['kerberos_realm']}'"
  action :run
end

###############  CREATE PRINCIPALS AND KEYTABS ###########

directory '/user_items/keytabs' do
  mode '1700'
  action :create
  recursive true
end

users = data_bag('users')

# Create KDC Principals
users.each do |kdc_entry|
  user = data_bag_item('users', kdc_entry)
  execute 'create kdc principals' do
    command "kadmin.local -r #{node['kerberos_realm']} -q 'addprinc -maxrenewlife 7days +allow_renewable -randkey #{user['keytab_principal']}@#{node['kerberos_realm']}'"
    action :run
    not_if "kadmin.local -q 'getprinc #{user['keytab_principal']}' | grep 'Principal: #{user['keytab_principal']}@#{node['kerberos_realm']}'"
  end
end

# Create Keytabs
users.each do |kdc_entry|
  user = data_bag_item('users', kdc_entry)
  execute 'create keytabs' do
    command "kadmin.local -r #{node['kerberos_realm']} -q 'xst -k #{user['keytab_location']}/#{user['keytab_filename']} #{user['keytab_principal']}@#{node['kerberos_realm']}'; chmod #{user['keytab_permissions']} #{user['keytab_location']}/#{user['keytab_filename']}"
    action :run
    notifies :run, 'execute[chown keytab to user]'
    not_if "ls -lah #{user['keytab_location']}/#{user['keytab_filename']}"
  end

  execute 'chown keytab to user' do
    command "chown #{user['keytab_owner']}:hdpadm #{user['keytab_location']}/#{user['keytab_filename']}"
    action :nothing
  end
end

