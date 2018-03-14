'''
Azure HDP cluster: Implementation to manage HDP (Hortonworks Data Flatform) on Azure Cloud

Version: v1.0 01/02/2018

Authors: Anil Dahiya anil.dahiya@hashmapinc.com

Fixes:

'''
import os
import sys
import argparse
from subprocess import Popen, PIPE, STDOUT
import yaml
import json

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

		print "\n" + cmd 
		return res

		process = Popen(cmd, bufsize=2048, stdin=PIPE, stdout=PIPE, shell=True)
		(child_stdin, child_stdout) = (process.stdin, process.stdout)
		if process.wait() != 0:
			print "Error: Shell command execution failed"
		for line in child_stdout:
			# the real code does filtering here
			line = line.rstrip()
			res.append(line)
			print line
		print "Shell command returned output: " + str(res)
		return res

	def json_validator(cluster, filename):
		try:
        		json.load(open(filename))
        		return True
    		except ValueError as error:
        		print("Error: Invalid json in file %s: %s" % (filename, error))
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
		print "\nPassed HDP Cluster configuration is: "
		print(cluster.config['cluster'])
		print(cluster.config['database'])

		cluster.name = cluster.config['cluster']['name']
		print "\nHDP Cluster Name: " + cluster.name

		cluster.blueprint = cluster.config['cluster']['blueprint']
		print "\nHDP Cluster Blueprint: " + cluster.blueprint
		ret = cluster.json_validator(cluster.blueprint)
		if(ret == False):
			print("\nError: HDP Cluster Blueprint file contains invalid JSON Format")
			return ret

		cluster.hostmap = cluster.config['cluster']['hostmap']
		print "\nHDP Cluster Blueprint Hostmap: " + cluster.hostmap
		ret = cluster.json_validator(cluster.hostmap)
		if(ret == False):
			print("\nError: HDP Cluster Hostmapping file contains invalid JSON Format")
			return ret

		cluster.username = cluster.config['cluster']['ssh']['username']
		print "\nHDP Cluster SSH username: " + cluster.username

		cluster.ssh_key = cluster.config['cluster']['ssh']['privkey']
		print "\nHDP Cluster SSH private keyfile: " + cluster.ssh_key

		cluster.ambari = cluster.config['cluster']['ambari']
		cluster.ambari.host = cluster.config['cluster']['ambari']['host']
		print "\nHDP Cluster Ambari Server: " + cluster.ambari.host

		print "\nHDP Cluster Nodes are:" 
		print(cluster.config['cluster']['nodes'])

		return True

	def hdp_ambari_configure(cluster, manager):
		#knife bootstrap -i ~/cluster-ssh-privkey -x cddadmin --sudo -r role['ambari-server'] hdp-en01
