#
# Cookbook:: hdp-cloud
# Recipe:: local-users

# Set up local users
local_users = data_bag('users')

local_users.each do |entry|
  local_user = data_bag_item('users', entry)

  # Create account for user if service account, otherwise they are created by ldap server
  next if local_user['regular_user'] == 'true'

  user local_user['id'] do
    uid local_user['uid']
    password local_user['password'].to_s
  end

  execute 'change minimum password change age to 0' do
    command "chage -m 0 -M -1 #{local_user['id']}"
    action :run
  end

  directory "/home/#{local_user['id']}/.ssh" do
    owner local_user['id'].to_s
    group local_user['id'].to_s
    mode  '0700'
    action :create
    recursive true
  end

  # Add user to sudo group
  next unless local_user['sudo_user'] == 'true'
  group 'hdpadm' do
    action :manage
    members [local_user['id'].to_s]
    append true
  end
end
