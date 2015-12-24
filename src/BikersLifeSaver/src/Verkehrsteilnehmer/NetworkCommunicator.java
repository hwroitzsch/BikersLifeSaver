package Verkehrsteilnehmer;

public interface NetworkCommunicator {

	SensorDataEvaluator sensorDataEvaluator = null;

	void notifySensorDataEvaluator();

	void sendEvent();

	void registerSensorDataEvaluator();

}