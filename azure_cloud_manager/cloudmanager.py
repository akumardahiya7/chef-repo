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
		res = []

		cmd = cmd + "> /dev/null 2>&1" 
		logging.debug("\nShell command to be executed: " + cmd)
#		return res

		process = Popen(cmd, bufsize=2048, stdin=PIPE, stdout=PIPE, shell=True)
		(child_stdin, child_stdout) = (process.stdin, process.stdout)
		if process.wait() != 0:
			logging.error("Error: Could not executed shell command: %s", cmd)
		for line in child_stdout:
			# the real code does filtering here
			line = line.rstrip()
			res.append(line)
			logging.debug(line)
		logging.debug("Shell command returned output: " + str(res))
		return res

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
			logging.error("Error: HDP Cluster Blueprint file contains invalid JSON Format")
			return ret

		cluster.hostmap = cluster.config['cluster']['hostmap']
		logging.info("\nHDP Cluster Blueprint Hostmap: " + cluster.hostmap)
		ret = cluster.json_validator(cluster.hostmap)
		if(ret == False):
			logging.error("Error: HDP Cluster Hostmapping file contains invalid JSON Format")
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

		return True

	def hdp_ambari_configure(cluster, manager):
		#knife bootstrap -i ~/cluster-ssh-privkey -x cddadmin --sudo -r role['ambari-server'] hdp-en01
#		print sys._getframe().f_code.co_name + ": IN"
		res = []
	#	print "Configure ambari node"


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
		res = cluster.shell_cmd_exec(cmd)
		logging.info("\nSuccessfully configured Ambari Server")
		return res

	def hdp_node_configure(cluster, node):
		'''
		Configure all HDP nodes with ambari-agent role 

		Example:
		knife bootstrap -i ~/cluster-ssh-privkey -x cddadmin --sudo -r role['ambari-agent'] hdp-en01
		'''
		role = "role['ambari-agent']"

		logging.info("\nConfiguring HDP node: " + str(node) + " ...")
		res = []
		cmd = "knife bootstrap --sudo " \
				+ " -i " + cluster.ssh_key \
				+ " -x " + cluster.username \
				+ " -r " + role \
				+ " " + node  + "> /dev/null 2>&1"

		res = cluster.shell_cmd_exec(cmd)
		logging.info("\nSuccessfully configured HDP HDP node: " + str(node)) 
		return res


	def hdp_nodes_configure(cluster, manager):
		'''
		Configure all HDP nodes with ambari-agent role 
		
		Example:
		knife bootstrap -i ~/cluster-ssh-privkey -x cddadmin --sudo -r role['ambari-agent'] hdp-en01
		'''
		logging.info("\nConfiguring HDP nodes ...")
		role = "role['ambari-agent']"

		for node in cluster.config['cluster']['nodes']: 
			cluster.hdp_node_configure(node)

		logging.info("\nSuccessfully configured HDP nodes")


	def hdp_blueprint_create(cluster, manager):
		'''
		Create HDP blueprint
		
		Example:
		$ curl -H "X-Requested-By: ambari" -X POST -u admin:admin \
				http://hdp-en01:8080/api/v1/blueprints/hdp-small-default @hdp-small-default.json
		'''

		res = []

		logging.info("\nUploading HDP blueprint: " + cluster.blueprint + " ...")
		cmd = 'curl -H "X-Requested-By: ambari" -X POST '\
				+ ' -u ' + cluster.ambari_username + ':' + cluster.ambari_passwd \
				+ ' http://' + cluster.ambari_host + ':8080/api/v1/blueprints/' + cluster.name \
				+ ' -d @' +  str(cluster.blueprint)

		res = cluster.shell_cmd_exec(cmd)
		logging.info("\nSucessfully uploaded HDP blueprint " + cluster.blueprint)
		return res


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
		root_logger = logging.getLogger()
		logging.info("\nHDP Cluster installation progress (%):")
		root_logger.setLevel(logging.WARNING)

		headers = {'X-Requested-By': 'ambari'}
		url = 'http://' + cluster.ambari_host + ':8080/api/v1/clusters/' + cluster.name + "/requests/1"
		logging.debug(url)

		res = requests.get(url, headers=headers, auth=(cluster.ambari_username, cluster.ambari_passwd))
		logging.debug(res)

		progress = 0
		while progress < 100:
			res = requests.get(url, headers=headers, auth=(cluster.ambari_username, cluster.ambari_passwd))
			if res.raise_for_status() is not None:
				print "Error: HDP installation has failed"
				return False
			result = res.json().get('Requests')
			progress = result['progress_percent']
			time.sleep( 5 )
    			sys.stdout.write("\r%d%%" % progress)
			sys.stdout.flush()

		root_logger.setLevel(logging.INFO)
		logging.info("\nCluster build is complete")
		return res


	def hdp_installation(cluster, manager):
		'''
		Install HDP cluster using blueprint	

		Example:
		$curl -H "X-Requested-By: ambari" -X POST -u admin:admin \
					http://hdp-en01:8080/api/v1/clusters/hdp-small-default -d @hostmap.json
		'''

		res = []
		logging.info("\nInstalling HDP Clutser: " + cluster.name + " ...")
		cmd = 'curl -H "X-Requested-By: ambari" -X POST '\
				+ ' -u ' + cluster.ambari_username + ':' + cluster.ambari_passwd \
				+ " http://" + cluster.ambari_host + ":8080/api/v1/clusters/" + cluster.name \
				+ " -d @" +  str(cluster.hostmap)

		res = cluster.shell_cmd_exec(cmd)
		logging.info("\nHDP Cluster installation has been started, access HDP Ambari dashboard using link"\
						 + '\nhttp://' + cluster.ambari_host + ':8080/\n')
		return res

	def hdp_cluster_stop(cluster, manager):
		'''
		Stop HDP cluster

		Example:
		$curl -u admin:admin -i -H 'X-Requested-By: ambari' -X PUT -d \
				'{"RequestInfo": \
					{"context": "_PARSE_.STOP.ALL_SERVICES","operation_level": \
						{"level":"CLUSTER","cluster_name":"hdpspark"}\
					},\
					"Body": {"ServiceInfo":	{"state":"INSTALLED"}}\
				}'\
				http://hdp-an01.gombe.com:8080/api/v1/clusters/hdpspark/services
		'''

		logging.info("\nStopping all services of HDP Clutser: " + cluster.name + " ...")
