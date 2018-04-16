name "hdp-knox"
description "A role to configure node as HDP knox node"
#run_list "recipe[selinux]", "recipe[basic-packages]", "recipe[ssh-keys]"
run_list "recipe[hdp_knox]"
default_attributes "ssh_keys" => { "cddadmin" => "cddadmin" }
