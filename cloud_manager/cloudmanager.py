'''
Azure HDP cluster: Implementation to manage HDP (Hortonworks Data Flatform) on Azure Cloud

Version: v1.0 01/02/2018

Authors: Anil Dahiya anil.dahiya@hashmapinc.com

Fixes:

'''
import os
import sys
import logging
import argparse
from subprocess import Popen, PIPE, STDOUT
import yaml
import json
import requests
import time

'''
HDP Cluster related to operations 
'''

class cluster_init(object):
	def __init__(cluster):
		res = False
		cluster.init = True
		return

	def shell_cmd_exec(manager, cmd):
		ret = 0
		res = []

#		cmd = cmd + "> /dev/null 2>&1" 
		cmd = cmd + ">> /tmp/cloud_manager.log 2>&1" 
		logging.debug("\nShell command to be executed: " + cmd)
#		return ret

		process = Popen(cmd, bufsize=2048, stdin=PIPE, stdout=PIPE, shell=True)
		(child_stdin, child_stdout) = (process.stdin, process.stdout)
		if process.wait() != 0:
			ret = -1

		for line in child_stdout:
			# the real code does filtering here
			line = line.rstrip()
			res.append(line)
			logging.debug(line)

		if ret < 0:
			logging.error("Error: Could not execute shell command:: %s\n", cmd)
			logging.error(res)
			return ret

		logging.debug("Shell command returned output: %s\n", cmd)
		logging.debug(res)
		return ret

	def json_validator(cluster, filename):
		try:
        		json.load(open(filename))
        		return True
    		except ValueError as error:
        		logging.error("Error: Invalid json in file %s: %s" % (filename, error))
       			return False


	def hdp_config(cluster, config):
		'''
		cluster:
			name: walgreens_hdp_spark
			blueprint: walgreens_hdp_spark.json
			hostmapping: walgreens_hdp_spark-hostmap.json
			ambari: hdp-an01.gombe.com
			nodes: 
				- hdp-en01.gombe.com
				- hdp-mn01.gombe.com
				- hdp-mn02.gombe.com
				- hdp-mn03.gombe.com
				- hdp-sn01.gombe.com
				- hdp-sn02.gombe.com
		database:
			host: hdp-db01.gombe.com
			ambari: 
				- name: ambari
				- username: ambari
				- passwd: bigdata 
		'''
		ret = 0 
		with open(config, 'r') as ymlfile:
    			cluster.config = yaml.load(ymlfile)

