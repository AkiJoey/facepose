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
		mtx = np.array(obj['mtx'])
		dist = np.array(obj['dist'])

		return mtx, dist
