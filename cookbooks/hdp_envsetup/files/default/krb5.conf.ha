ncludedir /etc/krb5.conf.d/

[logging]
 default = FILE:/var/log/krb5libs.log
 kdc = FILE:/var/log/krb5kdc.log
 admin_server = FILE:/var/log/kadmind.log

[libdefaults]
 dns_lookup_realm = false
 ticket_lifetime = 24h
 renew_lifetime = 7d
 forwardable = true
 rdns = false
default_realm = HASHWALMS.COM
# default_ccache_name = KEYRING:persistent:%{uid}
#
# [realms]
# HASHWALMS.COM = {
# kdc = hdp-db01.clouddatadojo.com
# admin_server = hdp-db01.clouddatadojo.com
# }
#
# CLOUDDATADOJO.COM = {
# kdc = adPDC.clouddatadojo.com
# admin_server = adPDC.clouddatadojo.com
# }
#
#
# [domain_realm]
# .hashwalms.com = HASHWALMS.COM
# hashwalms.com = HASHWALMS.COM
# .clouddatadojo.com = CLOUDDATADOJO.COM
# clouddatadojo.com = CLOUDDATADOJO.COM
# hdp-mn01.clouddatadojo.com = HASHWALMS.COM
# hdp-mn03.clouddatadojo.com = HASHWALMS.COM
#
# [capaths]
# CLOUDDATADOJO.COM = {
# HASHWALMS.COM = .
#  }
#
