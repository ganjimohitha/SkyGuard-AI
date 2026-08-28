export type TimeRange = "24h" | "7d" | "30d";

export interface TrendPoint {
  label: string; // x-axis tick, e.g. "00:00" or "Mon"
  value: number;
}

export interface AnomalyFrequencyPoint {
  label: string;
  critical: number;
  warning: number;
}

export interface SensorStatusSlice {
  name: string;
  value: number;
  color: string;
}

export interface ConfidencePoint {
  label: string;
  confidence: number;
}

export interface AnalyticsDataset {
  temperatureTrend: TrendPoint[];
  pressureTrend: TrendPoint[];
  humidityTrend: TrendPoint[];
  anomalyFrequency: AnomalyFrequencyPoint[];
  sensorStatusDistribution: SensorStatusSlice[];
  detectionConfidence: ConfidencePoint[];
}
