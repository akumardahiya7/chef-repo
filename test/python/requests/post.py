import requests
import json

#curl -i -H "X-Requested-By: ambari" -X PUT  -u admin:admin -d '{"RequestInfo": {"context": "_PARSE_.START.ALL_SERVICES","operation_level":{"level":"CLUSTER","cluster_name":"hdpspark"}}, "Body": {"ServiceInfo": {"state":"STARTED"}}}' http://hdp-an01.gombe.com:8080/api/v1/clusters/hdpspark/services

headers = {'X-Requested-By': 'ambari'}
auth = {'admin', 'admin'}
url = 'http://hdp-an01.gombe.com:8080/api/v1/blueprints'
payload = {"RequestInfo": \
		{"context": "_PARSE_.START.ALL_SERVICES", "operation_level":\
								{"level":"CLUSTER","cluster_name":"hdpspark"}\
		},\
 	"Body":\
		{"ServiceInfo":\
			 {"state":"STARTED"}\
		}\
	}
res = requests.post(url, headers=headers, params=payload, auth=('admin','admin'))
print "\n*************** res ******************"
print res
print res.text
print res.status_code
print res.headers['Content-Type']