#		cmd = 'curl -i -H "X-Requested-By: ambari"-X PUT '\
#				+ ' -u ' + cluster.ambari_username + ':' + cluster.ambari_passwd \
#				+ ' -d {"RequestInfo": '\
#					+ '{"context": "_PARSE_.STOP.ALL_SERVICES","operation_level":'\
#						+ '{"level":"CLUSTER","cluster_name":"' + cluster.name + '"}' \
#					+ '},'\
#					+ ' "Body": {"ServiceInfo": {"state":"INSTALLED"}}'\
#				+ '}'\
#				+ " http://" + cluster.ambari_host \
#					+ ":8080/api/v1/clusters/" + cluster.name + '/services'\
#
#		res = cluster.shell_cmd_exec(cmd)
		logging.info("\nSucessfully stopped HDP cluster " + cluster.name)
		return res

	def hdp_cluster_start(cluster, manager):
		'''
		Start HDP cluster

		Example:
		$curl -u admin:admin -i -H 'X-Requested-By: ambari' -X PUT -d \
				'{"RequestInfo": \
					{"context": "_PARSE_.START.ALL_SERVICES","operation_level": \
						{"level":"CLUSTER","cluster_name":"hdpspark"}\
					},\
					"Body": {"ServiceInfo":	{"state":"STARTED"}}\
				}'\
				http://hdp-an01.gombe.com:8080/api/v1/clusters/hdpspark/services
		'''

		print "\nStarting all services of HDP Clutser: " + cluster.name + " ..." 
		cmd = 'curl -i -H "X-Requested-By: ambari" -X PUT '\
				+ ' -u ' + cluster.ambari_username + ':' + cluster.ambari_passwd \
				+ ' -d ' \
				+ "'" + '{"RequestInfo": '\
					+ '{"context": "_PARSE_.START.ALL_SERVICES","operation_level":'\
						+ '{"level":"CLUSTER","cluster_name":"' + cluster.name + '"}' \
					+ '},'\
					+ ' "Body": {"ServiceInfo": {"state":"STARTED"}}'\
				+ '}' +  "'" \
				+ " http://" + cluster.ambari_host + ":8080/api/v1/clusters/" + cluster.name + '/services'
		res = cluster.shell_cmd_exec(cmd)
		print json.dumps(res, indent=4)
		json_string = json.dumps(res)
		datastore = json.loads(json_string) 
		print datastore[16]
	
		print "\nSucessfully started HDP cluster " + cluster.name 
		return res

	def hdp_cluster_start(cluster, manager):
		'''
		Start HDP cluster

		Example:
		$curl -u admin:admin -i -H 'X-Requested-By: ambari' -X PUT -d \
				'{"RequestInfo": \
					{"context": "_PARSE_.START.ALL_SERVICES","operation_level": \
						{"level":"CLUSTER","cluster_name":"hdpspark"}\
					},\
					"Body": {"ServiceInfo":	{"state":"STARTED"}}\
				}'\
				http://hdp-an01.gombe.com:8080/api/v1/clusters/hdpspark/services
		'''

		print "\nStarting all services of HDP Clutser: " + cluster.name + " ..." 
		cmd = 'curl -i -H "X-Requested-By: ambari" -X PUT '\
				+ ' -u ' + cluster.ambari_username + ':' + cluster.ambari_passwd \
				+ ' -d ' \
				+ "'" + '{"RequestInfo": '\
					+ '{"context": "_PARSE_.START.ALL_SERVICES","operation_level":'\
						+ '{"level":"CLUSTER","cluster_name":"' + cluster.name + '"}' \
					+ '},'\
					+ ' "Body": {"ServiceInfo": {"state":"STARTED"}}'\
				+ '}' +  "'" \
				+ " http://" + cluster.ambari_host + ":8080/api/v1/clusters/" + cluster.name + '/services'
		res = cluster.shell_cmd_exec(cmd)
		print json.dumps(res, indent=4)
		json_string = json.dumps(res)
		datastore = json.loads(json_string) 
		print datastore[16]
	
		print "\nSucessfully started HDP cluster " + cluster.name 
		return res



