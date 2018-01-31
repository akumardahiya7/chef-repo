#
# Cookbook:: hdp-cloud
# Recipe:: nfs-server

# Create keytab shared directory
directory '/user_items/keytabs' do
  action :create
  mode '1777'
  recursive true
end

# Create home_dir shared directory
directory '/user_items/home' do
  action :create
  mode '0755'
  recursive true
end

# Export /user_items/
nfs_export '/user_items' do
  network '*.redstack.com'
  writeable true
  sync true
  options ['no_subtree_check']
end

service 'rpcbind' do
  action [:enable, :start]
end

service 'nfs-server' do
  action [:enable]
end

service 'nfs' do
  action [:start]
end
