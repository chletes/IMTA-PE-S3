import json, glob, os
from main import get_parameters

parameters = get_parameters()

path = parameters['GENERAL'][0]['PATH']

#for filename in glob.glob(os.path.join(path, '*.txt')):# pour lire tous les fichiers qui finisent par .txt
for filename in os.listdir(path):
	print(filename)
	real_filename = path + '/' + filename
	archivo = open(real_filename, "r")
	linea = archivo.readline()
	print(linea)