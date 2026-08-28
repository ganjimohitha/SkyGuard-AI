export type SensorCondition = "Excellent" | "Good" | "Warning" | "Critical";

export type SensorOverallStatus = "healthy" | "warning" | "critical";

export interface SensorHealth {
  station: string;
  location: string;
  healthScore: number; // 0 - 100
  temperatureCondition: SensorCondition;
  pressureCondition: SensorCondition;
  humidityCondition: SensorCondition;
  lastCalibration: string; // human readable date
  status: SensorOverallStatus;
  maintenanceRecommendation: string;
}
