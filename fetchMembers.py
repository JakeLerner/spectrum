import requests
import json


def fetch_current_house():
	url = "https://www.govtrack.us/api/v2/role?current=true&role_type=representative&limit=500"
	people = [role["person"] for role in requests.get(url).json()['objects']]
	return people

def fetch_current_senate():
	url = "https://www.govtrack.us/api/v2/role?current=true&role_type=senator&limit=500"
	people = [role["person"] for role in requests.get(url).json()['objects']]
	return people

def print_senate_id_list():
	ids = [person['id'] for person in fetch_current_senate()]
	print ids

def print_house_id_list():
	ids = [person['id'] for person in fetch_current_house()]
	print ids

print_house_id_list()