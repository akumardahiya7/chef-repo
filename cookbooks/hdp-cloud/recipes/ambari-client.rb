#
# Cookbook:: hdp-cloud
# Recipe:: ambari-client

# Add resource to clean yum metadata
execute 'yum_cache_clear_ambari_repos' do
  action :nothing
  command 'yum clean metadata'
end

# Add the bigred yum repo
template 'ambari.repo.erb' do
  path '/etc/yum.repos.d/ambari.repo'
  source 'ambari.repo.erb'
  mode '0644'
  notifies :run, 'execute[yum_cache_clear_ambari_repos]', :immediate
end

# Install ambari-agent
yum_package 'ambari-agent' do
  action :install
end

template '/etc/ambari-agent/conf/ambari-agent.ini' do
  source 'ambari-agent.ini.erb'
  mode 0755
  notifies :restart, 'service[ambari-agent]'
end

template '/var/lib/ambari-agent/public_hostname.sh' do
  source 'public_hostname.erb'
  mode '0755'
end

template '/var/lib/ambari-agent/hostname.sh' do
  source 'hostname.erb'
  mode '0755'
end

# Start ambari-agent
service 'ambari-agent' do
  action [:enable, :start]
end