#		for section in cluster.config:
#			print(section)
		#print "\nPassed HDP Cluster configuration is: "
		#print(cluster.config['cluster'])

		cluster.name = cluster.config['cluster']['name']
		logging.info("\nHDP Cluster Name: " + cluster.name)

		cluster.blueprint = cluster.config['cluster']['blueprint']
		logging.info("\nHDP Cluster Blueprint: " + cluster.blueprint)
		ret = cluster.json_validator(cluster.blueprint)
		if(ret == False):
			ret = -1	
			logging.error("Error: HDP Cluster Blueprint file contains invalid JSON Format")
			return ret

		cluster.hostmap = cluster.config['cluster']['hostmap']
		logging.info("\nHDP Cluster Blueprint Hostmap: " + cluster.hostmap)
		ret = cluster.json_validator(cluster.hostmap)
		if(ret == False):
			ret = -1	
			logging.error("Error: HDP Cluster Hostmapping file contains invalid JSON Format")
			return ret

		if ('ssh' in cluster.config['cluster']) == False:
			ret = -1	
			logging.error("\nError: HDP cluster ssh config has not been specified \n")
			return ret

		cluster.username = cluster.config['cluster']['ssh']['username']
		logging.info("\nHDP Cluster SSH username: " + cluster.username)

		cluster.ssh_key = cluster.config['cluster']['ssh']['privkey']
		logging.info("\nHDP Cluster SSH private keyfile: " + cluster.ssh_key)

		cluster.ambari_host = cluster.config['cluster']['ambari']['host']
		logging.info("\nHDP Cluster Ambari Server node host: " + cluster.ambari_host)

		cluster.ambari_username = cluster.config['cluster']['ambari']['username']
		logging.info("\nHDP Cluster Ambari Server admin username: " + cluster.ambari_username)

		cluster.ambari_passwd = cluster.config['cluster']['ambari']['passwd']
		#print "\nHDP Cluster Ambari Server admin password: " + cluster.ambari_passwd

		cluster.ambari_db_type = cluster.config['cluster']['ambari']['database']['type']
		logging.info("\nHDP Cluster Ambari Server database type: " + cluster.ambari_db_type)

		cluster.ambari_db_host = cluster.config['cluster']['ambari']['database']['host']
		logging.info("\nHDP Cluster Ambari Server database host: " + cluster.ambari_db_host)

		cluster.ambari_db_port = cluster.config['cluster']['ambari']['database']['port']
		logging.info("\nHDP Cluster Ambari Server database port: " + str(cluster.ambari_db_port))

		cluster.ambari_db_name = cluster.config['cluster']['ambari']['database']['name']
		logging.info("\nHDP Cluster Ambari Server database name: " + cluster.ambari_db_name)

		cluster.ambari_db_username = cluster.config['cluster']['ambari']['database']['username']
		logging.info("\nHDP Cluster Ambari Server database username: " + cluster.ambari_db_username)

		cluster.ambari_db_passwd = cluster.config['cluster']['ambari']['database']['passwd']
		#print "\nHDP Cluster Ambari Server database password: " + cluster.ambari_db_passwd


		logging.info("\nHDP Cluster Nodes are:") 

		logging.info(cluster.config['cluster']['nodes'])

		if ('kerberos' in cluster.config['cluster']) == True:
			cluster.kerberos_conf = cluster.config['cluster']['kerberos']['conf']
			logging.info("\nHDP KERBEROS config: " + cluster.kerberos_conf)
			ret = cluster.json_validator(cluster.kerberos_conf)
			if(ret == False):
				ret = -1	
				logging.error("Error: %s KERBEROS conf file contains invalid JSON Format")
				return ret



			cluster.kerberos_principal = cluster.config['cluster']['kerberos']['principal']
			logging.info("\nHDP KERBEROS principal config: " + cluster.kerberos_principal)
			ret = cluster.json_validator(cluster.kerberos_principal)
			if(ret == False):
				ret = -1	
				logging.error("Error: %s KERBEROS Principal file contains invalid JSON Format")
				return ret

		return ret

	def hdp_ambari_configure(cluster, manager):
		#knife bootstrap -i ~/cluster-ssh-privkey -x cddadmin --sudo -r role['ambari-server'] hdp-en01
		
		ret = 0

		data = {}  
		data['ambari'] = {} 
		data['ambari']['database'] = {}
		data['ambari']['database']['type'] = cluster.ambari_db_type 
		data['ambari']['database']['host'] = cluster.ambari_db_host
		data['ambari']['database']['port'] = cluster.ambari_db_port
		data['ambari']['database']['name'] = cluster.ambari_db_name
		data['ambari']['database']['username'] = cluster.ambari_db_username
		data['ambari']['database']['password'] = cluster.ambari_db_passwd

		json_data = json.dumps(data)
		logging.debug(json_data)

		role = "role['ambari-server']"
		logging.debug("HDP Cluster Name: " + cluster.name)
		cmd = "knife bootstrap --sudo " \
				+ " -i " + cluster.ssh_key \
				+ " -x " + cluster.username \
				+ " -r " + role \
				+ " -j " + "'" + json_data + "'" \
				+ " " + cluster.ambari_host
				
		logging.info("\nConfiguring ambari server ...")
		ret = cluster.shell_cmd_exec(cmd)
		if ret < 0:
			logging.error("\nError: Could not configure Ambari Server")
			return ret

		logging.info("Successfully configured Ambari Server")
		return ret

	def hdp_node_configure(cluster, node):
		'''
		Configure all HDP nodes with ambari-agent role 

		Example:
		knife bootstrap -i ~/cluster-ssh-privkey -x cddadmin --sudo -r role['ambari-agent'] hdp-en01
		'''
		ret = 0
		role = "role['ambari-agent']"

		logging.info("\nConfiguring HDP node: " + str(node) + " ...")

		cmd = "knife bootstrap --sudo " \
				+ " -i " + cluster.ssh_key \
				+ " -x " + cluster.username \
				+ " -r " + role \
				+ " " + node  

		ret = cluster.shell_cmd_exec(cmd)
		if ret < 0:
			logging.error("Error: Could not configure HDP node: %s", node)
			return -1

		logging.info("Successfully configured HDP node: " + str(node)) 
		return 0


	def hdp_nodes_configure(cluster, manager):
		'''
		Configure all HDP nodes with ambari-agent role 
		
		Example:
		knife bootstrap -i ~/cluster-ssh-privkey -x cddadmin --sudo -r role['ambari-agent'] hdp-en01
		'''
		ret = 0
		logging.info("\nConfiguring HDP nodes ...")
		role = "role['ambari-agent']"

		count = 0 
		num = 0 
		for node in cluster.config['cluster']['nodes']: 
			num = num + 1
			ret = cluster.hdp_node_configure(node)
			if ret == 0:
				count = count + 1

		# log error based up on how many hdp nodes being configured
		if count == 0:
			logging.error("\nError: Could not configure any HDP node")
			return -1

		if count != num:
			logging.warning("\nWarning: Successfully configured only HDP %d node(s) out of %d node(s)", count, num)
			return 0

		logging.info("\nSuccessfully configured HDP nodes")
		return 0


	def hdp_blueprint_create(cluster, manager):
		'''
		Create HDP blueprint
		
		Example:
		$ curl -H "X-Requested-By: ambari" -X POST -u admin:admin \
				http://hdp-en01:8080/api/v1/blueprints/hdp-small-default @hdp-small-default.json
		'''

		ret = 0 

		logging.info("\nUploading HDP blueprint: " + cluster.blueprint + " ...")
		cmd = 'curl -H "X-Requested-By: ambari" -X POST '\
				+ ' -u ' + cluster.ambari_username + ':' + cluster.ambari_passwd \
				+ ' http://' + cluster.ambari_host + ':8080/api/v1/blueprints/' + cluster.name \
				+ ' -d @' +  str(cluster.blueprint)

		ret = cluster.shell_cmd_exec(cmd)
		if ret < 0:
			logging.error("Error: Could not upload HDP blueprint")
			return -1

		logging.info("Sucessfully uploaded HDP blueprint:" + cluster.blueprint)
		return 0


	def hdp_installation_status(cluster, manager):
		'''
		Install HDP cluster using blueprint	

		Example:
		$curl -H "X-Requested-By: ambari" -X POST -u admin:admin \
					http://hdp-en01:8080/api/v1/clusters/hdp-small-default -d @hostmap.json
		'''

	#	res = []
	#	headers = {'X-Requested-By': 'ambari'}
	#	url = 'http://' + cluster.ambari_host + ':8080/api/v1/clusters/' + cluster.name
	#	print url

	#	data = json.loads(open(cluster.hostmap).read())
	#	print data
	#	res = requests.post(url, headers=headers, params=data, auth=(cluster.ambari_username, cluster.ambari_passwd))
	#	print res
	#	print res.text
		#if res.raise_for_status() is not None:
		#	print "Error: Uploading blueprint," + res.text
		#	return False

	#	result = res.json().get('items')
	#	url = result[0]['href']
		ret = 0 
		root_logger = logging.getLogger()

		logging.info("\nHDP Cluster installation progress (%):")

		headers = {'X-Requested-By': 'ambari'}
		url = 'http://' + cluster.ambari_host + ':8080/api/v1/clusters/' + cluster.name + "/requests/1"
		logging.debug(url)

		root_logger.setLevel(logging.WARNING)
		res = requests.get(url, headers=headers, auth=(cluster.ambari_username, cluster.ambari_passwd))
		root_logger.setLevel(logging.INFO)
		logging.debug(res)

		progress = 0
		while progress < 100:
			root_logger.setLevel(logging.WARNING)

			res = requests.get(url, headers=headers, auth=(cluster.ambari_username, cluster.ambari_passwd))
			logging.debug(res)
			if res.raise_for_status() is not None:
				logging.error("Error: HDP installation has failed")
				return -1

			result = res.json().get('Requests')
			progress = result['progress_percent']
			time.sleep( 5 )
    			sys.stdout.write("\r%d%%" % progress)
			sys.stdout.flush()
			logging.info("HDP Cluster installation progress (%s):", progress)

			root_logger.setLevel(logging.INFO)

		logging.info("\nSuccessfully installed HDP Cluster")
		return 0

	def hdp_kerberose_conf(cluster, manager):
		'''
		Create and set KERBEROS service configurations

		$ curl -H "X-Requested-By:ambari" -u admin:admin -i -X PUT \
			 -d @./payload http://AMBARI_SERVER:8080/api/v1/clusters/CLUSTER_NAME
		Example:
		'''

		res = []
		headers = {'X-Requested-By': 'ambari'}
		url = 'http://' + cluster.ambari_host + ':8080/api/v1/clusters/' + cluster.name
		logging.debug("url: " + url)

		data = json.loads(open(cluster.hostmap).read())
		logging.debug("data: " + data)
		res = requests.post(url, headers=headers, params=data, auth=(cluster.ambari_username, cluster.ambari_passwd))
		logging.debug("res: " + res)
		logging.debug("res.text: " + res.text)
		logging.debug("res.status_code: " + res.status_code)
		

		if res.raise_for_status() is not None:
			logging.error("Error: Uploading blueprint," + res.text)
			return False

		result = res.json().get('items')
		url = result[0]['href']
		logging.info("\nCluster build is complete")
		return ret



	def hdp_installation(cluster, manager):
		'''
		Install HDP cluster using blueprint	

		Example:
		$curl -H "X-Requested-By: ambari" -X POST -u admin:admin \
					http://hdp-en01:8080/api/v1/clusters/hdp-small-default -d @hostmap.json
		'''

		ret = 0 
		logging.info("\nInstalling HDP Clutser: " + cluster.name + " ...")
		cmd = 'curl -H "X-Requested-By: ambari" -X POST '\
				+ ' -u ' + cluster.ambari_username + ':' + cluster.ambari_passwd \
				+ " http://" + cluster.ambari_host + ":8080/api/v1/clusters/" + cluster.name \
				+ " -d @" +  str(cluster.hostmap)

		ret = cluster.shell_cmd_exec(cmd)
		if ret < 0:
			logging.error("Error: Could not start HDP cluster installtion")
			return -1

		logging.info("HDP Cluster installation has been started, access HDP Ambari dashboard using link"\
						 + '\nhttp://' + cluster.ambari_host + ':8080/\n')
		return 0

	def hdp_cluster_stop(cluster, manager):
		'''
		Stop all services

		Example:
		$ curl -H "X-Requested-By:ambari" -u admin:admin -i -X PUT \
				-d  '{"RequestInfo":{"context":"Stop Service"}, \
					"Body":{"ServiceInfo":{"state":"INSTALLED"}}}'\
			 	http://AMBARI_SERVER:8080/api/v1/clusters/CLUSTER_NAME/services
		'''

		root_logger = logging.getLogger()

		logging.info("\nStopping all services of HDP Clutser: " + cluster.name + " ...")
		
		headers = {'X-Requested-By': 'ambari'}
		url = 'http://' + cluster.ambari_host + ':8080/api/v1/clusters/' \
						+ cluster.name + "/services"
		logging.debug(url)

		data = {}
		data['RequestInfo'] = {}
		data['RequestInfo']['context'] = "Stop Service"

		data['Body'] = {}
		data['Body']['ServiceInfo'] = {}
		data['Body']['ServiceInfo']['state'] = "INSTALLED"

		json_data = json.dumps(data)
		logging.debug(json_data)

		root_logger.setLevel(logging.WARNING)
		res = requests.put(url, headers=headers, data=json_data, auth=(cluster.ambari_username, cluster.ambari_passwd))
		root_logger.setLevel(logging.INFO)

		logging.debug(res)
		logging.debug(res.text)

		logging.debug(res)

		if res.status_code == 200: 
			logging.warning("Warning: HDP cluster services already stopped")
			return 0

		if res.raise_for_status() is not None:
			logging.error("Error: Could not stop HDP Cluster: %s Services", cluster.name)
			return -1

		if res.status_code != 202: 
			logging.error("Error: Could not stop HDP Cluster, HTTP error code: %d" % (res.status_code))
			return -1

		url = res.json().get('href')
		logging.debug(url)

		progress = 0
		while progress < 100:
			root_logger.setLevel(logging.WARNING)
			res = requests.get(url, headers=headers, auth=(cluster.ambari_username, cluster.ambari_passwd))
			logging.debug(res)

			if res.raise_for_status() is not None:
				logging.error("Error: HDP cluster stop operation has failed")
				return -1

			result = res.json().get('Requests')
			progress = result['progress_percent']
			time.sleep( 5 )
    			sys.stdout.write("\r%d%%" % progress)
			sys.stdout.flush()

			logging.info("HDP Cluster Stop progress (%s):", progress)
			root_logger.setLevel(logging.INFO)


		logging.info("\nSucessfully stopped HDP cluster " + cluster.name)
		return 0

	def hdp_cluster_start(cluster, manager):
		'''
		Start HDP cluster

		Example:
		$ curl -H "X-Requested-By:ambari" -u admin:admin -i -X PUT \
					-d '{"ServiceInfo": {"state" : "STARTED"}}' \
					http://AMBARI_SERVER:8080/api/v1/clusters/CLUSTER_NAME/services


		'''
		root_logger = logging.getLogger()
		logging.info("\nStarting all services of HDP Clutser: " + cluster.name + " ...")
		
		headers = {'X-Requested-By': 'ambari'}
		url = 'http://' + cluster.ambari_host + ':8080/api/v1/clusters/' \
						+ cluster.name + "/services"
		logging.debug(url)

		data = {}
		data['ServiceInfo'] = {}
		data['ServiceInfo']['state'] = "STARTED"

		json_data = json.dumps(data)
		logging.debug(json_data)

		root_logger.setLevel(logging.WARNING)
		res = requests.put(url, headers=headers, data=json_data, auth=(cluster.ambari_username, cluster.ambari_passwd))
		root_logger.setLevel(logging.INFO)

		logging.debug(res)
		logging.debug(res.text)

		logging.debug(res)

		if res.status_code == 200: 
			logging.warning("Warning: HDP cluster services already stopped")
			return 0

		if res.raise_for_status() is not None:
			logging.error("Error: Could not start HDP Cluster: %s Services", cluster.name)
			return -1


		if res.status_code != 202: 
			logging.error("Error: Could not start HDP Cluster, HTTP error code: %d" % (res.status_code))
			return -1

		url = res.json().get('href')
		logging.debug(url)


		progress = 0
		while progress < 100:
			root_logger.setLevel(logging.WARNING)

			res = requests.get(url, headers=headers, auth=(cluster.ambari_username, cluster.ambari_passwd))
			logging.debug(res)
			if res.raise_for_status() is not None:
				logging.error("Error: Could not get status of start HDP Services operation")
				return -1

			result = res.json().get('Requests')
			progress = result['progress_percent']
			time.sleep( 5 )
    			sys.stdout.write("\r%d%%" % progress)
			sys.stdout.flush()
			logging.info("HDP Cluster start progress (%s):", progress)

			root_logger.setLevel(logging.INFO)


		logging.info("\nSucessfully started HDP cluster " + cluster.name)
		return 0


	def hdp_node_kerberos_client_create(cluster, node):
		'''
		Create Kerberos client on all HDP nodes
		
		Example:
		curl -H "X-Requested-By:ambari" -u admin:admin -i -X POST \
				 -d '{"host_components" : [{"HostRoles" : {"component_name":"KERBEROS_CLIENT"}}]}' \
				 http://AMBARI_SERVER:8080/api/v1/clusters/CLUSTER_NAME/hosts?Hosts/host_name=HOST_NAME

		'''
		
		ret = 0

		json_data = '{"host_components" : [{"HostRoles" : {"component_name":"KERBEROS_CLIENT"}}]}' 
		logging.debug(json_data)

		url = 'http://' + cluster.ambari_host + ':8080/api/v1/clusters/' \
							+ cluster.name + "/hosts?Hosts/host_name=" \
							+ str(node) 
		logging.debug(url)

