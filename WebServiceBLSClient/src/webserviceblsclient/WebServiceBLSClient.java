package webserviceblsclient;

import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * Die Klasse "BLSWebServiceClient" enthaelt die Methoden
 * fuer das Speichern der Unfalldaten(Geo-Koor. & TimeStamp) 
 * in die Tabelle  "received_coordinates"
 * @author BKonstantin
 */
public class WebServiceBLSClient {

    /**
     * Die Methode gibt einen String-Wert im Format 
     * (Bsp. 2015-11-29T23:32:22) fuer MySQL-TimeStamp zurueck
     * 
     * @return currentTimeStamp - Zeit, wenn der Unfall passiert wurde und
     * wenn die Geo-Koordinaten empfangen wurden.
     */
    private String getCurrentTimeStamp(){
        Date date = new Date();   
        DateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd"); // Datum
        DateFormat timeFormat = new SimpleDateFormat("HH:mm:ss");   // Zeit     
        String currentTimeStamp = dateFormat.format(date) + "T" + timeFormat.format(date); // Bsp. Format fuer MySQL: 2015-11-29T23:32:22
        
        return currentTimeStamp;
    }
    
    /**
     * Die Methode schickt ein JSON an DB als POST-Anfrage, damit die Geo-Koordinaten und die Zeit
     * des Unfalls in die Tabelle "received_coordinates" gespeichert werden.
     * 
     * @param latitude  - Latitude, wo der Unfall war
     * @param longitude - Longitude, wo der Unfall war
     */
    public void postGeoCoordinates(Double latitude, Double longitude){
        RestfulClient client =new RestfulClient();
        String jsonString= "{\"latitude\":"+latitude+",\"longitude\":"+longitude+",\"timeStamp\":\""+getCurrentTimeStamp()+"\"}";
        client.create_JSON(jsonString);
        client.close();
    }
    
    /**
     * Main-Methode, um zu testen!
     * @param args 
     */
    public static void main(String[] args) {        
        WebServiceBLSClient webServiceClient = new WebServiceBLSClient();
        webServiceClient.postGeoCoordinates(58.33555,19.72057);
    }
    
}
