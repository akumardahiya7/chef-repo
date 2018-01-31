#
# Cookbook:: hdp-cloud
# Recipe:: kerberos-client

# Install packages for kerberos client
package ['krb5-libs', 'krb5-workstation'] do
  action :install
end

# Configure krb5.conf
template '/etc/krb5.conf' do
  source 'krb5.conf.erb'
  mode 0644
  owner 'root'
end

# Create keytabs directory
directory '/etc/security/keytabs' do
  owner 'root'
  mode '0755'
  action :create
end
