import yaml

"""
cluster:
	name: walgreens_hdp_spark
	blueprint: walgreens_hdp_spark.json
	hostmapping: walgreens_hdp_spark-hostmap.json
	ssh:
		- username: cddadmin
		- privkey: ./priv-akhanolk
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

"""

with open("hdp_cluster_config.yml", 'r') as ymlfile:
    cluster = yaml.load(ymlfile)



for section in cluster:
    print(section)
print(cfg['mysql'])
print(cfg['other'])
print(cfg['mysql']['passwd'])
print(type(cfg['mysql']['passwd'])[1])

