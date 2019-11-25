"""This fill contains all functions related to the database

The most important one for the software is export_types_json() :
this function allowed to update the existing types of ships in config.json
and thus allowed the software to work properly (given that the user has
selected the types he wanted for the search)
2 libraries are used :
- xlrd, to read the database which is a .xlsx file (Excel),
- json, for all treatments of config.json.
See the respective documentations if necessary.

There are 3 different functions looking for the type of the ships
Use export_type_json if you want to update types in the config.json file
Use search_mmsi(message) if you want to add the type of the ship to message
Use mmsi_in_database(mmsi) if you want to get the type of a ship given its mmsi

The last functon looks for the names of ships, given a list of mmsi (usefull if
used in conjonction with type 5 AIS message to verify if the name is correct)

The following assumptions are made for the database
it's a .xlsx file with one sheet
the first colonn contains the mmsi
the third one, the names
the fifth one, the types
If it's modified in the database, modifify the global variables in accordance
with those changes.

"""

__version__ = 0.2
__author__ = 'snal'

import xlrd
import json
import time
all_searched_mmsi = {}  # reduce memory programm complexity for search_mmsi()
						# by stocking all already searched mmsi :
						# key : mmsi, value : type of the ship
index_col_mmsi = 1
index_col_name = 2
index_col_type = 4

#def export_types_json(path_of_the_database='../ship_db_t.xlsx'):
def export_types_json(path_of_the_database):
	"""export the types from the database into config.json"""
	types_u = set([t for t in xlrd.open_workbook(path_of_the_database
							).sheet_by_index(0).col_values(index_col_type)])
	json_file = open('./configuration/config.json','r')
	config = json.load(json_file)
	for t in types_u:
		if t in config['TYPE_BATEAUX'].keys():
			continue
		else:
			config['TYPE_BATEAUX'][t]=0
	json_file.close()
	with open('./configuration/config.json', 'w') as outfile:
		#print(config['TYPE_BATEAUX'])
		json.dump(config, outfile, indent = 4)
	return None

def update_info_list_config(path_of_the_database):
	column_name = []
	excel = xlrd.open_workbook(path_of_the_database).sheet_by_index(0)
	json_file = open('./configuration/config.json','r')
	config = json.load(json_file)
	for i in range(excel.ncols):
		column_name.append(excel.col_values(i)[0])
	for t in column_name:
		if t in config['WANTED_INFO'].keys():
			continue
		else:
			config['WANTED_INFO'][t]=0
	json_file.close()
	with open('./configuration/config.json', 'w') as outfile:
		json.dump(config, outfile)
	return None


def search_mmsi(message, path_of_the_database):
	"""add the type of the ship to the message if the mmsi is in the database
	return true if operation is successful, false otherwise
	"""
	# the global dictionnary all_searched_mmsi is used here
	#first we checked whether we've already searched for the current mmsi
	if (message['mmsi'] in all_searched_mmsi.keys()):
		message['type']=all_searched_mmsi[message['mmsi']]
		return True
	else:  # otherwise it's the first encounter with this mmsi
		# extract information from the database
		database_mmsi = [t for t in xlrd.open_workbook(path_of_the_database
								).sheet_by_index(0).col_values(index_col_mmsi)]
		database_type = [t for t in xlrd.open_workbook(path_of_the_database
								).sheet_by_index(0).col_values(index_col_type)]
		# search for the mmsi in the database
		try:
			type_of_the_ship = database_type[database_mmsi.index(mmsi)]
			all_searched_mmsi[message['mmsi']]=type_of_the_ship
			message['type']=type_of_the_ship
			return True
		except:  # if a ValueError exception is raised (i.e. no mmsi found)
			message['type']="None"
			return False


def mmsi_in_database(mmsi):
	"""look for the mmsi in the database and return the type of the ship
	If the search was unsuccessful, return False
	"""
	book = xlrd.open_workbook('../ShipData.xlsx')
	db = book.sheet_by_index(0)
	list_of_all_mmsi = db.col(index_col_mmsi)
	try:
		i = list_of_all_mmsi.index(mmsi)  # an exception may rise : ValueError
		shiptype = db.col(index_col_type)
		return shiptype[i]
	except:
		return False

def find_name_of_ships(list_of_mmsi, path_of_the_database):
	"""find the name of all corresponding ships by using there mmsi
	return a dictionnary with the mmsi as key and the name
	A list is also returned which contained all mmsi which aren't registred in
	the database.
	"""
	# only mmsi and names of ships are usefull here
	database_mmsi = [t for t in xlrd.open_workbook(path_of_the_database
							).sheet_by_index(0).col_values(index_col_mmsi)]
	database_name = [t for t in xlrd.open_workbook(path_of_the_database
							).sheet_by_index(0).col_values(index_col_name)]
	# creating the dictionnary and the list returned
	names_of_the_ships = {}
	unknown_ships_mmsi = []
	# looking for the names of the ships
	for mmsi in list_of_mmsi:
		try:
			names_of_the_ships[mmsi] = database_name[database_mmsi.index(
																		mmsi)]
			# index() raises a ValueError exception when no element correspon
			# -ding to mmsi is found
		except:
			unknown_ships_mmsi.append(mmsi)
	return names_of_the_ships,unknown_ships_mmsi

def find_mmsi_per_type(list_of_types,path_of_the_database):
		#extract information from the database
		database_mmsi = [t for t in xlrd.open_workbook(path_of_the_database
								).sheet_by_index(0).col_values(index_col_mmsi)]
		database_type = [t for t in xlrd.open_workbook(path_of_the_database
	 							).sheet_by_index(0).col_values(index_col_type)]
		# database_mmsi = xlrd.open_workbook(path_of_the_database
		# 						).sheet_by_index(0).col_values(index_col_mmsi)
		# database_type = xlrd.open_workbook(path_of_the_database
		# 						).sheet_by_index(0).col_values(index_col_type)
		mmsi = {}
		for type_ in list_of_types:
			mmsi[type_] = []
			for i in range(0,len(database_type)):
				if database_type[i] == type_:
					if database_mmsi[i] != '':
						mmsi[type_].append(database_mmsi[i])
					else:
						mmsi[type_].append('No MMSI')
		return mmsi
