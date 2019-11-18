"""Run this file to launch the software

The current version works using a terminal. It should work under all OS.
The file necessaire.txt contains all instructions to install specific libraries
that are needed in the software.
"""

__version__ = '0.1'
__author__ = ''

# libraries
import os
import json
from geopy.distance import great_circle
# files needed for the software
###### f5ae2152d9a0f232a543fb38a5e82c2bbe82c5c0
import pyAISm
from decode import decode
from find_possible_transbordements import find_transbordements, find_mmsi_in_message_type_5
from json_lire import lecture_fichier_configuration
from database_functions import export_types_json, search_mmsi

def get_parameters():
	"""read the parameters (where to find json, etc.) and return them """
	archivo_entrada_abierto = False
	config = {}  # will contain the content of config.json deserialized
	if not archivo_entrada_abierto:
		try:
			with open('./configuration/config.json') as json_file:
				try:
					config = json.load(json_file)
				except:
					print("Error en el json")
			archivo_entrada_abierto = True
		except:
			print("Erreur avec l'ouveture du fichier de configuration.")
	return config

def first_function():
	"""Choix de l'utilisateur.
		1. Retrouve dans la base de données "ShipData" tous les types de bateaux
		   Puis demande à l'utilisateur si ses choix  de types sont	faits.
		2. Accede au fichier de configuration pour changer les paramètres de 
		   recherche des transbordements (chemins d'accès, vitesse maximale,
		   distance maximale entre deux bateaux, etc.)
		3. Lance le programme. 
	"""
	choix = 0;
	while 1:
		print("\nBienvenu à notre logiciel!")
		print("")
		possibles_choix = {	0:"Sortir du programme. ",
							1:"Mettre a jour les types de bateaux. ", 
							2:"Acceder au fichier de configuration. ",
							3:"Chercher les possibles transbordements. "}
		for q, a in possibles_choix.items():
			print('{0}. {1}'.format(q, a))
		print("")
		try:
			choix = int(input("Entrez votre décision: "))
			if choix not in [0, 1, 2, 3]:
				print ("Choix incorrect !")
				choix = 0
			else:
				print('Choix fait: {0}'.format(possibles_choix[choix]))
				if choix == 0:
					break
				if choix == 1:
					#Mise a jour des types de bateaux
					export_types_json(parametres['GENERAL'][0]['DATABASE'])

				if choix == 2:
					#Accede au fichier de configuration
					lecture_fichier_configuration(parametres['GENERAL'][0]['TEXT_EDITOR'], './configuration/config.json')
					
				if choix == 3:
					#Chercher les possibles transbordements
					mensajes123 = [];
					mensajes5 = [];
					path = parametres['GENERAL'][0]['PATH']
					#for filename in glob.glob(os.path.join(path, '*.txt')):# pour lire tous les fichiers qui finisent par .txt
					for filename in os.listdir(path):
						real_filename = path + '/' + filename
						n_mensajes123, n_mensajes5, n_lineas_malas = decode(real_filename, mensajes123, mensajes5)
					print('Les fichiers avaient {0} messages de type 1, 2, ou 3 , {1} messages de type 5 et {2} messages undécodables.'.format(n_mensajes123, n_mensajes5, n_lineas_malas))
					possibles_transbordements = find_transbordements(parametres, mensajes123)
					with open('output.json', 'w') as outfile:
						json.dump(possibles_transbordements, outfile)
		except ValueError :
			print("Choix incorrect ! Saisisez un numero aussi!")
	 
##############################################################################
#tests
##############################################################################
parametres = {}
parametres = get_parameters()

if parametres != {}:
	first_function()