# Name: python_postRequest.py
# Haupt-Funktion: sendet die aktuelle Position mit dem Zeitstempel an den Server

__author__ = "BKonstantin"
__date__ = "$14.12.2015 13:29:04$"

#if __name__ == "__main__":
#    print ("start postRequest...")

# Imports:
# Die Bibliothek "requests" muss vorher installiert werden.
import requests
import json

# gibt einige Information auf der Konsole aus
def printoutInformation(response, myCoordinates):
	# gibt die Information aus
	print("created JSON:")
	print(json.dumps(myCoordinates))
	# prueft, ob die Anfrage erfolgreich abgeschlossen wurde
	if response.status_code == requests.codes.ok:
		print("RESPONSE:OK")

	if response.status_code == 204:
		print("Status Code = 204(Position has been saved.The response is without a message-body)")
	elif response.status_code == 201:
		print("Status Code = 201(Position has been saved.The request has been fulfilled)")


# Die Methode "postCoordinates" sendet aktuelle Position mit dem Zeitstempel an den Server
#	latitude  - aktuelle Breite
#	longitude - aktuelle Laenge
#	timeStamp - Zeitstempel
def postCoordinates(latitude, longitude, timeStamp):
	# erzeuge JSON-Inhalt: GeoCoordinaten und TimeStamp
	myCoordinates = {'latitude': latitude,'longitude':longitude,'timeStamp':timeStamp}
	# definiere Header: zum Server wird ein JSON-Objekt gesendet
	headers = {'content-type': 'application/json'}
	# sende eine Anfragen an den Server, um die aktuelle Position in die DB zu speichern.
	# json.dumps() erzeugt aus dem Woerterbuch (myCoordinates) ein JSON-Objekt
	response = requests.post('http://85.214.69.226:8080/WebServiceBLS/webresources/receivedcoordinates',
	data=json.dumps(myCoordinates), headers=headers)
	# gibt einige Information auf der Konsole aus
	# WICHTIG: muss spaeter auskommentiert werden
	printoutInformation(response, myCoordinates)


# teste die Funktion
# WICHTIG: Test-Funktion muss geloescht werden!!!
print ("start postRequest...")
postCoordinates('58.33444','19.72878','2015-12-15T11:31:41')

#if response.status_code != 201:
#    raise APIError('POST /tasks/ {}'.format(response.status_code))

#assert response.status_code == 201
