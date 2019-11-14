from geopy.distance import great_circle

def check_in_all_possible_transbordements(all_possible_transbordements, mmsi_a, mmsi_b):
	for x in all_possible_transbordements:
		if (x[0] == mmsi_a and x[1] == mmsi_b) or (x[1] == mmsi_a and x[0] == mmsi_b):
			return True, all_possible_transbordements.index(x)
	return False, -1


def find_transbordements(parametres, messages):
	"""determine which ships may be doing a transhipment
	return the corresponding list of ships and a list of all failed cases
	"""
	distance_maximale_km = parametres['TRANSBORDEMENTS'][0]['DISTANCE_MAXIMALE_KM']
	vitesse_maximale_noeuds = parametres['TRANSBORDEMENTS'][0]['VITESSE_MAXIMALE_NOEUDS']
	deltaTS_maximale = parametres['TRANSBORDEMENTS'][0]['DELTATS_MAXIMALE']
	types_de_bateaux = []
	diccionaire = parametres['TYPE_BATEAUX']
	for n in diccionaire:
		if diccionaire[n] == 1:
			types_de_bateaux.append(n)

	#print(types_de_bateaux)
	#print("Possibles rendez-vous entre ", len(messages), " bateaux (à distance maximale de ", str(distance_maximale_km),"km et vitesse inferieure à ", str(vitesse_maximale_noeuds), " noeuds).")
	#print(" {:-<76}".format(''))
	#print("|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|".format('Message A', 'Bateau A', 'vitesse A', 'Message B', 'Bateau B', 'vitesse B', 'distance'))
	#print(" {:-<76}".format(''))
	elements = []
	elements_problematiques = []
	all_possible_transbordements = []
	num_messages = len(messages)
	for x in range(0, num_messages):
		possibles_transbordements_avec_LE_message = []
		for y in range(x+1, num_messages):
			valladolid = (messages[x]['lon'], messages[x]['lat'])
			salamanca = (messages[y]['lon'], messages[y]['lat'])
			try:
				if ((messages[x]['mmsi'] != messages[y]['mmsi']) and (messages[y]['mmsi'] not in possibles_transbordements_avec_LE_message)):
					distance = great_circle(valladolid, salamanca).km
					deltaTS = abs(messages[x]['Timestamp']-messages[y]['Timestamp'])/60000
					if ((float(distance) <= float(distance_maximale_km)) and (deltaTS < deltaTS_maximale)):
						if ((float(messages[x]['speed']) <= float(vitesse_maximale_noeuds)) and (float(messages[y]['speed']) <= float(vitesse_maximale_noeuds))):
							elements.append((messages[x], messages[y], distance,deltaTS))
							possibles_transbordements_avec_LE_message.append((messages[y]['mmsi']))
							check, index = check_in_all_possible_transbordements(all_possible_transbordements, messages[x]['mmsi'], messages[y]['mmsi'])
							if check == False:
								all_possible_transbordements.append((messages[x]['mmsi'], messages[y]['mmsi'], [[distance, deltaTS]]))
							else:
								all_possible_transbordements[index][2].append(([distance, deltaTS]))

							#print(possibles_transbordements_avec_LE_message)
							#print("|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10}|{:^10.2f}|".format(x, messages[x]['mmsi'], messages[x]['speed'], y, messages[y]['mmsi'], messages[y]['speed'], distance ))
							#print(" {:-<76}".format(''))
			except:
				#elements_problematiques.append((messages[x], messages[y]))
				pass
	print(len(all_possible_transbordements))
	print(len(all_possible_transbordements[0][2]))
	print(all_possible_transbordements[0])
		#if len(possibles_transbordements_avec_LE_message) != 0:
			#print("possibles transbordement avec le message {0}: {1}.\n".format(x, len(possibles_transbordements_avec_LE_message)))
	print("possibles transbordements total: {0}".format(len(elements)))
	return elements, elements_problematiques

