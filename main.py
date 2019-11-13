import json, os
from geopy.distance import great_circle
import pyAISm
from decode import decode

def get_parameters():
	"""read the parameters (where to find json, etc.) and return them """
	archivo_entrada_abierto = False
	if not archivo_entrada_abierto:
		try:
			with open('./configuration/config.json') as json_file:
				try:
					config = json.load(json_file)
				except:
					print("Error en el json")
			archivo_entrada_abierto = True
		except:
			print("Error en el fichero de configuracion")
	return config

def find_transbordements(parametres, mensajes):
	"""determine which ships may be doing a transhipment
	return the corresponding list of ships and a list of all failed cases
	"""
	distance_maximale_km = parametres['TRANSBORDEMENTS'][0]['DISTANCE_MAXIMALE_KM']
	vitesse_maximale_noeuds = parametres['TRANSBORDEMENTS'][0]['VITESSE_MAXIMALE_NOEUDS']
	deltaTS_maximale = parametres['TRANSBORDEMENTS'][0]['DELTATS_MAXIMALE']
	types_de_bateaux = parametres['BATEAUX'][0]['TYPE']
	#print(types_de_bateaux)
	print("Possibles rendez-vous entre ", len(mensajes), " bateaux (à distance maximale de ", str(distance_maximale_km),"km et vitesse inferieure à ", str(vitesse_maximale_noeuds), " noeuds).")
	print(" {:-<76}".format(''))
	print("|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|".format('Message A', 'Bateau A', 'vitesse A', 'Message B', 'Bateau B', 'vitesse B', 'distance'))
	print(" {:-<76}".format(''))
	elementos = []
	elementos_problematicos = []
	num_mensajes = len(mensajes)
	for x in range(0, num_mensajes):
		for y in range(x+1, num_mensajes):
			valladolid = (mensajes[x]['lon'], mensajes[x]['lat'])
			salamanca = (mensajes[y]['lon'], mensajes[y]['lat'])
			try:
				distance = great_circle(valladolid, salamanca).km
				if (float(distance) <= float(distance_maximale_km)):
					if ((float(mensajes[x]['speed']) <= float(vitesse_maximale_noeuds)) and (float(mensajes[y]['speed']) <= float(vitesse_maximale_noeuds))):
						deltaTS = abs(mensajes[x]['Timestamp']-mensajes[y]['Timestamp'])/60000
						if (deltaTS <= deltaTS_maximale):
							elementos.append((mensajes[x], mensajes[y], distance,deltaTS))
							print("|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10.2f}|".format(x, mensajes[x]['mmsi'], mensajes[x]['speed'], y, mensajes[y]['mmsi'], mensajes[y]['speed'], distance ))
							print(" {:-<76}".format(''))
			except:
				elementos_problematicos.append((mensajes[x], mensajes[y]))
	return elementos, elementos_problematicos


##############################################################################
#tests
##############################################################################
parametres=get_parameters()
mensajes123 = [];
mensajes5 = [];
path = parametres['GENERAL'][0]['PATH']
#for filename in glob.glob(os.path.join(path, '*.txt')):# pour lire tous les fichiers qui finisent par .txt
for filename in os.listdir(path):
	print(filename)
	real_filename = path + '/' + filename
	decode(real_filename, mensajes123, mensajes5)

#elementos, elementos_problematicos = find_transbordements(parametres,mensajes123)
#print(elementos)
#print(mensajes123[5])
