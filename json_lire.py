"""Read the configuration file
"""
__version__ = '0.1'
__author__ = ''

import json, subprocess

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