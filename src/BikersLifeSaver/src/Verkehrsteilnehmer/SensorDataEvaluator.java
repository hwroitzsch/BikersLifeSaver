package Verkehrsteilnehmer;

public class SensorDataEvaluator {

	private HashMap<Integer, ArrayList<ProcessedSensorData>> sensorProcessSensorDataMap;
	private ArrayList<NetworkCommunicator> networkCommunicators;

	/**
	 * 
	 * @param processedSensorData
	 */
	public void evaluateProcessedSensorData(ProcessedSensorData processedSensorData) {
		// TODO - implement SensorDataEvaluator.evaluateProcessedSensorData
		throw new UnsupportedOperationException();
	}

	private void emitWarningSignal() {
		// TODO - implement SensorDataEvaluator.emitWarningSignal
		throw new UnsupportedOperationException();
	}

	/**
	 * 
	 * @param event
	 */
	private void notifyNetworkCommunicators(Event event) {
		// TODO - implement SensorDataEvaluator.notifyNetworkCommunicators
		throw new UnsupportedOperationException();
	}

	public void registerNetworkCommunicator() {
		// TODO - implement SensorDataEvaluator.registerNetworkCommunicator
		throw new UnsupportedOperationException();
	}

}