import json

#config = {}
#config['TRANSBORDEMENTS'] = []
#config['TRANSBORDEMENTS'].append({
#    'DISTANCE_MAXIMALE_KM': 10,
#    'VITESSE_MAXIMALE_NOEUDS': 10,
#})
#config['TYPE_BATEAUX'] = {}
#config['TYPE_BATEAUX']['Tug']=0


with open('output.json', 'w') as outfile:
    json.dump(config, outfile)
