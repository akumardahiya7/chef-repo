
# Java jdk attribute
default['java']['jdk'] = 'jdk1.8.0_73'

# Overridden by runtime recipe in redstack
default['volume_device'] = '/dev/vdb'
default['mount_location'] = '/grid/0'
default['kerberos_realm'] = 'REDSTACK.COM'
default['domain'] = '.redstack.com'
default['master_node'] = 'rs-master.redstack.com'

# Default passwords
default['kerberos_password'] = 'redstack'
default['ambari_mysql_password'] = 'ambari'

# Default cluster node values, change these as needed
default['redstack']['cluster']['rs-master']['external_ip'] = '10.63.110.73'
default['redstack']['cluster']['rs-master']['internal_ip'] = '192.168.198.193'
default['redstack']['cluster']['rs-master']['fqdn'] = 'rs-master.redstack.com'
default['redstack']['cluster']['rs-control1']['external_ip'] = '10.60.151.41'
default['redstack']['cluster']['rs-control1']['internal_ip'] = '192.168.198.4'
default['redstack']['cluster']['rs-control1']['fqdn'] = 'rs-control2.redstack.com'
default['redstack']['cluster']['rs-control2']['external_ip'] = '10.60.151.41'
default['redstack']['cluster']['rs-control2']['internal_ip'] = '192.168.198.4'
default['redstack']['cluster']['rs-control2']['fqdn'] = 'rs-control2.redstack.com'
default['redstack']['cluster']['rs-data1']['external_ip'] = '10.60.151.41'
default['redstack']['cluster']['rs-data1']['internal_ip'] = '192.168.198.4'
default['redstack']['cluster']['rs-data1']['fqdn'] = 'rs-data1.redstack.com'
default['redstack']['cluster']['rs-data2']['external_ip'] = '10.60.151.41'
default['redstack']['cluster']['rs-data2']['internal_ip'] = '192.168.198.4'
default['redstack']['cluster']['rs-data2']['fqdn'] = 'rs-data2.redstack.com'
default['redstack']['cluster']['redstackdat3']['external_ip'] = '10.60.151.41'
default['redstack']['cluster']['redstackdat3']['internal_ip'] = '192.168.198.4'
default['redstack']['cluster']['redstackdat3']['fqdn'] = 'redstackdat3.redstack.com'
default['redstack']['cluster']['redstackdat4']['external_ip'] = '10.60.151.41'
default['redstack']['cluster']['redstackdat4']['internal_ip'] = '192.168.198.4'
default['redstack']['cluster']['redstackdat4']['fqdn'] = 'redstackdat4.redstack.com'
