"""This fill search for the names of ships

To find the corresponding names, only the mmsi is required. The programm will
automatically find the corresponding names in the database if it exists.
Otherwise an error will be printed.
In a future version it might be possible to look for the best matches (i.e.
assuming there was a small mistake in the mmsi name and looking for the best
correspondance)

"""

#from __future__ import barry_as_FLUFL

#__all__ = []
__version__ = 0.1
__author__ = snal

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
	database_of_ships = import_database('specify the path of the database')
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