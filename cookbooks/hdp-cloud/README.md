# hdp-cloud

Installs and configures a cluster for use with Ambari

 - default.rb - run on all clients
 - master.rb - run on the specified master node
 
Override attributes to your clusters configured settins

To create a user on the cluster, create a new data bag and add JSON like:

`````
{
  "id": "redstack-admin",
  "uid": "1501",
  "keytab_principal": "redstack-admin",
  "keytab_filename": "redstack-admin.headless.keytab",
  "keytab_location": "/user_items/keytabs",
  "keytab_owner": "redstack-admin",
  "keytab_groupowner": "redstack-admin",
  "keytab_permissions": "400",
  "create_hdfs_home": "true",
  "create_ssh_key": "true",
  "regular_user": "true",
  "sudo_user": "true",
  "install_smoke_test": "true",
  "password": "[generated_password_hash]"
}
`````

 - Where the value for `password` is an encrypted password generated by openssl
 - The password is encrypted with a general unix crypt hash, it can be created with `openssl passwd -1  password_string`
 - To create a service user, set the `regular_user` flag to false.  This is how to create a service account for something like Hue
 - Note that service account are not present in the LDAP server, only as a local account
 