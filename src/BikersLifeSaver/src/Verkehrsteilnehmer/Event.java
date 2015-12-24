package Verkehrsteilnehmer;

public class Event {

	private LocalDateTime timeStamp;
	private Vehicle eventSenderType;
	private GeoCoordinate geoCoordinate;
	private int eventID;

	public LocalDateTime getTimeStamp() {
		return this.timeStamp;
	}

	public Vehicle getEventSenderType() {
		return this.eventSenderType;
	}

	public int getEventID() {
		return this.eventID;
	}

}