#
# Cookbook:: hdp_envsetup
# Recipe:: default
#
# Copyright:: 2018, Hashmap Inc, All Rights Reserved.

yum_package 'ntp' do
	action :install
end

service 'ntpd' do
	action [ :enable, :start ]  
end

execute 'set_umask' do 
 command 'umask 0022'
end

cookbook_file "/etc/python/cert-verification.cfg" do
  source 'cert-verification.cfg'
  owner 'root'
  group 'root'
  mode '0644'
end

search(:users, '*:*').each do |u|
  directory "/home/#{u['id']}/.ssh" do
    owner u['id']
  end

  file "/home/#{u['id']}/.ssh/id_rsa" do
    owner u['id']
    group u['id']
    mode '600'
    content u['id_rsa']
  end
end
