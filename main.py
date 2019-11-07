import pyAISm, json
from geopy.distance import great_circle

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
						elementos.append((mensajes[x], mensajes[y], distance))
						print("|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10.2f}|".format(x, mensajes[x]['mmsi'], mensajes[x]['speed'], y, mensajes[y]['mmsi'], mensajes[y]['speed'], distance ))
						print(" {:-<76}".format(''))
			except:
				elementos_problematicos.append((mensajes[x], mensajes[y]))
	return elementos, elementos_problematicos

def decode(filename):
	"""seperate the different AIS message into 2 lists :
	mensajes123 which contains all messages about a ship movement
	mensajes5 which contains all messages about a ship identification
	return (mensajes123,mensajes5)
	"""
	archivo_entrada_abierto = False
	cadena_vacia = ""
	cadena_salt0 = "\n"
	lineas_malas = 0
	mensajes123 = []
	mensajes5 = []

	if not archivo_entrada_abierto:
		try:
			archivo = open(filename, "r")
			archivo_entrada_abierto = True

			linea = archivo.readline()

			while (linea != cadena_vacia):
				linea = linea.rstrip("\n")
				try:
					ais_data=pyAISm.decod_ais(linea)
					ais_data=pyAISm.format_ais(ais_data)
					if str(ais_data['type']) == '1' or str(ais_data['type']) == '2' or str(ais_data['type']) == '3':
						mensajes123.append(ais_data)
					if str(ais_data['type']) == '5':
						mensajes5.append(ais_data)
				except:
					lineas_malas = lineas_malas + 1
					pass
				linea = archivo.readline()
			archivo.close()
		except IOError:
			print('Error en apertura de archivo ', filename)
	print('Le fichier avait ', str(len(mensajes123)), ' messages de type 1, 2, ou 3 , ', str(len(mensajes5)), 'messages de type 5 et ', str(lineas_malas), ' messages undécodables.\n')
	return mensajes123,mensajes5

##############################################################################
#tests
##############################################################################
parametres=get_parameters()
mensajes123, mensajes5 = decode(parametres["GENERAL"][0]["FICHIER"])
elementos, elementos_problematicos = find_transbordements(parametres,mensajes123)
#print(elementos)
#print(mensajes123[5])