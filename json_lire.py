import json

def lecture_fichier_configuration():
	with open('./configuration/config.json') as json_file:
	    config = json.load(json_file)
	    #print(config)
	    for p in config:
	    	for q in config[p]:
	    		print("{0}:\n {1}".format(p,q))

	        #print('DISTANCE_MAXIMALE_KM: ' + str(p['DISTANCE_MAXIMALE_KM']))
	        #print('VITESSE_MAXIMALE_NOEUDS: ' + str(p['VITESSE_MAXIMALE_NOEUDS']))
	        