import json

def lecture_fichier_configuration():
	with open('./configuration/config.json') as json_file:
	    config = json.load(json_file)
	    print(json.dumps(config, indent=4, sort_keys=True))
	        