# Name: python_getAccidentspotsRequest.py
# Haupt-Funktion: erhaelt die aktuelle Unfallschwerpunkte vom Server

__author__ = "BKonstantin"
__date__ = "$14.12.2015 13:29:04$"

#if __name__ == "__main__":
#    print ("start postRequest...")

# Imports:
# Die Bibliothek "requests" muss vorher installiert werden.
import requests
import json


def printoutInformation(response):
	"""This method prints information in the terminal."""

	# check if the request has been handled successully
	if response.status_code == requests.codes.ok:
		print("RESPONSE:OK")
	else:
		print('WARNING: Request was not handled successfully.')

	# print information about the response header
	print("Content-Type:")
	print(response.headers.get('content-type'))
	print(response.headers)

	# print received response
	print("received RESPONSE:")
	print(response.text)

def getAccidentSpots():
	"""This method sends a request to the server, in order to receive a set of accident spots as a response."""

	# define the header
	# we expect the server to respond with a JSON object
	headers = {'Accept': 'application/json'}

	# send the request to the server
	response = requests.get(
		'http://85.214.69.226:8080/WebServiceBLS/webresources/accidentspots',
		headers=headers
	)

	# gibt einige Information auf der Konsole aus
	# WICHTIG: muss spaeter auskommentiert werden
	printoutInformation(response)

	# speichert das zurueckgelieferte JSON-Objekt ins File accidentspots.json
	data = response.json()
	with open('/home/pi/bikerslifesaver_env/src/accidentspots.json', 'w') as f:
		json.dump(data, f)


# teste die Funktion
# gibt einige Information auf der Konsole aus
# WICHTIG: muss spaeter auskommentiert werden
# print ("start getRequest...")
# getAccidentSpots()
