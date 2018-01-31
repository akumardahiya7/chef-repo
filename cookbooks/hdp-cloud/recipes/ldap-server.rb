# install packages
package ['openldap', 'openldap-servers', 'openldap-clients'] do
  action :install
end

execute "Restart slapd after restarts" do
  command "systemctl enable slapd.service"
end

execute "Start slapd after crashes" do
  command "sed -i '/\[Service\]/a Restart=always' /usr/lib/systemd/system/slapd.service"
end

execute "Reload systemctl daemon" do
  command "systemctl daemon-reload"
end

# start slapd service
service 'slapd' do
  action [:start, :enable]
end

template '/tmp/manager.ldif' do
  source 'manager.ldif.erb'
  notifies :run, 'execute[configure openldap]', :immediately
  notifies :run, 'execute[add the cosine package to the ldap server]', :immediately
  notifies :run, 'execute[add the inetorgperson package to the ldap server]', :immediately
  notifies :run, 'execute[add the nis package to the ldap server]', :immediately
end

# add the cosine package to the ldap server
execute 'add the cosine package to the ldap server' do
  command 'ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/cosine.ldif'
  action :nothing
end

# add the inetorgperson package to the ldap server
execute 'add the inetorgperson package to the ldap server' do
  command 'ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/inetorgperson.ldif'
  action :nothing
end

# add the inetorgperson package to the ldap server
execute 'add the nis package to the ldap server' do
  command 'ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/nis.ldif'
  action :nothing
end

execute 'configure openldap' do
  command 'ldapmodify -Y EXTERNAL -H ldapi:/// -f /tmp/manager.ldif'
  action :nothing
end

# fetch the data from the data bags
local_users = data_bag('users')
users = []

# iterate the users and build the users to pass to the data bag
local_users.each do |entry|
  local_user = data_bag_item('users', entry)

  next unless local_user['regular_user'] == 'true'
  if local_user['password']
    password = '{CRYPT}' + local_user['password']
  else
    local_user['id'] + '-password'
  end

  local_user['password'] = password
  users.push(local_user)
end

# build the template
template '/tmp/users.ldif' do
  source 'users.ldif.erb'
  owner 'root'
  group 'root'
  mode '0644'
  variables(
    users: users
  )
  notifies :run, 'execute[add the ldif to the server]', :immediately
end

# add the users to the ldap server
execute 'add the ldif to the server' do
  command 'ldapadd -f /tmp/users.ldif -D cn=redstack,dc=redstack,dc=com -w admin -h localhost'
  action :nothing
end

# Create nfs home directories for users
local_users.each do |entry|
  local_user = data_bag_item('users', entry)

  # Create account for user if service account, otherwise they are created by ldap server
  next unless local_user['regular_user'] == 'true'

  # Create home, SSH dir
  directory "/user_items/home/#{local_user['id']}/.ssh" do
    mode '0700'
    action :create
    recursive true
    notifies :run, 'execute[chown directory to user]'
  end

  template 'user bash_profile' do
    source 'bash_profile.erb'
    path "/user_items/home/#{local_user['id']}/.bash_profile"
  end

  if local_user['create_ssh_key'] == 'true'

    bash 'generate ssh key and authorized hosts' do
      action :run
      code <<-EOH
        ssh-keygen -f /user_items/home/#{local_user['id']}/.ssh/id_rsa -N '';
        cat /user_items/home/#{local_user['id']}/.ssh/id_rsa.pub >> /user_items/home/#{local_user['id']}/.ssh/authorized_keys
      EOH
      not_if { ::File.exist?("/user_items/home/#{local_user['id']}/.ssh/#{local_user['id']}_id_rsa") }
    end
  end

  execute 'chown directory to user' do
    command "chown -R #{local_user['id']}:hdpadm /user_items/home/#{local_user['id']}"
    action :nothing
  end
end
