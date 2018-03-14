import requests
import json

#curl -i -H "X-Requested-By: ambari" -X PUT  -u admin:admin -d '{"RequestInfo": {"context": "_PARSE_.START.ALL_SERVICES","operation_level":{"level":"CLUSTER","cluster_name":"hdpspark"}}, "Body": {"ServiceInfo": {"state":"STARTED"}}}' http://hdp-an01.gombe.com:8080/api/v1/clusters/hdpspark/services

#curl -H "X-Requested-By:ambari" -u admin:admin -i -X PUT -d  '{"RequestInfo":{"context":"Stop Service"},"Body":{"ServiceInfo":{"state":"INSTALLED"}}}' http://AMBARI_SERVER:8080/api/v1/clusters/CLUSTER_NAME/services


headers = {'X-Requested-By': 'ambari'}
auth = {'admin', 'admin'}
url = 'http://hdp-an01.gombe.com:8080/api/v1/blueprints'

data = {}
data['RequestInfo'] = {}
data['RequestInfo']['context'] = {'Stop Service'}

data['Body'] = {}
data['Body']['ServiceInfo'] = {}
data['Body']['ServiceInfo']['state'] = {'INSTALLED'}

json_data = json.dumps(data)
logging.debug(json_data)


res = requests.post(url, headers=headers, params=payload, auth=('admin','admin'))
print "\n*************** res ******************"
print res
print res.text
print res.status_code
print res.headers['Content-Type']




