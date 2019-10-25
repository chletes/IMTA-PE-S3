import json

with open('config.json') as json_file:
    config = json.load(json_file)
    for p in config['TRANSBORDEMENTS']:
        print('DISTANCE_MAXIMALE_KM: ' + str(p['DISTANCE_MAXIMALE_KM']))
        print('VITESSE_MAXIMALE_NOEUDS: ' + str(p['VITESSE_MAXIMALE_NOEUDS']))