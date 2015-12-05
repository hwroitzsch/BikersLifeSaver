/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package de.thwildau.entityFromDB;

import java.io.Serializable;
import java.util.Date;
import javax.persistence.Basic;
import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.NamedQueries;
import javax.persistence.NamedQuery;
import javax.persistence.Table;
import javax.persistence.Temporal;
import javax.persistence.TemporalType;
import javax.validation.constraints.NotNull;
import javax.xml.bind.annotation.XmlRootElement;

/**
 *
 * @author BKonstantin
 */
@Entity
@Table(name = "received_coordinates")
@XmlRootElement
@NamedQueries({
    @NamedQuery(name = "ReceivedCoordinates.findAll", query = "SELECT r FROM ReceivedCoordinates r"),
    @NamedQuery(name = "ReceivedCoordinates.findByNodeId", query = "SELECT r FROM ReceivedCoordinates r WHERE r.nodeId = :nodeId"),
    @NamedQuery(name = "ReceivedCoordinates.findByLatitude", query = "SELECT r FROM ReceivedCoordinates r WHERE r.latitude = :latitude"),
    @NamedQuery(name = "ReceivedCoordinates.findByLongitude", query = "SELECT r FROM ReceivedCoordinates r WHERE r.longitude = :longitude"),
    @NamedQuery(name = "ReceivedCoordinates.findByTimeStamp", query = "SELECT r FROM ReceivedCoordinates r WHERE r.timeStamp = :timeStamp")})
public class ReceivedCoordinates implements Serializable {
    private static final long serialVersionUID = 1L;
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Basic(optional = false)
    @Column(name = "NodeId")
    private Integer nodeId;
    @Basic(optional = false)
    @NotNull
    @Column(name = "Latitude")
    private double latitude;
    @Basic(optional = false)
    @NotNull
    @Column(name = "Longitude")
    private double longitude;
    @Basic(optional = false)
    @NotNull
    @Column(name = "TimeStamp")
    @Temporal(TemporalType.TIMESTAMP)
    private Date timeStamp;

    public ReceivedCoordinates() {
    }

    public ReceivedCoordinates(Integer nodeId) {
        this.nodeId = nodeId;
    }

    public ReceivedCoordinates(Integer nodeId, double latitude, double longitude, Date timeStamp) {
        this.nodeId = nodeId;
        this.latitude = latitude;
        this.longitude = longitude;
        this.timeStamp = timeStamp;
    }

    public Integer getNodeId() {
        return nodeId;
    }

    public void setNodeId(Integer nodeId) {
        this.nodeId = nodeId;
    }

    public double getLatitude() {
        return latitude;
    }

    public void setLatitude(double latitude) {
        this.latitude = latitude;
    }

    public double getLongitude() {
        return longitude;
    }

    public void setLongitude(double longitude) {
        this.longitude = longitude;
    }

    public Date getTimeStamp() {
        return timeStamp;
    }

    public void setTimeStamp(Date timeStamp) {
        this.timeStamp = timeStamp;
    }

    @Override
    public int hashCode() {
        int hash = 0;
        hash += (nodeId != null ? nodeId.hashCode() : 0);
        return hash;
    }

    @Override
    public boolean equals(Object object) {
        // TODO: Warning - this method won't work in the case the id fields are not set
        if (!(object instanceof ReceivedCoordinates)) {
            return false;
        }
        ReceivedCoordinates other = (ReceivedCoordinates) object;
        if ((this.nodeId == null && other.nodeId != null) || (this.nodeId != null && !this.nodeId.equals(other.nodeId))) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        return "de.thwildau.entityFromDB.ReceivedCoordinates[ nodeId=" + nodeId + " ]";
    }
    
}
