import requests
import pandas as pd
from module import get_manor_ids
from module import get_manor_info

def place_id():	
	"""
	Retrieves a list of all place IDs in Derbyshire from the OpenDomesday API.
	Returns:
	--------
	list of int:
		A list of all place IDs in Derbyshire.
	"""
	url = "https://opendomesday.org/api/1.0/county/dby"
	response = requests.get(url)	
	if response.status_code == 200:
		data = response.json()
		place_ids = [place["id"] for place in data["places_in_county"]]
		return place_ids
	else:
		print(f"Failed to retrieve data. Error code: {response.status_code}")

def get_all_manor_ids_in_derbyshire(place_ids_list):
	"""
	Retrieves a list of all manor IDs in all places in Derbyshire.
	Parameters:
	-----------
	place_ids_list: list of int
	A list of all place IDs in Derbyshire.
	Returns:
	--------
	list of int:
		A list of all manor IDs in Derbyshire.
	"""
	all_manor_ids = []
	cpt=0
	# Iterate through all place IDs in Derbyshire and call get_manor_ids for each place
	for place_id in place_ids_list:
		manor_ids = get_manor_ids(place_id)
		all_manor_ids.extend(manor_ids)
	return all_manor_ids



if __name__ == '__main__':
	place_ids=place_id()
	print(place_ids)
	manor_ids = get_all_manor_ids_in_derbyshire(place_ids)
	manor_info = get_manor_info(manor_ids)
	df = pd.DataFrame(manor_info)
	print(df)	
	total_geld_paid = df['geld'].sum()
	total_ploughs_owned = df['total_ploughs'].sum()
	print("total_geld_paid = ", total_geld_paid)
	print("total_ploughs_owned = ", total_ploughs_owned )
