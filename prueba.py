import pyAISm
from geopy.distance import great_circle

def find_transbordements(distance_maximale_km, mensajes):
	print("Possibles rendez-vous entre ", len(mensajes), " bateaux (à distance maximale de ", str(distance_maximale_km),"km).")
	print(" {:-<54}".format(''))
	print("|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|".format('Message A', 'Bateau A', 'Message B', 'Bateau B', 'distance'))
	print(" {:-<54}".format(''))
	elementos = []
	elementos_problematicos = []
	num_mensajes = len(mensajes)
	for x in range(0, num_mensajes):
		for y in range(x+1, num_mensajes):
			valladolid = (mensajes[x]['lon'], mensajes[x]['lat'])
			salamanca = (mensajes[y]['lon'], mensajes[y]['lat'])
			try:
				distance = great_circle(valladolid, salamanca).km
				if (int(distance) <= int(distance_maximale_km)):
					elementos.append((mensajes[x], mensajes[y], distance))
					
					print("|{:^10d}|{:^10}|{:^10d}|{:^10}|{:^10.2f}|".format(x, mensajes[x]['mmsi'], y, mensajes[y]['mmsi'], distance))
					print(" {:-<54}".format(''))
			except:
				elementos_problematicos.append((mensajes[x], mensajes[y]))
	return elementos, elementos_problematicos

archivo_entrada_abierto = False
cadena_vacia = ""
cadena_salt0 = "\n"
lineas_malas = 0
mensajes = []
if not archivo_entrada_abierto:
	try:
		archivo = open("prueba2.txt", "r")
		archivo_entrada_abierto = True

		linea = archivo.readline()

		while (linea != cadena_vacia):
			linea = linea.rstrip("\n")
			try:
				ais_data=pyAISm.decod_ais(linea)
				ais_data=pyAISm.format_ais(ais_data)
				if str(ais_data['type']) == '1' or str(ais_data['type']) == '2' or str(ais_data['type']) == '3':
					mensajes.append(ais_data)
			except:
				lineas_malas = lineas_malas + 1
				pass
			linea = archivo.readline()
		archivo.close()
	except IOError:
		print('Error en apertura de archivo /archivos/archivo1.txt')
print('Le fichier avait ', str(len(mensajes)), ' messages de type 1, 2 ou 3, et ', str(lineas_malas), ' messages undécodables.\n')
#print(mensajes[0])
elementos, elementos_problematicos = find_transbordements(10,mensajes)
