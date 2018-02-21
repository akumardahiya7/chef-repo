import yaml

"""
mysql:
    host: localhost
    user: root
    passwd: my secret password
    db: write-math
other:
    preprocessing_queue:
        - preprocessing.scale_and_center
        - preprocessing.dot_reduction
        - preprocessing.connect_lines
    use_anonymous: yes

"""

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

for section in cfg:
    print(section)
#print(cfg['mysql'])
#print(cfg['other'])
#print(cfg['mysql']['passwd'])
print(cfg['other']['preprocessing_queue'])
#
