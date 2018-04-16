#
# Cookbook:: hdp-cloud
# Recipe:: nfs-client

# Create directory to mount NFS share
directory '/user_items' do
  owner 'root'
  group 'root'
  mode  '0755'
  action :create
end

nfs '/user_items' do
  server node['master_node']
  export '/user_items'
  options 'sync'
end
