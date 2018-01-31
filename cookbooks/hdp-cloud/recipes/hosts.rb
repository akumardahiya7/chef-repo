#
# Cookbook:: hdp-cloud
# Recipe:: hosts

# Apply /etc/hosts file to each node
template '/etc/hosts' do
  source 'hosts.erb'
  mode '0644'
  variables(
    hosts: node['redstack']['cluster'],
  )
end

