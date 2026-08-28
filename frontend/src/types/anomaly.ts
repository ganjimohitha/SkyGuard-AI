export type AnomalySeverity = "critical" | "warning" | "resolved";

export interface Anomaly {
  id: string;
  station: string;
  location: string;
  anomalyType: string;
  parameter: "Temperature" | "Pressure" | "Humidity";
  currentValue: string;
  expectedValue: string;
  confidence: number; // 0 - 100
  severity: AnomalySeverity;
  detectedAt: string; // human readable
}
