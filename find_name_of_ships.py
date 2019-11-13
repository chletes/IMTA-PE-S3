"""This fill search for the names of ships

To find the corresponding names, only the mmsi is required. The programm will
automatically find the corresponding names in the database if it exists.
Otherwise an error will be printed.
In a future version it might be possible to look for the best matches (i.e.
assuming there was a small mistake in the mmsi name and looking for the best
correspondance)
The code here is separated from main.py for a better management of the programm


Betterments possible :
 create a fonction which will be the interface with the database ?
"""

#from __future__ import barry_as_FLUFL

#__all__ = []
__version__ = 0.1
__author__ = 'snal'

import xlrd

def import_database(path_of_the_database):
	"""open the database and convert it to a dictionnary
	return the dictionnary
	"""
	workbook = xlrd.open_workbook(path_of_the_database)
	workbook = xlrd.open_workbook(path_of_the_database, on_demand = True)
	worksheet = workbook.sheet_by_index(0)
	first_row = [] # The row where we stock the name of the column
	for col in range(worksheet.ncols):
	    first_row.append( worksheet.cell_value(0,col) )
	# tronsform the workbook to a list of dictionnary
	data =[]
	for row in range(1, worksheet.nrows):
	    elm = {}
	    for col in range(worksheet.ncols):
	        elm[first_row[col]]=worksheet.cell_value(row,col)
	    data.append(elm)
	return data

def find_name_of_ships(list_of_mmsi):
	"""find the name of all corresponding ships by using there mmsi
	return a dictionnary with the mmsi as key and the name
	A list is also returned which contained all mmsi which aren't registred in
	the database.
	"""
	database_of_ships = import_database('../ShipData.xlsx')
	# creating the dictionnary and the list returned
	names_of_the_ships = {}
	unknown_ships_mmsi = []
	# looking for the names of the ships
	for mmsi in list_of_mmsi:
		try:
			names_of_the_ships[mmsi] = database_of_ships[mmsi]  # should not work yet
		except:
			unknown_ships_mmsi.append(mmsi)  # stocking unknown mmsi
	return names_of_the_ships,unknown_ships_mmsi


def search_mmsi(message):
	"""add the type of the ship to the message if the mmse is in the database
	return true if operation is successful, false otherwise
	"""
	print('beginning of the search')
	database_of_ships = import_database('../ShipData.xlsx')
	print('database ok')
	all_searched_mmsi = {}  # reduce memory programm complexity
	if (message['mmsi'] in all_searched_mmsi.keys()):
		print('known mmsi')
		# case where we've already searched for this mmsi
		message['type']=all_searched_mmsi[message['mmsi']]
		return True
	else:
		print('unknown mmsi')
		# 2nd case : first time encounter with this mmsi
		try:
			# searching in the database
			type_of_the_ship = database_of_ships[message['mmsi']]
			print('search : success')
			all_searched_mmsi[message['mmsi']]=type_of_the_ship
			message['type']=type_of_the_ship
			return True
		except:  # the search was a failure
			print('search : failure')
			return False


##test
print('bchsk')
ma={'type': 1, 'repeat': 0, 'mmsi': 211506970, 'status': 'Under way using engine',
 'turn': 'N/A', 'speed': '0.0', 'accuracy': '1', 'lon': 0.12568666666666667, 
 'lat': 49.48391, 'course': '102.7°', 'heading': 'N/A', 'second': 19,
  'maneuver': 1, 'raim': '1', 'radio': 49228}
search_mmsi(ma)
print('fdgxhcg')