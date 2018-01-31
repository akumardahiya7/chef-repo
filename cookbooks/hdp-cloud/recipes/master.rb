#
# Cookbook:: hdp-cloud
# Recipe:: master
#
# Include this recipe to configure the master node in a cluster with ambari-server

include_recipe 'redstack::runtime'
include_recipe 'redstack::disk'
include_recipe 'redstack::hosts'
include_recipe 'redstack::os'
include_recipe 'redstack::kerberos-client'
include_recipe 'redstack::kerberos-server'
include_recipe 'redstack::ldap-client'
include_recipe 'redstack::ldap-server'
include_recipe 'redstack::nfs-server'
include_recipe 'redstack::local-users'
include_recipe 'redstack::ambari-client'
include_recipe 'redstack::ambari-server'
