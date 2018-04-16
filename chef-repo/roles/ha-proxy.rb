name "ha-proxy"
description "A role to configure node as HA proxy server"
#run_list "recipe[selinux]", "recipe[basic-packages]", "recipe[ssh-keys]"
run_list "recipe[ha_proxy]"
default_attributes "ssh_keys" => { "cddadmin" => "cddadmin" }