'''
Azure Cloud Manager to interact with outside world
'''
class azure_hdp_manager_init(object):
	def __init__(manager):
		res = False
		manager.init = True
		logging.info("\nSuccessfully initilized Azure HDP Cloud Manager")
		return

	def parse_args(manager):
		manager.parser = argparse.ArgumentParser(description='Manages Hortonworks HDP on Azure Cloud.')
		manager.parser.add_argument('-c', '--config', nargs='+',\
						help='HDP Cluster YAML Config file')
		manager.parser.add_argument('--start', nargs='?',\
						help='Start all HDP Cluster Services')
#		manager.parser.add_argument('--stop', nargs='?',\
#						help='Stop all HDP Cluster Services')
#		manager.parser.add_argument('--restart', nargs='+',\
#						help='Restart all HDP Cluster Services')
		manager.args = manager.parser.parse_args()
		if manager.args is None:
			manager.parser.print_help()	
			return
		return manager.args

	def process_args(manager):
		if manager.args.config is None:
			logging.error("Error: HDP Cluster Configurartion file is missing")
			manager.parser.print_help()	
			return

		cluster = cluster_init()
		cluster.hdp_config(str(manager.args.config[0]))
		cluster.hdp_ambari_configure(manager)
		cluster.hdp_nodes_configure(manager)
		cluster.hdp_blueprint_create(manager)
		cluster.hdp_installation(manager)
		cluster.hdp_installation_status(manager)
#		cluster.hdp_cluster_stop(manager)
#		cluster.hdp_cluster_start(manager)

if __name__ == '__main__':
	''' main entry point '''
	logging.basicConfig(format='%(message)s', level=logging.INFO)
#	logging.basicConfig(filename='example.log', format='%(asctime)s %(message)s', filemode='w', level=logging.DEBUG)
	sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
	res = ''

	manager = azure_hdp_manager_init()
	args = manager.parse_args()
	res = manager.process_args()