#		logging.info("\nCreating Kerberos client on HDP node: " + str(node) + " ...")

		cmd = 'curl -H "X-Requested-By:ambari" -u admin:admin -i -X POST '
		cmd = cmd + " -d " +  " '" + json_data + "' "
		cmd = cmd + url

		logging.debug(cmd)
		ret = cluster.shell_cmd_exec(cmd)
		if ret < 0:
			logging.error("Error: Could not create Kerberos client HDP node: %s", node)
			return -1

		logging.info("Successfully created Kerberos client on HDP node: " + str(node)) 
		return 0



	def hdp_nodes_kerberos_client_create(cluster, manager):
		'''
		Create Kerberos client on all HDP nodes
		
		'''
		ret = 0
		logging.info("\nCreating Kerberos client on HDP nodes ...")


		node = cluster.ambari_host
		ret = cluster.hdp_node_kerberos_client_create(node)
		if ret != 0:
			logging.error("Error: Could not create Kerberos client on ambari node")
			return -1

		count = 0 
		num = 0 
		for node in cluster.config['cluster']['nodes']: 
			num = num + 1
			ret = cluster.hdp_node_kerberos_client_create(node)
			if ret == 0:
				count = count + 1

		# log error based up on how many hdp nodes being configured
		if count == 0:
			logging.error("Error: Could not create Kerberos client on any HDP node")
			return -1

		if count != num:
			logging.warning("Warning: Successfully created Kerberos client only on %d node(s) out of %d node(s)", count, num)
			return 0

		logging.info("Successfully created Kerberos client on HDP nodes")
		return 0

	def hdp_kereros_enable(cluster, manager):
		'''
		# Enable Kerberos 

		Example:
		$ curl -H "X-Requested-By:ambari" -u admin:admin -i -X PUT -d @./payload \
					http://AMBARI_SERVER:8080/api/v1/clusters/CLUSTER_NAME

		'''
		root_logger = logging.getLogger()

		logging.info("\nEnable KERBEROS progress (%): ")


		headers = {'X-Requested-By': 'ambari'}
		url = 'http://' + cluster.ambari_host + ':8080/api/v1/clusters/' + cluster.name 
		logging.debug(url)

        	data = json.load(open(cluster.kerberos_principal))
		json_data=json.dumps(data)
		logging.debug(json_data)
		

		root_logger.setLevel(logging.WARNING)
		res = requests.put(url, headers=headers, json=json_data, auth=(cluster.ambari_username, cluster.ambari_passwd))
		root_logger.setLevel(logging.INFO)

		logging.debug(res)
		logging.debug(res.text)

		if res.status_code == 200: 
			logging.warning("Warning: KERBEROS is already enabled")
			return 0

		if res.raise_for_status() is not None:
			logging.error("Error: Could not enable KERBEROS")
			return -1

		if res.status_code != 202: 
			logging.error("Error: Could not enable KERBEROS")
			return -1

		url = res.json().get('href')
		logging.debug(url)


		progress = 0
		while progress < 100:
			root_logger.setLevel(logging.WARNING)

			res = requests.get(url, headers=headers, auth=(cluster.ambari_username, cluster.ambari_passwd))
			logging.debug(res)
			if res.raise_for_status() is not None:
				logging.error("Error: Could not retrieve status of KERBEROS enable operation")
				return -1

			result = res.json().get('Requests')
			progress = result['progress_percent']
			time.sleep( 5 )
    			sys.stdout.write("\r%d%%" % progress)
			sys.stdout.flush()
			logging.info("Enable KERBEROS progress (%s):", progress)

			root_logger.setLevel(logging.INFO)

		logging.info("\nSuccessfully enabled KERBEROS")
		return 0




	def hdp_kerberos_install(cluster, manager):
		'''
		Install the KERBEROS service and components

		Example:
		$ curl -H "X-Requested-By:ambari" -u admin:admin -i -X PUT \
					-d '{"ServiceInfo": {"state" : "INSTALLED"}}' \
					 http://AMBARI_SERVER:8080/api/v1/clusters/CLUSTER_NAME/services/KERBEROS

		'''
		root_logger = logging.getLogger()

		logging.info("\nKERBEROS service installation progress (%):")

		headers = {'X-Requested-By': 'ambari'}
		url = 'http://' + cluster.ambari_host + ':8080/api/v1/clusters/' \
							+ cluster.name + "/services/KERBEROS"
		logging.debug(url)

		data = {}
		data['ServiceInfo'] = {}
		data['ServiceInfo']['state'] = "INSTALLED"
		json_data = json.dumps(data)
		logging.debug(json_data)

		root_logger.setLevel(logging.WARNING)
		res = requests.put(url, headers=headers, data=json_data, auth=(cluster.ambari_username, cluster.ambari_passwd))
		root_logger.setLevel(logging.INFO)

		logging.debug(res)
		logging.debug(res.text)
		logging.debug(res.status_code)


		if res.status_code == 200: 
			logging.warning("Warning: KERBEROS service is already installed")
			return 0

		if res.raise_for_status() is not None:
			logging.error("Error: Could not install KERBEROS service")
			return -1

		if res.status_code != 202: 
			logging.error("Error: Could not install KERBEROS service")
			return -1

		url = res.json().get('href')
		logging.debug(url)


		progress = 0
		while progress < 100:
			root_logger.setLevel(logging.WARNING)

			res = requests.get(url, headers=headers, auth=(cluster.ambari_username, cluster.ambari_passwd))
			logging.debug(res)

			if res.raise_for_status() is not None:
				logging.error("Error: Could not retrieve status of KERBEROS service install operation")
				return -1

			result = res.json().get('Requests')
			progress = result['progress_percent']
			time.sleep( 5 )
    			sys.stdout.write("\r%d%%" % progress)
			sys.stdout.flush()

			logging.info("KERBEROS service install progress (%s):", progress)
			root_logger.setLevel(logging.INFO)

		logging.info("\nSuccessfully installed KERBEROS service")
		return 0



	
	def kerberos_service_conf_set(cluster, manager):
		'''
		# Add KERBEROS Service to cluster

		Example:
		$curl -H "X-Requested-By:ambari" -u admin:admin -i -X POST \
				http://AMBARI_SERVER:8080/api/v1/clusters/CLUSTER_NAME/services/KERBEROS

		'''

		root_logger = logging.getLogger()

		logging.info("\nAdding KERBEROS Service to cluster ...")

		headers = {'X-Requested-By': 'ambari'}
		url = 'http://' + cluster.ambari_host + ':8080/api/v1/clusters/' + cluster.name 
		logging.debug(url)

        	data = json.load(open(cluster.kerberos_conf))
		json_data=json.dumps(data)
		logging.debug(json_data)
		
		root_logger.setLevel(logging.WARNING)
		res = requests.put(url, headers=headers, json=json_data, auth=(cluster.ambari_username, cluster.ambari_passwd))
		root_logger.setLevel(logging.INFO)

		logging.debug(res)
		logging.debug(res.text)
		logging.debug(res.status_code)

		if res.status_code == 200: 
			logging.info("Successfully added KERBEROS Service\n")
			return 0

		if res.raise_for_status() is not None:
			logging.error("Error: Could not add KERBEROS service")
			return -1

		logging.error("Error: Could not add KERBEROS service")
		return -1




	def kerberos_component_add(cluster, manager):
		'''
		# Add the KERBEROS_CLIENT component to the KERBEROS service

		Example:
		curl -H "X-Requested-By:ambari" -u admin:admin -i -X POST \
			http://AMBARI_SERVER:8080/api/v1/clusters/CLUSTER_NAME/services/KERBEROS/components/KERBEROS_CLIENT

		'''
		root_logger = logging.getLogger()
		logging.info("\nAdding KERBEROS client component to KERBEROS service ...")


		headers = {'X-Requested-By': 'ambari'}
		url = 'http://' + cluster.ambari_host + ':8080/api/v1/clusters/' \
					+ cluster.name + "/services/KERBEROS/components/KERBEROS_CLIENT"
		logging.debug(url)

		root_logger.setLevel(logging.WARNING)
		res = requests.post(url, headers=headers, auth=(cluster.ambari_username, cluster.ambari_passwd))
		root_logger.setLevel(logging.INFO)

		logging.debug(res)
		logging.debug(res.text)
		logging.debug(res.status_code)

		if res.status_code == 201: 
			logging.info("Sucessfully added KERBEROS client component")
			return 0

		if res.status_code == 409: 
			logging.info("Sucessfully added KERBEROS client component")
			#logging.warning("Warning: KERBEROS component already being added")
			return 0

		if res.raise_for_status() is not None:
			logging.error("Error: Could not add KERBEROS client component")
			return -1

		logging.error("Error: Could not add KERBEROS KERBEROS client component")
		return -1		
		


	def kerberos_service_add(cluster, manager):
		'''
		#Add the KERBEROS Service to cluster

		Example:
		curl -H "X-Requested-By:ambari" -u admin:admin -i -X POST \
				 http://AMBARI_SERVER:8080/api/v1/clusters/CLUSTER_NAME/services/KERBEROS

		'''
		root_logger = logging.getLogger()

		logging.info("\nAdding KERBEROS service to the HDP cluster...")


		headers = {'X-Requested-By': 'ambari'}
		url = 'http://' + cluster.ambari_host + ':8080/api/v1/clusters/' \
							+ cluster.name + "/services/KERBEROS"
		logging.debug(url)

		root_logger.setLevel(logging.WARNING)
		res = requests.post(url, headers=headers, auth=(cluster.ambari_username, cluster.ambari_passwd))
		root_logger.setLevel(logging.INFO)

		logging.debug(res)
		logging.debug(res.text)
		logging.debug(res.status_code)

		if res.status_code == 200: 
			logging.info("Sucessfully added KERBEROS service")
			return 0

		if res.status_code == 409: 
			logging.info("Sucessfully added KERBEROS service")
			#logging.warning("Warning: KERBEROS service already being added")
			return 0

		if res.raise_for_status() is not None:
			logging.error("Error: Could not add KERBEROS service")
			return -1

		logging.info("Error: Could not add KERBEROS service")
		return -1


	def hdp_cluster_kerberization(cluster, manager):
		'''

		# KERBEROS Service to cluster 
		Example:
		$curl -H "X-Requested-By:ambari" -u admin:admin -i -X POST \
				http://AMBARI_SERVER:8080/api/v1/clusters/CLUSTER_NAME/services/KERBEROS
		'''

		ret = 0 
		# Add the KERBEROS Service to cluster
		ret = cluster.kerberos_service_add(manager)
		if ret < 0:
			return ret

		# Add the KERBEROS_CLIENT component to the KERBEROS service
		ret = cluster.kerberos_component_add(manager)
		if ret < 0:
			return ret

		# Create and set KERBEROS service configurations
		ret = cluster.kerberos_service_conf_set(manager)
		if ret < 0:
			return ret


		# Create the KERBEROS_CLIENT host component	
		ret = cluster.hdp_nodes_kerberos_client_create(manager)
		if ret < 0:
			return ret

		# Install the KERBEROS service and components
		ret = cluster.hdp_kerberos_install(manager)
		if ret < 0:
			return ret

		# Stop all services
		ret = cluster.hdp_cluster_stop(manager)
		if ret < 0:
			return ret


		# Enable Kerberos
		ret = cluster.hdp_kereros_enable(manager)
		if ret < 0:
			return ret

		# Start all services
		ret = cluster.hdp_cluster_start(manager)
		if ret < 0:
			return ret

		return 0








