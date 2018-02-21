import requests
import json

#curl -H "X-Requested-By: ambari" -X GET -u admin:admin http://hdp-an01.gombe.com:8080/api/v1/blueprints
headers = {'X-Requested-By': 'ambari'}
auth = {'admin', 'admin'}
url = 'http://hdp-an01.gombe.com:8080/api/v1/blueprints'

res = requests.get(url, headers=headers, auth=('admin','admin'))
print "\n*************** res ******************"
print res
print res.text
print res.status_code
print res.headers['Content-Type']

result = res.json()
print(result)

print "\n*************** href ******************"
result = res.json().get('href')
print(result)

print "\n*************** items ******************"
result = res.json().get('items')
print(result)
print(result[0])
print(result[0]['Blueprints'])
print(result[0]['href'])
print(result[0]['Blueprints']['blueprint_name'])




