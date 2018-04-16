name "ambari-agent"
description "A role to configure node as HDP ambari agent"
#run_list "recipe[selinux]", "recipe[basic-packages]", "recipe[ssh-keys]"
run_list "recipe[selinux]", "recipe[hdp_envsetup]", "recipe[firewalld]", "recipe[ssh-keys]", "recipe[ambari::agent]"
default_attributes "ssh_keys" => { "cddadmin" => "cddadmin" }
