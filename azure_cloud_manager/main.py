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

class cluster_init(object):
	def __init__(cluster):
		res = False
		cluster.init = True
		print("\nSuccessfully initilized Clusterr")
		return

	def config(cluster, config):
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
		print "check"
		print config
		with open(config, 'r') as ymlfile:
			cfg = yaml.load(ymlfile)

		for section in cfg.config:
			print(section)
		print(cfg['cluster'])
		print(cfg['database'])


		return res
		print sys._getframe().f_code.co_name + ": Exit "





class azure_hdp_manager_init(object):
	def __init__(manager):
		res = False
		manager.init = True
		print("\nSuccessfully initilized Azure HDP Cloud Manager")
		return

	def shell_cmd_exec(manager, cmd):
		res = []
		print "cmd : " + cmd

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


	def hdp_ambari_server_node_configure(manager):
		#knife bootstrap -i ~/cluster-ssh-privkey -x cddadmin --sudo -r role['ambari-server'] hdp-en01
#		print sys._getframe().f_code.co_name + ": IN"
		res = []
		role = "role['ambari-server']"
		cmd = "knife bootstrap --sudo " \
					+ " -i " + manager.cluster_privkey \
					+ " -x " + manager.cluster_username \
					+ " -r " + role \
					+ " --config " + manager.chef_knife_config \
					+ " " + str(manager.args.ambarinode[0])
				
		print "\n" + cmd 
#		res = manager.shell_cmd_exec(cmd)
		return res
		print sys._getframe().f_code.co_name + ": Exit "

	def hdp_ambari_agent_node_configure(manager):
		#knife bootstrap -i ~/cluster-ssh-privkey -x cddadmin --sudo -r role['ambari-agent'] hdp-en01
		print sys._getframe().f_code.co_name + ": IN"

		'''
		Configure all HDP nodes with ambari-agent role 
		'''
		role = "role['ambari-agent']"
		for node in manager.args.hdpnodes: 
			print "Configuring HDP node " + str(node) + " with ambari-agent role" 
			res = []
			cmd = "knife bootstrap --sudo " \
						+ " -i " + manager.cluster_privkey \
						+ " -x " + manager.cluster_username \
						+ " -r " + role \
						+ " --config " + manager.chef_knife_config \
						+ " " + str(node)
			print "\n" + cmd 
#			res = manager.shell_cmd_exec(cmd)
			print res
		print sys._getframe().f_code.co_name + ": Exit "

	def hdp_blueprint_create(manager):
		'''
		Create HDP blueprint
		
		Example:
		$ curl -H "X-Requested-By: ambari" -X POST -u admin:admin \
									http://hdp-en01:8080/api/v1/blueprints/hdp-small-default @hdp-small-default.json
		'''
		res = []
		blueprint =  manager.args.blueprint
		blueprint_name = blueprint.split('.')
		manager.blueprint_name = str(blueprint_name[0]) 
		print " HDP blueprint name: " + manager.blueprint_name 

		ambari_server = str(manager.args.ambarinode[0])
		print ambari_server

		cmd = 'curl -H "X-Requested-By: ambari" -X POST -u admin:admin' \
							+ " http://" + ambari_server \
									+ ":8080/api/v1/blueprints/" + manager.blueprint_name \
							+ " -d @" +  str(manager.args.blueprint)

		print "\n" + cmd 
#		res = manager.shell_cmd_exec(cmd)
		return res

	def hdp_installation(manager):
		'''
		Install HDP cluster using blueprint	

		Example:
		$curl -H "X-Requested-By: ambari" -X POST -u admin:admin \
									http://hdp-en01:8080/api/v1/clusters/hdp-small-default -d @hostmap.json
		'''

		res = []
		print "HDP blueprint name: " + manager.blueprint_name 

		ambari_server = str(manager.args.ambarinode[0])
		print "HDP ambari server: " + ambari_server

		cmd = 'curl -H "X-Requested-By: ambari" -X POST -u admin:admin'\
							+ " http://" + ambari_server \
									+ ":8080/api/v1/blueprints/" + manager.blueprint_name \
							+ " -d @" +  str(manager.args.hostmap)

		print "\n" + cmd 
#		res = manager.shell_cmd_exec(cmd)
		return res
		print sys._getframe().f_code.co_name + ": Exit "





	def parse_args(manager):
		manager.parser = argparse.ArgumentParser(description='Manages Hortonworks HDP on Azure Cloud.')
		manager.parser.add_argument('-c', '--config', nargs='+',\
											help='HDP Cluster YAML Config file')
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
		cluster.config(str(manager.args.config[0]))
#		cluster_config_init()

#		manager.hdp_ambari_server_node_configure()

#		manager.hdp_ambari_agent_node_configure()

#		manager.hdp_blueprint_create()

#		manager.hdp_installation()
		print sys._getframe().f_code.co_name + ": Exit "



if __name__ == '__main__':
	''' main entry point '''
	sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
	res = ''

	manager = azure_hdp_manager_init()
	args = manager.parse_args()
	res = manager.process_args()

