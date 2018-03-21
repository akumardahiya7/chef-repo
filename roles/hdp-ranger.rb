name "hdp-ranger"
description "A role to configure node as HDP ranger node"
#run_list "recipe[selinux]", "recipe[basic-packages]", "recipe[ssh-keys]"
run_list "recipe[hdp_ranger]"
default_attributes "ssh_keys" => { "cddadmin" => "cddadmin" }
