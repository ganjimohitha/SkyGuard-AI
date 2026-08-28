import type { AnalyticsDataset, TimeRange } from "../types/analytics";

// TODO: Replace with aggregated time-series data from the analytics API.

const hourly24h: AnalyticsDataset = {
  temperatureTrend: [
    { label: "00:00", value: 24.1 },
    { label: "03:00", value: 22.8 },
    { label: "06:00", value: 23.6 },
    { label: "09:00", value: 27.9 },
    { label: "12:00", value: 32.4 },
    { label: "15:00", value: 33.8 },
    { label: "18:00", value: 30.2 },
    { label: "21:00", value: 26.5 },
  ],
  pressureTrend: [
    { label: "00:00", value: 1011.2 },
    { label: "03:00", value: 1011.8 },
    { label: "06:00", value: 1012.4 },
    { label: "09:00", value: 1011.6 },
    { label: "12:00", value: 1009.8 },
    { label: "15:00", value: 1008.9 },
    { label: "18:00", value: 1009.6 },
    { label: "21:00", value: 1010.7 },
  ],
  humidityTrend: [
    { label: "00:00", value: 78 },
    { label: "03:00", value: 81 },
    { label: "06:00", value: 79 },
    { label: "09:00", value: 68 },
    { label: "12:00", value: 58 },
    { label: "15:00", value: 54 },
    { label: "18:00", value: 63 },
    { label: "21:00", value: 72 },
  ],
  anomalyFrequency: [
    { label: "00:00", critical: 0, warning: 1 },
    { label: "03:00", critical: 0, warning: 0 },
    { label: "06:00", critical: 0, warning: 1 },
    { label: "09:00", critical: 1, warning: 1 },
    { label: "12:00", critical: 0, warning: 2 },
    { label: "15:00", critical: 1, warning: 0 },
    { label: "18:00", critical: 0, warning: 1 },
    { label: "21:00", critical: 0, warning: 0 },
  ],
  sensorStatusDistribution: [
    { name: "Excellent", value: 62, color: "#16a34a" },
    { name: "Good", value: 24, color: "#2563eb" },
    { name: "Warning", value: 10, color: "#f59e0b" },
    { name: "Critical", value: 4, color: "#ef4444" },
  ],
  detectionConfidence: [
    { label: "00:00", confidence: 91 },
    { label: "03:00", confidence: 88 },
    { label: "06:00", confidence: 93 },
    { label: "09:00", confidence: 95 },
    { label: "12:00", confidence: 97 },
    { label: "15:00", confidence: 94 },
    { label: "18:00", confidence: 92 },
    { label: "21:00", confidence: 90 },
  ],
};

const daily7d: AnalyticsDataset = {
  temperatureTrend: [
    { label: "Mon", value: 29.4 },
    { label: "Tue", value: 30.1 },
    { label: "Wed", value: 31.8 },
    { label: "Thu", value: 33.2 },
    { label: "Fri", value: 30.6 },
    { label: "Sat", value: 28.9 },
    { label: "Sun", value: 29.7 },
  ],
  pressureTrend: [
    { label: "Mon", value: 1010.9 },
    { label: "Tue", value: 1010.2 },
    { label: "Wed", value: 1009.4 },
    { label: "Thu", value: 1008.1 },
    { label: "Fri", value: 1009.8 },
    { label: "Sat", value: 1011.3 },
    { label: "Sun", value: 1011.9 },
  ],
  humidityTrend: [
    { label: "Mon", value: 70 },
    { label: "Tue", value: 73 },
    { label: "Wed", value: 76 },
    { label: "Thu", value: 81 },
    { label: "Fri", value: 74 },
    { label: "Sat", value: 66 },
    { label: "Sun", value: 68 },
  ],
  anomalyFrequency: [
    { label: "Mon", critical: 0, warning: 2 },
    { label: "Tue", critical: 1, warning: 1 },
    { label: "Wed", critical: 0, warning: 3 },
    { label: "Thu", critical: 2, warning: 2 },
    { label: "Fri", critical: 1, warning: 1 },
    { label: "Sat", critical: 0, warning: 0 },
    { label: "Sun", critical: 0, warning: 1 },
  ],
  sensorStatusDistribution: [
    { name: "Excellent", value: 58, color: "#16a34a" },
    { name: "Good", value: 27, color: "#2563eb" },
    { name: "Warning", value: 11, color: "#f59e0b" },
    { name: "Critical", value: 4, color: "#ef4444" },
  ],
  detectionConfidence: [
    { label: "Mon", confidence: 90 },
    { label: "Tue", confidence: 92 },
    { label: "Wed", confidence: 89 },
    { label: "Thu", confidence: 96 },
    { label: "Fri", confidence: 94 },
    { label: "Sat", confidence: 91 },
    { label: "Sun", confidence: 93 },
  ],
};

const monthly30d: AnalyticsDataset = {
  temperatureTrend: [
    { label: "Wk 1", value: 28.6 },
    { label: "Wk 2", value: 30.2 },
    { label: "Wk 3", value: 32.1 },
    { label: "Wk 4", value: 31.4 },
  ],
  pressureTrend: [
    { label: "Wk 1", value: 1011.5 },
    { label: "Wk 2", value: 1010.6 },
    { label: "Wk 3", value: 1009.2 },
    { label: "Wk 4", value: 1010.1 },
  ],
  humidityTrend: [
    { label: "Wk 1", value: 69 },
    { label: "Wk 2", value: 74 },
    { label: "Wk 3", value: 79 },
    { label: "Wk 4", value: 71 },
  ],
  anomalyFrequency: [
    { label: "Wk 1", critical: 2, warning: 5 },
    { label: "Wk 2", critical: 3, warning: 6 },
    { label: "Wk 3", critical: 1, warning: 4 },
    { label: "Wk 4", critical: 2, warning: 3 },
  ],
  sensorStatusDistribution: [
    { name: "Excellent", value: 55, color: "#16a34a" },
    { name: "Good", value: 29, color: "#2563eb" },
    { name: "Warning", value: 12, color: "#f59e0b" },
    { name: "Critical", value: 4, color: "#ef4444" },
  ],
  detectionConfidence: [
    { label: "Wk 1", confidence: 91 },
    { label: "Wk 2", confidence: 93 },
    { label: "Wk 3", confidence: 95 },
    { label: "Wk 4", confidence: 94 },
  ],
};

export const mockAnalyticsData: Record<TimeRange, AnalyticsDataset> = {
  "24h": hourly24h,
  "7d": daily7d,
  "30d": monthly30d,
};