'''
Azure Cloud Manager to interact with outside world
'''
class azure_hdp_manager_init(object):
	def __init__(manager):
		manager.init = True
		logging.info("\nSuccessfully initilized Azure HDP Cloud Manager")
		return None

	def parse_args(manager):
		manager.parser = argparse.ArgumentParser(description='Manages Hortonworks HDP on Azure Cloud.')
		manager.parser.add_argument('-c', '--config', dest='hdp_config', \
							help='HDP Cluster YAML Config file')

		manager.parser.add_argument('-i', '--install', action="store_true", \
							dest='hdp_install', default=False, \
							help='HDP Cluster YAML Config file')

		manager.parser.add_argument('-k', '--kerberos', action='store_true', \
							dest='kerberos_install', default=False, \
							help='Kerberize HDP Cluster')
		manager.parser.add_argument('-s', '--stop', action='store_true', \
							dest='hdp_cluster_stop', default=False, \
							help='Stop HDP Cluster')
#		manager.parser.add_argument('--stop', nargs='?',\
#						help='Stop all HDP Cluster Services')
#		manager.parser.add_argument('--restart', nargs='+',\
#						help='Restart all HDP Cluster Services')
		manager.args = manager.parser.parse_args()
		logging.debug("manager.args: %s", manager.args) 
		if manager.args is None:
			manager.parser.print_help()	
			return -1
		return 0 

	def process_args(manager):
		ret = 0 
		if manager.args.hdp_config is None:
			logging.error("Error: HDP Cluster Configurartion file is missing")
			manager.parser.print_help()	
			return -1

		cluster = cluster_init()

		ret = cluster.hdp_config(manager.args.hdp_config)
		if ret < 0:
			logging.error("Error: Invalid HDP Cluster YAML config file")
			return ret

		if manager.args.hdp_install is True:
			logging.info("\nHDP cluster installation started ...")
			ret = cluster.hdp_ambari_configure(manager)
			if ret < 0:
				return ret

			ret = cluster.hdp_nodes_configure(manager)
			if ret < 0:
				return ret

			ret = cluster.hdp_blueprint_create(manager)
			if ret < 0:
				return ret

			ret = cluster.hdp_installation(manager)
			if ret < 0:
				return ret

			ret = cluster.hdp_installation_status(manager)
			if ret < 0:
				return ret

		if manager.args.kerberos_install is True:
			logging.info("\nHDP kerberization process has been started ...")
			time.sleep( 10 )
			ret = cluster.hdp_cluster_kerberization(manager)
			if ret < 0:
				return ret


		if manager.args.hdp_cluster_stop is True:
			logging.info("\nStopping all HDP services ...\n")
			ret = cluster.hdp_cluster_stop(manager)
			if ret < 0:
				return ret

		return 0

if __name__ == '__main__':
	''' main entry point '''

	ret = 0
	logging.basicConfig(format='%(message)s', level=logging.INFO)
	#logging.basicConfig(format='%(message)s', level=logging.DEBUG)
	#logging.basicConfig(filename='/tmp/cloudmanager.log', format='%(asctime)s %(message)s', filemode='w', level=logging.DEBUG)
	sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
	res = ''

	manager = azure_hdp_manager_init()

	ret = manager.parse_args()
#	if ret < 0:
#		return ret

	ret = manager.process_args()
#	if ret < 0:
#		return ret

	#return ret

