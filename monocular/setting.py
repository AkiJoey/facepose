import os
import yaml
import numpy as np

# get config path
root_path = os.getcwd() + '/'
config_path = root_path + 'config.yml'

def read():
	with open(config_path, encoding = 'utf-8') as config:
		obj = yaml.load(config.read(), Loader = yaml.FullLoader)

		# get monocular config
		mtx = np.array(obj['monocular']['mtx'])
		dist = np.array(obj['monocular']['dist'])

		return mtx, dist

def write(mtx, dist):
	with open(config_path, encoding = 'utf-8') as config:
		obj = yaml.load(config.read(), Loader = yaml.FullLoader)

		# set monocular config
		obj['monocular']['mtx'] = mtx.tolist()
		obj['monocular']['dist'] = dist.tolist()
	
		yaml.dump(obj, open(config_path, 'w'))
