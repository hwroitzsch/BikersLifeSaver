package Verkehrsteilnehmer;

public abstract class SensorData {

	private int sensorID;
	private SensorType sensorType;
	private LocalDateTime timeStamp;
	private T data;

	public int getSensorID() {
		return this.sensorID;
	}

	public SensorType getSensorType() {
		return this.sensorType;
	}

	public LocalDateTime getTimeStamp() {
		return this.timeStamp;
	}

	public void setTimeStamp(LocalDateTime timeStamp) {
		this.timeStamp = timeStamp;
	}

	public T getData() {
		return this.data;
	}

	public void setData(T data) {
		this.data = data;
	}

}