package accidentspotsfinder;

import java.sql.*;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author BKonstantin
 */
public class DB_Manager {

    private final static float RADIUS_OF_POINT = 30;
    // erzeuge einige globale Variablen
    private Connection conn = null;       // Verbindung zur Datenbank
    private Statement stmt = null;        // ist fuer "SELECT * FROM received_coordinates";"
    private Statement stmtGlobal = null;  // ist fuer "SELECT NodeId, GROUP_CONCAT(Neighbor SEPARATOR ';') ..."
    private Statement stmtGlobal2 = null; // ist fuer "INSERT INTO accident_spots ..."
    private Statement stmtGlobal3 = null; // ist fuer "SELECT Latitude, Longitude FROM received_coordinates ..."
    private String sql = null;            // String fuer SQL-Anfragen
    java.util.Date date = new java.util.Date();

    /**
     * erzeugt die Verbindung zur Datenbank
     *
     * @param dbConnector - das Objekt der Klasse 'DB_Manager', um die
     * Verbindung zu erstellen
     */
    private void createConnectionToDB(DB_Connector dbConnector) {

        try {
            // erstellt die Verbindung zu DB
            conn = dbConnector.createConnectionToDB();
            System.out.println("Creating statement...");
            // erzeugt globale die Statements, um spaeter die Anfragen
            // an DB zu schicken z.B. mit der Methode .executeQuery(sql);
            stmt = conn.createStatement();
            stmtGlobal = conn.createStatement();
            stmtGlobal2 = conn.createStatement();
            stmtGlobal3 = conn.createStatement();

        } catch (SQLException ex) {
            Logger.getLogger(DB_Manager.class.getName()).log(Level.SEVERE, null, ex);
        }

    }

