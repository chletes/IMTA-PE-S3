"""Run this file to launch the software

The current version works using a terminal and with all OS. 
"""

__version__ = '0.1'
__author__ = ''

# libraries
import os
import platform
import json
import pyAISm
from geopy.distance import great_circle
from decode import decode
from find_possible_transbordements import find_transbordements, find_mmsi_in_message_type_5
from json_functions import lecture_fichier_configuration, get_parameters, ecriture_fichier_sortie
from database_functions import export_types_json, search_mmsi


def first_function():
	"""Choix de l'utilisateur.
		1. 	Retrouve dans la base de données (définie dans ./configuration/config.json) 
			pour mettre à jour la liste TYPE_BATEAUX (définie dans ./configuration/config.json)
		2. 	Montre la configuration actuelle du logiciel. Pour les utilisateurs de Windows, 
			il permet aussi de lancer l'éditeur par defaut pour modifier le fichier ./configuration/config.json
		3. 	Cherche les transbordements entre les différents messages des fichiers du dossier INPUT_PATH 
			(défini dans ./configuration/config.json)
	"""
	choix = 0;
	SO = platform.system()
		
	while 1:
		if SO == "Windows":
			os.system("cls")
		if SO == "Linux":
			os.system("clear")
		print("\nMenu principal")
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
				print ("Choix incorrect ! Appuyez la touche 'Enter' pour revenir au choix...")
				input()
				choix = 0
			else:
				if SO == "Windows":
					os.system("cls")
				if SO == "Linux":
					os.system("clear")
				print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
				print('Choix fait: {0}\n'.format(possibles_choix[choix]))
				if choix == 0:
					break
				if choix == 1:
					#Mise a jour des types de bateaux
					export_types_json(parametres['GENERAL'][0]['DATABASE'])
					print("Succes! Appuyez la touche 'Enter' pour revenir au menu principal...")
					input()

				if choix == 2:
					#Accede au fichier de configuration
					lecture_fichier_configuration(parametres['GENERAL'][0]['TEXT_EDITOR'], './configuration/config.json')
					print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
					
				if choix == 3:
					#Chercher les possibles transbordements
					mensajes123 = [];
					mensajes5 = [];
					input_path = parametres['GENERAL'][0]['INPUT_PATH']
					
					#for filename in glob.glob(os.path.join(path, '*.txt')):# pour lire tous les fichiers qui finisent par .txt
					for filename in os.listdir(input_path):
						real_filename = input_path + '/' + filename
						n_mensajes123, n_mensajes5, n_lineas_malas = decode(real_filename, mensajes123, mensajes5)
					print('Les fichiers avaient {0} messages de type 1, 2, ou 3 , {1} messages de type 5 et {2} messages undécodables.'.format(n_mensajes123, n_mensajes5, n_lineas_malas))
					possibles_transbordements = find_transbordements(parametres, mensajes123)
					print("\nSucces ! {0} possibles transbordements trouvés.".format(len(possibles_transbordements)))
					ecriture_fichier_sortie(parametres['GENERAL'][0]['OUTPUT_FILENAME'], parametres['GENERAL'][0]['OUTPUT_PATH'], possibles_transbordements)
					
					print("Appuyez la touche 'Enter' pour revenir au menu principal...")
					input()
					print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
					
		except ValueError :
			print("Choix incorrect ! Saisisez un numero aussi!")

parametres = {}
parametres = get_parameters()

if parametres != {}:
	first_function()