import os
import yaml
import numpy as np

# get config path
root_path = os.getcwd() + '/'
config_path = root_path + 'config.yml'

def read():
	with open(config_path, encoding = 'utf-8') as config:
		obj = yaml.load(config.read(), Loader = yaml.FullLoader)

		# get binocular config
		mtx1 = np.array(obj['binocular']['mtx1'])
		dist1 = np.array(obj['binocular']['dist1'])
		mtx2 = np.array(obj['binocular']['mtx2'])
		dist2 = np.array(obj['binocular']['dist2'])
		rvecs = np.array(obj['binocular']['rvecs'])
		tvecs = np.array(obj['binocular']['tvecs'])

		return mtx1, dist1, mtx2, dist2, rvecs, tvecs

def write(mtx1, dist1, mtx2, dist2, rvecs, tvecs):
	with open(config_path, encoding = 'utf-8') as config:
		obj = yaml.load(config.read(), Loader = yaml.FullLoader)

		# set binocular config
		obj['binocular']['mtx1'] = mtx1.tolist()
		obj['binocular']['dist1'] = dist1.tolist()
		obj['binocular']['mtx2'] = mtx2.tolist()
		obj['binocular']['dist2'] = dist2.tolist()
		obj['binocular']['rvecs'] = rvecs.tolist()
		obj['binocular']['tvecs'] = tvecs.tolist()
	
		yaml.dump(obj, open(config_path, 'w'))
