'''
Azure HDP Manager: Implementation to manage HDP (Hortonworks Data Flatform) on Azure Cloud

Version: v1.0 01/02/2018

Authors: Anil Dahiya anil.dahiya@hashmapinc.com

Fixes:

'''
import os
import sys
import argparse
from subprocess import Popen, PIPE, STDOUT



class azure_hdp_manager(object):
	def __init__(manager):
		res = False
#		print sys._getframe().f_code.co_name + ": IN"
		manager.init = True
		manager.workdir = "/home/cddadmin"
		manager.cluster_username = "cddadmin"
		manager.cluster_privkey = manager.workdir + "/" + "cluster.privkey"
		manager.chef_knife_config = manager.workdir + "/" + "chef-repo/.chef/knife.rb"
#		print manager.chef_knife_config
#		print sys._getframe().f_code.co_name + ": Exit "
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
					+ "-x " + manager.cluster_username \
					+ " -r " + role \
					+ " --config " + manager.chef_knife_config \
					+ str(manager.args.edgenode)
				
		print "\n" + cmd 
		res = manager.shell_cmd_exec(cmd)
		return res
#		print sys._getframe().f_code.co_name + ": Exit "

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
						+ "-x " + manager.cluster_username \
						+ " -r " + role \
						+ " --config " + manager.chef_knife_config \
						+ str(node)
			print "\n" + cmd 
	#		res = manager.shell_cmd_exec(cmd)
			print res
#		print sys._getframe().f_code.co_name + ": Exit "

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

		ambari_server = str(manager.args.edgenode[0])
		print ambari_server

		cmd = 'curl -H "X-Requested-By: ambari" -X POST -u admin:admin' \
							+ " http://" + ambari_server \
									+ ":8080/api/v1/blueprints/" + manager.blueprint_name \
							+ " -d @" +  str(manager.args.blueprint)

		print "\n" + cmd 
	#	res = manager.shell_cmd_exec(cmd)
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

		ambari_server = str(manager.args.edgenode[0])
		print "HDP ambari server: " + ambari_server

		cmd = 'curl -H "X-Requested-By: ambari" -X POST -u admin:admin'\
							+ " http://" + ambari_server \
									+ ":8080/api/v1/blueprints/" + manager.blueprint_name \
							+ " -d @" +  str(manager.args.hostmap)

		print "\n" + cmd 
	#	res = manager.shell_cmd_exec(cmd)
		return res
#	
#		print sys._getframe().f_code.co_name + ": Exit "


	

	def parse_args(manager):
#		print sys._getframe().f_code.co_name + ": IN"
		manager.parser = argparse.ArgumentParser(description='Manages Hortonworks HDP on Azure Cloud.')
		manager.parser.add_argument('-e', '--edgenode', nargs='+',\
											help='HDP edge node hostname')
		manager.parser.add_argument('-n', '--hdpnodes', nargs='+',\
											help='List of HDP nodes hostnames')
		manager.parser.add_argument('-b', '--blueprint',\
				 							help='HDP Cluster Blueprint JSON file')
		manager.parser.add_argument('-m', '--hostmap',\
											help='HDP Cluster hostname mapping JSON file')

		manager.args = manager.parser.parse_args()
		print "HDP edge node: " + str(manager.args.edgenode)
		print "HDP nodes: " + str(manager.args.hdpnodes)
		print "Blueprint JSON file pathname: " + str(manager.args.blueprint)
		print "Hostmapping JSON file pathname: " + str(manager.args.hostmap)
#		print sys._getframe().f_code.co_name + ": Exit "

		return manager.args

	def process_args(manager):
#		print sys._getframe().f_code.co_name + ": IN"
		if manager.args.edgenode is None:
			print "Error: HDP edge node hostname is missing"
			manager.parser.print_help()	
			return
			
		if manager.args.hdpnodes is None:
			print "Error: List of HDP nodes hostname is missing"
			manager.parser.print_help()	
			return

		if manager.args.blueprint is None:
			print "Error: HDP Cluster Blueprint JSON file pathname is missing"
			manager.parser.print_help()	
			return

		if manager.args.hostmap is None:
			print "Error: HDP Cluster hostname mapping JSON file pathname is missing" 
			manager.parser.print_help()	
			return

		manager.hdp_ambari_server_node_configure()

		manager.hdp_ambari_agent_node_configure()

		manager.hdp_blueprint_create()

		manager.hdp_installation()
#		print sys._getframe().f_code.co_name + ": Exit "



if __name__ == '__main__':
	''' main entry point '''
	sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
	res = ''
	#initialize hdp manager
	manager = azure_hdp_manager()

	# parse command line arguments
	args = manager.parse_args()

	# process command line argument
	res = manager.process_args()

