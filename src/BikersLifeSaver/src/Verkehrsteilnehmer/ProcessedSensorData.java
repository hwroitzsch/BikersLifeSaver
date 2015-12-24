package Verkehrsteilnehmer;

public class ProcessedSensorData {

	private Vehicle detectedVehicle;
	private double distance;
	private double speed;
	private int sensorID;
	private SensorType sensorType;
	private LocalDateTime timeStamp;
	private GeoCoordinate geoCoordinate;

	public Vehicle getDetectedVehicle() {
		return this.detectedVehicle;
	}

	public double getDistance() {
		return this.distance;
	}

	public double getSpeed() {
		return this.speed;
	}

	public int getSensorID() {
		return this.sensorID;
	}

	public SensorType getSensorType() {
		return this.sensorType;
	}

	public LocalDateTime getTimeStamp() {
		return this.timeStamp;
	}

	public boolean hasSpeed() {
		// TODO - implement ProcessedSensorData.hasSpeed
		throw new UnsupportedOperationException();
	}

	public boolean hasDistance() {
		// TODO - implement ProcessedSensorData.hasDistance
		throw new UnsupportedOperationException();
	}

}