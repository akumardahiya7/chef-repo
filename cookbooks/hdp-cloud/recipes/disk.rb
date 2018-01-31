#
# Cookbook:: hdp-cloud
# Recipe:: disk

execute "partition and format on #{node['volume_device']}" do
  command "parted -s #{node['volume_device']} mklabel gpt; parted -s #{node['volume_device']} mkpart primary ext4 0% 100%; mke2fs -F -L grid_0 -t ext4 -T es #{node['volume_device']}"
  not_if "df -h | grep #{node['volume_device']}"
end

# Create and mount
directory node['mount_location'] do
  owner 'root'
  group 'root'
  recursive true
  mode '0755'
  action :create
end

mount node['mount_location'] do
  device node['volume_device']
  device_type :device
  fstype 'ext4'
  options 'inode_readahead_blks=128,data=writeback,noatime,nodev,nobarrier'
  action [:mount, :enable]
end