    /**
     *      *** TEST: nur fuer das Testen; fuer das Endergebnis ist nicht relevant
     * ***
     *
     * gibt die Information (NodeId,Latitude,Longitude) auf die Konsole aus
     */
    public void giveInformation() {
        try {
            // SQL-Anfrage an DB
            sql = "SELECT * FROM received_coordinates";
            ResultSet rs = stmt.executeQuery(sql);

            // die Daten aus Ergebnismenge extrahieren
            while (rs.next()) {
                // nimmt die Daten aus der entsprechenden Spalte
                int nodeId = rs.getInt("NodeId");
                double latitude = rs.getDouble("Latitude");
                double longitude = rs.getDouble("Longitude");

                // die Ergebnisse ausgeben
                System.out.print("NodeId: " + nodeId + " | ");
                System.out.print("Latitude: " + latitude + " | ");
                System.out.print("Longitude: " + longitude + " | \n");
            }
        } catch (SQLException ex) {
            Logger.getLogger(DB_Manager.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    /**
     * Loescht die ganze Information aus der entsprechenden Tabelle
     *
     * @param tableName - Name der Tabelle
     */
    public void truncateTable(String tableName) {
        try {
            sql = "truncate " + tableName;
            ResultSet rs = stmt.executeQuery(sql);

        } catch (SQLException ex) {
            Logger.getLogger(DB_Manager.class.getName()).log(Level.SEVERE, null, ex);
        }

    }

    /**
     * Haupt Aufgabe dieser Methode: Die Relationstabelle (NodeId-Nachbar) in DB
     * auszufuellen. Die Punkten, die schon veraltet sind, werden dabei
     * gefiltert.
     */
    public void countNeighbors() {

        try {
            // SQL-Anfrage an DB: 
            // nimmt alle Eintraege aus der Tabelle
            sql = "SELECT * FROM received_coordinates";
            ResultSet queryResult = stmt.executeQuery(sql);
            // zaehlt alle Eintraege in der Tabelle
            sql = "SELECT COUNT(*) AS total FROM received_coordinates";
            Statement stmt2 = conn.createStatement();
            ResultSet queryResultCopy = stmt2.executeQuery(sql);
            // Position des Kursors wird vor dem ersten Element gesetzt,
            // um die die gelieferte Zahl aller Objekte rauszunehmen und zu speichern
            queryResultCopy.absolute(1);
            int numberOfNodes = queryResultCopy.getInt("total"); // speichere die Anzahl der Eintraege (Geo-Points)
            // Da in der while-Schleife die Daten aus der Tabelle parallel bearbeitet werden muessen,
            // wird hier wieder die Anfrage an DB geschickt
            sql = "SELECT * FROM received_coordinates";
            queryResultCopy = stmt2.executeQuery(sql);

            Statement stmt3 = conn.createStatement();
            int count = 0; // *just for test

            // weiter werden alle empfangene Geokoordinaten betrachtet
            while (queryResult.next()) {
                System.out.println("Step N " + ++count); // *just for test
                // speichere die Eigenschaften eines Knoten(Geo-Point) aus dem Anfrage-Ergebnis
                // in die Variablen
                int nodeId = queryResult.getInt("NodeId");
                double latitude = queryResult.getDouble("Latitude");
                double longitude = queryResult.getDouble("Longitude");

                // ueberpruefe, ob der Geo-Point noch nicht veraltet ist.
                if (isTimeStampOfCoordNotOld(queryResult)) { //  der Geo-Point ist noch aktuell...
                    int counter = 1; // zaehlt, wieviel Geo-Points schon betrachtet wurde
                    // gibt es weitere Geo-Points?
                    while (counter <= numberOfNodes) { // ja, es gibt weitere Geo-Points 
                        // Position des Kursors wird vor dem jeweiligen Geo-Point gesetzt,
                        // um die Eigenschaften dieses Points zu bekommen. (z.B.NodeId usw. )
                        queryResultCopy.absolute(counter);
                        int tempNodeId = queryResultCopy.getInt("NodeId"); // nimm ID disese Points
                        // es macht keinen Sinn, die Distanz zu sich selbst zu berechnen.
                        // d.h. berechne die Distanze nur zu den anderen Geo-Points
                        if (nodeId != tempNodeId) {
                            // Ist der Geo-Point, zu dem die Distanz berechnet werden soll, noch aktuell?
                            if (isTimeStampOfCoordNotOld(queryResultCopy)) {// ja, Geo-Point ist noch aktuell
                                //speichere die Eigenschaften dieses Points in Variablen
                                double tempLatitude = queryResultCopy.getDouble("Latitude");
                                double tempLongitude = queryResultCopy.getDouble("Longitude");
                                // berechne die Distanz
                                // latitude, longitude - Eigenschaften des "Haupt-" Geo-Points. Das ist
                                // der Geo-Point, der am Anfang der while-Schleife bekommen wurde. Sprich  "nodeId".
                                // tempLatitude, tempLongitude - die Eigenschaften des temporaeren Geo-Points, der gerade in dieser 
                                // zweiten while-Schleife betrachtet ist.
                                double distance = calculateDistanceBetweenPoints(latitude, longitude, tempLatitude, tempLongitude);
                                // wenn die Distanz gleich/kleiner als angegebene Grenze (30 Meter) ist, dann speichere diesen "temporaeren"
                                // Geo-Points als Nachbar-Point in die Relationstabelle.
                                if (distance <= RADIUS_OF_POINT) {
                                    sql = "INSERT INTO node_neighbor_relation VALUES ('" + nodeId + "','" + tempNodeId + "')";
                                    stmt3.executeUpdate(sql);

                                    // <nur fuer Testen>
                                    System.out.print("NodeId: " + tempNodeId + " | ");
                                    System.out.print("Latitude: " + tempLatitude + " | ");
                                    System.out.print("Longitude: " + tempLongitude + " | \n");
                                    System.out.println("Distance from " + nodeId + " to " + tempNodeId + " = " + distance);
                                    // </nur fuer Testen>

                                }

                            }
                        }
                        ++counter;
                    }
                }

            }

            // aktualisiere die Unfallschwerpunktstabelle 
            updateAccidentSpotsTable();

            // schliesse alle Anfragen und Statements
            queryResult.close();
            queryResultCopy.close();
            stmt2.close();
            stmt3.close();

        } catch (SQLException ex) {
            Logger.getLogger(DB_Manager.class.getName()).log(Level.SEVERE, null, ex);
        }

    }

    /**
     * Die Methode aktualisiert die Unfallschwerpunktstabelle
     */
    public void updateAccidentSpotsTable() {
        try {
            // SQL-Anfrage an DB:
            // nimm alle Geo-Points aus der Relationstabelle. Zu jedem Geo-Point 
            // wird eine Gruppe von Nachbarn verkettet und in der absteigenden Reihenfolge
            // sortiert. D.h. Der Geo-Point, der die hoechste Anzahl von Nachbarn hat, wird in der ersten Zeile stehen.
            sql = "SELECT NodeId, GROUP_CONCAT(Neighbor SEPARATOR ';') allNeighbors, COUNT(NodeId) numberOfNeighbors "
                    + "FROM node_neighbor_relation GROUP BY NodeId ORDER BY numberOfNeighbors DESC";
            ResultSet queryResult = stmtGlobal.executeQuery(sql);
            // Liste, in der die Points(Nachbarn) gespeichert sind, 
            // die schon in irgendeinem Unfallschwerpunktbereich sich befinden.
            List<Integer> allUsedNeighborsInt = new ArrayList<>();//(dauernde Speicherung)
            // Liste für die Nachbarn des jetzt betrachteten Points. (temporaere Speicherung)
            List<Integer> neighborsInt = new ArrayList<>();
            // betrachte alle Points aus dem "SELECT"-Ergebnis
            while (queryResult.next()) {
                // speichere die Eigenschaften des Geo-Points
                int nodeId = queryResult.getInt("NodeId");
                int numberOfNeighbors = queryResult.getInt("numberOfNeighbors");
                String allNeighbors = queryResult.getString("allNeighbors");
                // zerlege das String mit Nachbarn des jetzt betrachteten Geo-Points.
                // speichere die Nachbarn als String-Werte
                String[] neighborsStr = allNeighbors.split(";");
                neighborsInt.clear(); // leere die temporaere Liste
                for (String neighborsStr1 : neighborsStr) {
                    // speichere die Nachbarn als Integer-Werte
                    neighborsInt.add(Integer.parseInt(neighborsStr1));
                }
                // hat der Geo-Point mehr als zwei Nachbarn?
                if (numberOfNeighbors >= 2) { // ja, hat er ...
                    // ueberpruefe, ob sich der jetzt betrachtete Geo-Point schon in der 
                    // Liste der verwendeten Punkten befindet. (befindet sich schon in einem Unfallschwerpunkts-Bereich) 
                    boolean isNodeIdWasUsed;
                    isNodeIdWasUsed = allUsedNeighborsInt.contains(nodeId);

                    if (!isNodeIdWasUsed) { // nein, der Geo-Point befindet sicht nicht in der Liste der verwendeten Punkten
                        // fuege die Nachbarn des betrachteten Geo-Points in die dauerhaftspeicherte Liste hinzu
                        allUsedNeighborsInt.addAll(neighborsInt);
                        // nimm Latitude & Longitude des betrachteten Geo-Points
                        sql = "SELECT Latitude, Longitude FROM received_coordinates WHERE NodeId = " + nodeId + "";
                        ResultSet queryResultLatLong = stmtGlobal3.executeQuery(sql);
                        queryResultLatLong.next();
                        double latitude = queryResultLatLong.getDouble("Latitude");
                        double longitude = queryResultLatLong.getDouble("Longitude");
                        int numberOfMember = numberOfNeighbors + 1; // Anzahl der Geo-Points in dem Unfallschwerpunkts-Bereich
                        // fuege den Unfallschwerpunkt in die Unfallschwerpunktstabelle hinzu
                        sql = "INSERT INTO accident_spots (NodeId,Latitude,Longitude,Number_of_members) VALUES ('" + nodeId + "','" + latitude + "','" + longitude + "','" + numberOfMember + "')";
                        stmtGlobal2.executeUpdate(sql);

                    }

                }
            }
            // schliesse alle Anfragen und Statements
            allUsedNeighborsInt.clear();
            stmtGlobal.close();
            stmtGlobal2.close();
            stmtGlobal3.close();
        } catch (SQLException ex) {
            Logger.getLogger(DB_Manager.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    /**
     * Die Methode prueft, ob der Geo-Point noch aktuell ist
     *
     * @param queryResult - Query-Objekt
     * @return true - ist aktuell, false - ist schon veraltet
     */
    public boolean isTimeStampOfCoordNotOld(ResultSet queryResult) {

        try {
            // nimm das Timestamp des Geo-Points
            Timestamp currentSystemTimeStamp = new Timestamp(date.getTime());
            Timestamp timeStampOfCoord = queryResult.getTimestamp("TimeStamp");

            Calendar calendar = Calendar.getInstance();
            calendar.setTime(timeStampOfCoord);
            calendar.add(Calendar.DAY_OF_WEEK, 30); // addiere 30 Tage zu timeStampOfCoord
            Timestamp timeStampOfCoordPlusPeriod = new Timestamp(calendar.getTime().getTime());
            
            //true - ist aktuell, false - ist schon veraltet
            return timeStampOfCoordPlusPeriod.after(currentSystemTimeStamp);

        } catch (SQLException ex) {
            Logger.getLogger(DB_Manager.class.getName()).log(Level.SEVERE, null, ex);
            return false;
        }

    }

    /**
     * schliesst die Verbindung zu DB und alle Anfragen und Statements
     */
    private void closeConnection() {
        try {
            stmt.close();
            conn.close();
            System.out.println("Connecting to database was closed!");
        } catch (SQLException ex) {
            Logger.getLogger(DB_Manager.class.getName()).log(Level.SEVERE, null, ex);
        }
    }

    public double calculateDistanceBetweenPoints(double lat1, double long1, double lat2, double long2) {

        double distance;
        // konvertiert Koordinaten in Radian
        double lat1_rad = Math.toRadians(lat1);
        double long1_rad = Math.toRadians(long1);
        double lat2_rad = Math.toRadians(lat2);
        double long2_rad = Math.toRadians(long2);

        // berechne Kreisentfernung in Radiant
        double angle_rad = Math.acos(Math.sin(lat1_rad) * Math.sin(lat2_rad)
                + Math.cos(lat1_rad) * Math.cos(lat2_rad) * Math.cos(long1_rad - long2_rad));

        // zuruck in Grad konvertieren
        angle_rad = Math.toDegrees(angle_rad);

        // ein Grad auf einem großen Kreis der Erde ist 60 nautische Meilen
        // 60 nautische Meilen = 111.1200km
        distance = 111120 * angle_rad;

        return distance;
    }

    public static void main(String[] args) {
        // erzeuge das Objekt der DB_Manager-Klasse
        DB_Manager dbManager = new DB_Manager();
        // erzeuge das Objekt der DB_Connector-Klasse
        DB_Connector dbConnector = new DB_Connector();
        // erstelle die Verbindung zur DB
        dbManager.createConnectionToDB(dbConnector);
        // leere folgende Tabellen in DB
        dbManager.truncateTable("node_neighbor_relation");
        dbManager.truncateTable("quantity_of_neighbors");
        dbManager.truncateTable("accident_spots");
        // mach die ganze Berechnungen
        dbManager.countNeighbors();
        // schliess die Verbindung
        dbManager.closeConnection();

        // just for Test:
        //dbManager.giveInformation();
    }
}
