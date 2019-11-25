from geopy.distance import great_circle
from database_functions import find_mmsi_per_type
import time
import os
import json

def check_in_all_possible_transbordements(all_possible_transbordements, mmsi_a, mmsi_b):
	for x in range(0, len(all_possible_transbordements)):
		#print(all_possible_transbordements[x]['MMSI Bateau A'])
		if (all_possible_transbordements[x]['Information bateau A']['MMSI'] == mmsi_a and all_possible_transbordements[x]['Information bateau B']['MMSI'] == mmsi_b) or (all_possible_transbordements[x]['Information bateau A']['MMSI'] == mmsi_b and all_possible_transbordements[x]['Information bateau B']['MMSI'] == mmsi_a):
			return True, x
	return False, -1

def checkMMSI(types_bateaux, mmsi, goodBoats, badBoats):
	"""
		Checks if mmsi exists in the list of mmsi from DB
		goodBoats and badBoats are arrays that contain the mmsi that were already verified or discarded to not enter the bigger loop
		types_bateaux = lists of wanted boat types and mmsi 
	"""
	if (mmsi not in goodBoats):
		if(mmsi not in badBoats):
			for type in types_bateaux:
				for ind in type:
					if(mmsi == ind):
						goodBoats[type] = mmsi
						return type, True
			badBoats.append(mmsi)
			return -1, False
		return -1, False
	return goodBoats.index(mmsi), True

def find_transbordements(parametres, messages):
	"""determine which ships may be doing a transhipment
	return the corresponding list of ships and a list of all failed cases
	"""
	distance_maximale_km = parametres['TRANSBORDEMENTS'][0]['DISTANCE_MAXIMALE_KM']
	vitesse_maximale_noeuds = parametres['TRANSBORDEMENTS'][0]['VITESSE_MAXIMALE_NOEUDS']
	deltaTS_maximale = parametres['TRANSBORDEMENTS'][0]['DELTA_TIMESTAMP_ENTRE_MESSAGES_MAXIMALE']
	types_de_bateaux = []
	diccionaire = parametres['TYPE_BATEAUX']
	for n in diccionaire:
		if diccionaire[n] == 1:
			types_de_bateaux.append(n)

	print('Searching MMSI per TYPE...')

	t0 = time.time()
	bateaux = find_mmsi_per_type(types_de_bateaux,parametres['GENERAL'][0]['DATABASE'])
	t1 = time.time()
	print('Finished in {0:.2f} seconds.'.format(t1-t0))
	#print(types_de_bateaux)
	#print("Possibles rendez-vous entre ", len(messages), " bateaux (à distance maximale de ", str(distance_maximale_km),"km et vitesse inferieure à ", str(vitesse_maximale_noeuds), " noeuds).")
	#print(" {:-<76}".format(''))
	#print("|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|".format('Message A', 'Bateau A', 'vitesse A', 'Message B', 'Bateau B', 'vitesse B', 'distance'))
	#print(" {:-<76}".format(''))
	#elements = []
	#elements_problematiques = []
	all_possible_transbordements = {}
	num_messages = len(messages)
	#tot = 1
	#for i in range(0,num_messages):
		#tot += i
	print('Checking possible transbordements...')
	#sumaParcial = 0
	dic_index = 0
	#pge = 0
	#t0 = time.time()
	for x in range(0, num_messages):
		possibles_transbordements_avec_LE_message = []
		#pourcentage = int(100*(1-(tot - sumaParcial)/tot))
		#if (pourcentage != pge):
			#pge += 1
			#os.system('cls')	## clears the terminal
			#print("\n")																										#		Loading
			#print("Loading")																								#		Screen
			#print('[' + ("|" * int(pourcentage)) + (" " * int(100 - pourcentage)) + "] " + str(pourcentage) + " %")
		for y in range(x+1, num_messages):
			valladolid = (messages[x]['lon'], messages[x]['lat'])
			salamanca = (messages[y]['lon'], messages[y]['lat'])
			try:
				if ((messages[x]['mmsi'] != messages[y]['mmsi']) and (messages[y]['mmsi'] not in possibles_transbordements_avec_LE_message)):
					distance = great_circle(valladolid, salamanca).km
					deltaTS = abs(messages[x]['Timestamp']-messages[y]['Timestamp'])/60000
					if ((float(distance) <= float(distance_maximale_km)) and (deltaTS < deltaTS_maximale)):
						if ((float(messages[x]['speed']) <= float(vitesse_maximale_noeuds)) and (float(messages[y]['speed']) <= float(vitesse_maximale_noeuds))):
							#elements.append((messages[x], messages[y], distance,deltaTS))
								possibles_transbordements_avec_LE_message.append((messages[y]['mmsi']))
								check, index = check_in_all_possible_transbordements(all_possible_transbordements, messages[x]['mmsi'], messages[y]['mmsi'])
								#print(check)
								if check == False:
									info_A = {"MMSI": messages[x]['mmsi']}
									info_B = {"MMSI": messages[y]['mmsi']}
									all_possible_transbordements[len(all_possible_transbordements)] = {"Information bateau A": info_A, "Information bateau B": info_B, "Rencontres":{0:{"Distance entre bateaux":distance, "Timestamp 1e message":messages[x]['Timestamp'], "Timestamp 2e message": messages[y]['Timestamp'], "Temps entre messages:":deltaTS}}}
								else:
									lene = len(all_possible_transbordements[index]['Rencontres'])
									all_possible_transbordements[index]['Rencontres'][lene] = {"Distance entre les bateaux":distance,"Timestamp 1e message":messages[x]['Timestamp'], "Timestamp 2e message": messages[y]['Timestamp'], "Temps entre messages":deltaTS}
								#print(json.dumps(all_possible_transbordements, indent=4))
								#input()
							#print(possibles_transbordements_avec_LE_message)
							#print("|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10.2f}|".format(x, messages[x]['mmsi'], messages[x]['speed'], y, messages[y]['mmsi'], messages[y]['speed'], distance ))
							#print(" {:-<76}".format(''))
			except:
				#elements_problematiques.append((messages[x], messages[y]))
				pass
		#sumaParcial += num_messages - (x + 1)
	t1 = time.time()
	print('Finished in {0:.2f} seconds.'.format(t1-t0))
	#goodBoats = {}
	#badBoats = []
	#for trans in all_possible_transbordements:
		#typex, blx = checkMMSI(bateaux,trans[0],goodBoats,badBoats)
		#typey, bly = checkMMSI(bateaux,trans[1],goodBoats,badBoats)
		#if blx and bly:
			#trans.append((typex,typey))									#if not, that pair of boats are removed from the array
		#else:
			#all_possible_transbordements.pop(all_possible_transbordements.index(trans))
	#print(goodBoats)

	return all_possible_transbordements

def find_mmsi_in_message_type_5(transbordement_couple, messages_type5):
	for x in messages_type5:
		if x['mmsi'] == transbordement_couple[0][0]:
			transbordement_couple[0][0].append(x['shiptype'])
		if x['mmsi'] == transbordement_couple[1][0]:
			transbordement_couple[1][0].append(x['shiptype'])
