#
# Cookbook:: ha_proxy
# Recipe:: default
#
# Copyright:: 2018, The Authors, All Rights Reserved.
#
yum_package 'epel-release' do
	action :install
end

yum_package 'haproxy' do
	action :install
end


cookbook_file "/etc/haproxy/haproxy.cfg" do
  source 'haproxy.cfg'
  owner 'root'
  group 'root'
  mode '0644'
end


service 'haproxy' do
	action [ :enable, :start ]  
end
