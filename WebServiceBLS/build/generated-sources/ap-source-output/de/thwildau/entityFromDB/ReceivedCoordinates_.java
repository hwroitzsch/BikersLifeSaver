package de.thwildau.entityFromDB;

import java.util.Date;
import javax.annotation.Generated;
import javax.persistence.metamodel.SingularAttribute;
import javax.persistence.metamodel.StaticMetamodel;

@Generated(value="EclipseLink-2.5.2.v20140319-rNA", date="2015-12-05T16:13:33")
@StaticMetamodel(ReceivedCoordinates.class)
public class ReceivedCoordinates_ { 

    public static volatile SingularAttribute<ReceivedCoordinates, Date> timeStamp;
    public static volatile SingularAttribute<ReceivedCoordinates, Double> latitude;
    public static volatile SingularAttribute<ReceivedCoordinates, Integer> nodeId;
    public static volatile SingularAttribute<ReceivedCoordinates, Double> longitude;

}