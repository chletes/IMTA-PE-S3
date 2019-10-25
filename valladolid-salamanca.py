from geopy.distance import great_circle

valladolid = (41.652133,-4.728562)
salamanca = (40.965157,-5.664018)
print(great_circle(valladolid, salamanca).km)