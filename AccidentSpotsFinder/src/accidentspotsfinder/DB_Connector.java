package accidentspotsfinder;

import java.sql.*;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author BKonstantin
 */
public class DB_Connector {

    // JDBC-Driver und URL zur Datenbank
    private static final String JDBC_DRIVER = "com.mysql.jdbc.Driver";
    private static final String DB_URL = "jdbc:mysql://localhost/accidentspots";

    // User-Name und Passwort fuer die Datenbank
    private static final String USER = "root";
    private static final String PASS = "";

    // erzeuge Connection- & Statement-Objekte
    private Connection conn = null;
    private Statement stmt = null;

    public DB_Connector() {

        try {
            //STEP 2: JDBC-Driver registrieren
            Class.forName("com.mysql.jdbc.Driver");

            //STEP 3: die Verbindung zur Datenbank erstellen
            System.out.println("Connecting to database...");
            conn = DriverManager.getConnection(DB_URL, USER, PASS);
            
        } catch (SQLException | ClassNotFoundException ex) {
            Logger.getLogger(DB_Connector.class.getName()).log(Level.SEVERE, null, ex);
        }

    }

    /**
     * public-Methode, um die Verbindung zur Datenbank als ein Objekt
     * zurueckzugeben
     *
     * @return conn - Datenbankverbindung
     */
    public Connection createConnectionToDB() {
        if (conn == null) {
            DB_Connector db_Connector = new DB_Connector();
        }
        return conn;
    }

}
