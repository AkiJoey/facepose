import os
from configparser import ConfigParser

# get config path
root_path = os.getcwd() + '\\'
config_path = root_path + 'config.ini'

# read config
config = ConfigParser()
config.read(config_path, encoding = 'utf-8')

def read():

	# get binocular config
	mtx1 = config.get('Binocular', 'mtx1')
	dist1 = config.get('Binocular', 'dist1')
	mtx2 = config.get('Binocular', 'mtx2')
	dist2 = config.get('Binocular', 'dist2')
	rvecs = config.get('Binocular', 'rvecs')
	tvecs = config.get('Binocular', 'tvecs')

	return mtx1, dist1, mtx2, dist2, rvecs, tvecs

def write(mtx1, dist1, mtx2, dist2, rvecs, tvecs):

	# set binocular config
	config.set('Binocular', 'mtx1', mtx1)
	config.set('Binocular', 'dist1', dist1)
	config.set('Binocular', 'mtx2', mtx2)
	config.set('Binocular', 'dist2', dist2)
	config.set('Binocular', 'rvecs', rvecs)
	config.set('Binocular', 'tvecs', tvecs)
	
	config.write(open(config_path, 'r+'))
