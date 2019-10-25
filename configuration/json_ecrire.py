import json

config = {}
config['TRANSBORDEMENTS'] = []
config['TRANSBORDEMENTS'].append({
    'DISTANCE_MAXIMALE_KM': 10,
    'VITESSE_MAXIMALE_NOEUDS': 10,
})
config['BATEAUX'] = []
config['BATEAUX'].append({
	'TYPE':'peche'
	})


with open('config.json', 'w') as outfile:
    json.dump(config, outfile)