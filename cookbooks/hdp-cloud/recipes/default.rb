#
# Cookbook:: hdp-cloud
# Recipe:: master
#
# Include this recipe to configure a client node on the cluster

include_recipe 'redstack::runtime'
include_recipe 'redstack::disk'
include_recipe 'redstack::hosts'
include_recipe 'redstack::os'
include_recipe 'redstack::nfs-client'
include_recipe 'redstack::ldap-client'
include_recipe 'redstack::kerberos-client'
include_recipe 'redstack::local-users'
include_recipe 'redstack::ambari-client'
