import json, os
from geopy.distance import great_circle
import pyAISm
from decode import decode
from find_possible_transbordements import find_transbordements
from json_lire import lecture_fichier_configuration

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

def first_function():
	"""Choix de l'utilisateur.
		1. On retrouve de la base de données "ShipData" tous les types de bateux. Puis on demande à l'utilisateur si ses choix sont
			faits.
		2. On accede au fichier de configuration pour changer les parametres de recherche des transbordements (path, vitesse maximale, 
			distance entre deux bateaux maximale, etc.)
		3. On lance le programme. 
	"""
	print("Bienvenu à notre logiciel!")
	print("")
	possibles_choix = {	1:"Mettre a jour les types de bateaux. ", 
						2:"Acceder au fichier de configuration. ",
						3:"Chercher les possibles transbordements. "}
	for q, a in possibles_choix.items():
		print('{0}. {1}'.format(q, a))
	print("")
	choix = 0;
	while choix == 0:
		try:
			choix = int(input("Entrez votre décision: "))
			if choix not in [1, 2, 3]:
				print ("Choix incorrect !")
				choix = 0
			else:
				print('Choix fait: {0}'.format(possibles_choix[choix]))
		except ValueError :
			print("Choix incorrect ! Saisisez un numero aussi!")
	return choix
##############################################################################
#tests
##############################################################################
parametres=get_parameters()

choix = first_function()
if choix == 1:
	#Mise a jour des types de bateaux
	print("choix 1")
if choix == 2:
	#Accede au fichier de configuration
	lecture_fichier_configuration()
	#print("choix 2")
if choix == 3:
	#Chercher les possibles transbordements
	mensajes123 = [];
	mensajes5 = [];
	path = parametres['GENERAL'][0]['PATH']
	#for filename in glob.glob(os.path.join(path, '*.txt')):# pour lire tous les fichiers qui finisent par .txt
	for filename in os.listdir(path):
		#print(filename)
		real_filename = path + '/' + filename
		n_mensajes123, n_mensajes5, n_lineas_malas = decode(real_filename, mensajes123, mensajes5)
	print('Les fichiers avaient {0} messages de type 1, 2, ou 3 , {1} messages de type 5 et {2} messages undécodables.'.format(n_mensajes123, n_mensajes5, n_lineas_malas))
	
