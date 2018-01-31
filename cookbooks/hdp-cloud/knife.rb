
    cookbook_path                    '~/dev-cookbooks'
    role_path                        'chef/roles'
    environment_path                 'chef/environments'
    data_bag_path                    'chef/data_bags'
    knife[:bootstrap_version] =      '12.12.15'
#    knife[:berkshelf_path] =         '/var/stacker/deployments/krenz_redstack-krenz_restack-1510842725/cookbooks'
    Chef::Config[:ssl_verify_mode] = :verify_peer if defined? ::Chef
    knife[:host_key_verify] =        false

    node_name "krenz444"
    
