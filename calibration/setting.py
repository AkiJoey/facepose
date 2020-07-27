import os
import yaml

# get config path
root_path = os.getcwd() + '/'
config_path = root_path + 'config.yml'

def write(mtx, dist):
	with open(config_path, encoding = 'utf-8') as config:
		obj = yaml.load(config.read(), Loader = yaml.FullLoader)

		# set monocular config
		obj['mtx'] = mtx.tolist()
		obj['dist'] = dist.tolist()
	
		yaml.dump(obj, open(config_path, 'w'))
