
# install packages
package ['openldap', 'openldap-clients', 'nss-pam-ldapd', 'nss-pam-ldapd'] do
  action [:install, :upgrade]
end

# add the /etc/openldap
template '/etc/openldap/ldap.conf' do
  source 'ldap.conf.erb'
end

template '/etc/nsswitch.conf' do
  source 'nsswitch.conf.erb'
end

template '/etc/nslcd.conf' do
  source 'nslcd.conf.erb'
end

template '/etc/pam.d/system-auth-ac' do
  source 'system-auth-ac.erb'
end

template '/etc/pam.d/password-auth-ac' do
  source 'system-auth-ac.erb'
end

service 'nslcd' do
  action [:start, :enable]
end
