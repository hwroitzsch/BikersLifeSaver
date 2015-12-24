package Zentrale;

public class Query {

	private LocalDateTime timeStamp;
	private Vehicle querySenderType;
	private GeoCoordinate geoCoordinate;

	public LocalDateTime getTimeStamp() {
		return this.timeStamp;
	}

	public Vehicle getQuerySenderType() {
		return this.querySenderType;
	}

	public GeoCoordinate getGeoCoordinate() {
		return this.geoCoordinate;
	}

}