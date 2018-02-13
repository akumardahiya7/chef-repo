#ambari server
knife bootstrap --sudo  -i ./cluster.privkey -x centos -r role['ambari-server'] anil-hdp-en.hashmap.net

#master nodes
knife bootstrap --sudo  -i ./cluster.privkey -x centos -r role['ambari-agent'] anil-hdp-mn-1.hashmap.net
knife bootstrap --sudo  -i ./cluster.privkey -x centos -r role['ambari-agent'] anil-hdp-mn-2.hashmap.net
knife bootstrap --sudo  -i ./cluster.privkey -x centos -r role['ambari-agent'] anil-hdp-mn-3.hashmap.net

#slave nodes
knife bootstrap --sudo  -i ./cluster.privkey -x centos -r role['ambari-agent'] anil-hdp-sn-1.hashmap.net
knife bootstrap --sudo  -i ./cluster.privkey -x centos -r role['ambari-agent'] anil-hdp-sn-2.hashmap.net
knife bootstrap --sudo  -i ./cluster.privkey -x centos -r role['ambari-agent'] anil-hdp-sn-3.hashmap.net
