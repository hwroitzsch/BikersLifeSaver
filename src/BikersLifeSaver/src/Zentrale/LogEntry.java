package Zentrale;

public class LogEntry {

	private LocalDateTime timeStamp;
	private int logEntryID;
	private int eventID;
	private int errorCodeID;

	public LocalDateTime getTimeStamp() {
		return this.timeStamp;
	}

	public void setTimeStamp(LocalDateTime timeStamp) {
		this.timeStamp = timeStamp;
	}

}