#		print sys._getframe().f_code.co_name + ": IN"
		res = []
		role = "role['ambari-server']"
		print "\nHDP Cluster Name: " + cluster.name
		cmd = "knife bootstrap --sudo " \
				+ " -i " + cluster.ssh_key \
				+ " -x " + cluster.username \
				+ " -r " + role \
				+ " " + cluster.ambari
				
		print("\nConfiguring ambari server ...")
		res = cluster.shell_cmd_exec(cmd)
		print("\nSuccessfully configured Ambari Server")
		return res

	def hdp_node_configure(cluster, node):
		'''
		Configure all HDP nodes with ambari-agent role 

		Example:
		knife bootstrap -i ~/cluster-ssh-privkey -x cddadmin --sudo -r role['ambari-agent'] hdp-en01
		'''
		role = "role['ambari-agent']"

		print "\nConfiguring HDP node: " + str(node) + " ..." 
		res = []
		cmd = "knife bootstrap --sudo " \
				+ " -i " + cluster.ssh_key \
				+ " -x " + cluster.username \
				+ " -r " + role \
				+ " " + node
		res = cluster.shell_cmd_exec(cmd)
		print "\nSuccessfully configured HDP HDP node: " + str(node)  
		return res


	def hdp_nodes_configure(cluster, manager):
		'''
		Configure all HDP nodes with ambari-agent role 
		
		Example:
		knife bootstrap -i ~/cluster-ssh-privkey -x cddadmin --sudo -r role['ambari-agent'] hdp-en01
		'''
		print("\nConfiguring HDP nodes ...")
		role = "role['ambari-agent']"

		for node in cluster.config['cluster']['nodes']: 
			cluster.hdp_node_configure(node)

		print("\nSuccessfully configured HDP nodes")


	def hdp_blueprint_create(cluster, manager):
		'''
		Create HDP blueprint
		
		Example:
		$ curl -H "X-Requested-By: ambari" -X POST -u admin:admin \
				http://hdp-en01:8080/api/v1/blueprints/hdp-small-default @hdp-small-default.json
		'''

		res = []

		print "\nUploading HDP blueprint: " + cluster.blueprint + " ..." 
		cmd = 'curl -H "X-Requested-By: ambari" -X POST -u admin:admin' \
					+ " http://" + cluster.ambari \
					+ ":8080/api/v1/blueprints/" + cluster.name \
					+ " -d @" +  str(cluster.blueprint)
		res = cluster.shell_cmd_exec(cmd)
		print "\nSucessfully uploaded HDP blueprint " + cluster.blueprint 
		return res

	def hdp_installation(cluster, manager):
		'''
		Install HDP cluster using blueprint	

		Example:
		$curl -H "X-Requested-By: ambari" -X POST -u admin:admin \
					http://hdp-en01:8080/api/v1/clusters/hdp-small-default -d @hostmap.json
		'''

		res = []
		print "\nInstalling HDP Clutser: " + cluster.name + " ..." 
		cmd = 'curl -H "X-Requested-By: ambari" -X POST -u admin:admin'\
					+ " http://" + cluster.ambari \
					+ ":8080/api/v1/clusters/" + cluster.name \
					+ " -d @" +  str(cluster.hostmap)

		res = cluster.shell_cmd_exec(cmd)
		print "\nSucessfully created HDP cluster " + cluster.name 
		return res

	def hdp_cluster_stop(cluster, manager):
		'''
		Stop HDP cluster

		Example:
		$curl -u admin:admin -i -H 'X-Requested-By: ambari' -X PUT -d \
				'{"RequestInfo": \
					{"context": "_PARSE_.STOP.ALL_SERVICES","operation_level": \
						{"level":"CLUSTER","cluster_name":"hdpspark"}\
					},"Body": {"ServiceInfo":\
						{"state":"INSTALLED"}\
					}\
				}' http://hdp-an01.gombe.com:8080/api/v1/clusters/hdpspark/services
		'''

		res = []
		print "\nInstalling HDP Clutser: " + cluster.name + " ..." 
		cmd = 'curl -H "X-Requested-By: ambari" -X POST -u admin:admin'\
					+ " http://" + cluster.ambari \
					+ ":8080/api/v1/clusters/" + cluster.name \
					+ " -d @" +  str(cluster.hostmap)

		res = cluster.shell_cmd_exec(cmd)
		print "\nSucessfully created HDP cluster " + cluster.name 
		return res

'''
Azure Cloud Manager to interact with outside world
'''
class azure_hdp_manager_init(object):
	def __init__(manager):
		res = False
		manager.init = True
		print("\nSuccessfully initilized Azure HDP Cloud Manager")
		return

	def parse_args(manager):
		manager.parser = argparse.ArgumentParser(description='Manages Hortonworks HDP on Azure Cloud.')
		manager.parser.add_argument('-c', '--config', nargs='+',\
						help='HDP Cluster YAML Config file')
		manager.parser.add_argument('--start', nargs='+',\
						help='Start all HDP Cluster Services')
		manager.parser.add_argument('--stop', nargs='+',\
						help='Stop all HDP Cluster Services')
		manager.parser.add_argument('--restart', nargs='+',\
						help='Restart all HDP Cluster Services')
		manager.args = manager.parser.parse_args()
		if manager.args is None:
			manager.parser.print_help()	
			return
		return manager.args

	def process_args(manager):
		if manager.args.config is None:
			print "\nError: HDP Cluster Configurartion file is missing"
			manager.parser.print_help()	
			return

		cluster = cluster_init()
		cluster.hdp_config(str(manager.args.config[0]))
#		cluster.hdp_ambari_configure(manager)
#		cluster.hdp_nodes_configure(manager)
#		cluster.hdp_blueprint_create(manager)
#		cluster.hdp_installation(manager)

if __name__ == '__main__':
	''' main entry point '''
	sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
	res = ''

	manager = azure_hdp_manager_init()
	args = manager.parse_args()
	res = manager.process_args()

