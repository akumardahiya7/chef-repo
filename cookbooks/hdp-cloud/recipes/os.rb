#
# Cookbook:: hdp-cloud
# Recipe:: os

include_recipe 'yum'
include_recipe 'entropy'
# We need enough entropy to generate private keys and kerberos server

# Disable Selinux
execute 'disable selinux' do
  command 'setenforce 0'
end

replace_or_add 'selinux disabled' do
  path '/etc/selinux/config'
  pattern 'SELINUX=enforcing'
  line 'SELINUX=disabled'
end

# Fix init umask
execute 'umask-sysconfig-init' do
  command "sed -i 's/umask 027/umask 022/g' /etc/sysconfig/init"
  action :run
  not_if "grep 'umask 022' /etc/sysconfig/init"
end

# Enable password SSH login
replace_or_add 'PasswordAuthentication yes' do
  path '/etc/ssh/sshd_config'
  pattern 'PasswordAuthentication no'
  line 'PasswordAuthentication yes'
  notifies :run, 'execute[reload sshd]', :immediately
end

# Reload sshd's config
execute 'reload sshd' do
  command 'service sshd reload'
  action :nothing
end

# Set hostname for node
execute 'set hostname - required in kitchen with the KDC setup' do
  command "hostname #{node['hostname']}#{node['domain']}"
end

# Reload Ohai to reflect updated hostname
ohai 'reload' do
  action :reload
end

# Change TZ to CDT
execute 'change TZ to CDT' do
  command 'rm -f /etc/localtime; ln -s /usr/share/zoneinfo/America/Chicago /etc/localtime'
  not_if 'date | grep CDT'
end

execute 'change TZ to CDT' do
  command "echo 'ZONE=America/Chicago' > /etc/sysconfig/clock"
  not_if "grep 'ZONE=America/Chicago' /etc/sysconfig/clock"
end

# TODO: merge these into a single resource
package ['vim', 'ntp', 'screen', 'libpwquality', 'libxslt-python'] do
  action :install
end

# enable ntpd
service 'ntpd' do
  action [:enable, :start]
end

# Setup groups
group 'hadoop' do
  action :create
end

group 'hdpadm' do
  action :create
  members ['centos']
  gid 1051
end

group 'hdpservice' do
  action :create
  gid 1052
end

# Manage sudoer file
append_if_no_line 'add hdpadm to sudoers' do
  path '/etc/sudoers'
  line '%hdpadm   ALL=(ALL:ALL)   NOPASSWD: ALL'
end
