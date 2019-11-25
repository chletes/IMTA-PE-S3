"""Read the configuration file
"""
__version__ = '0.1'
__author__ = ''

import json, subprocess, datetime

def lecture_fichier_configuration(text_editor, config_file):
	with open(config_file) as json_file:
		config = json.load(json_file)
		print(json.dumps(config, indent=4))
		choix = 0
		while 1:
			possibles_choix = {	0:"Revenir au menu principal. ",
								1:"Ouvrir notepad pour editer le fichier de configuration. "}
			print("")
			for q, a in possibles_choix.items():
				print('{0}. {1}'.format(q, a))
			print("")
			try:
				choix = int(input("Entrez votre décision: "))
				if choix not in [0, 1]:
					print ("Choix incorrect !")
					choix = 0
				else:
					print('Choix fait: {0}'.format(possibles_choix[choix]))
					if choix == 0:
						break
					if choix == 1:
						subprocess.call([text_editor,config_file])
						
			except:
				pass
	return None

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

def ecriture_fichier_sortie(output_filename, output_path, possibles_transbordements):

	if output_filename == "":
		now = datetime.datetime.today()
		output_filename = "{0}{1}_{2}_{3}.json".format(output_path, now.year, now.month, now.day)
	else:
		output_filename = "{0}{1}.json".format(output_path, output_filename)
		
	with open(output_filename, 'w') as outfile:
		json.dump(possibles_transbordements, outfile, indent = 4)