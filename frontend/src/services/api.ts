/**
 * SkyGuard AI - Data service layer
 *
 * The backend + ML anomaly detection service is being built separately.
 * Every function here currently resolves with local mock data, but the
 * function signatures are already shaped like async API calls
 * (Promise-based) so pages don't need to change when the real backend
 * (REST / WebSocket) is wired in — only the implementation below does.
 */

import type { Station } from "../types/station";
import type { Anomaly } from "../types/anomaly";
import type { SensorHealth } from "../types/sensor";
import type { AnalyticsDataset, TimeRange } from "../types/analytics";

import {
  mockStations,
  stationSummary as mockStationSummary,
} from "../data/mockStations";
import {
  mockAnomalies,
  anomalySummary as mockAnomalySummary,
} from "../data/mockAnomalies";
import {
  mockSensorHealth,
  sensorHealthSummary as mockSensorHealthSummary,
} from "../data/mockSensorHealth";
import { mockAnalyticsData } from "../data/mockAnalytics";

// Base URL for the future backend. Not used yet — update once the
// backend team publishes the deployed API URL.
export const API_BASE_URL = "http://localhost:8000/api";

export async function fetchStations(): Promise<Station[]> {
  return Promise.resolve(mockStations);
}

export async function fetchStationSummary() {
  return Promise.resolve(mockStationSummary);
}

export async function fetchAnomalies(): Promise<Anomaly[]> {
  return Promise.resolve(mockAnomalies);
}

export async function fetchAnomalySummary() {
  return Promise.resolve(mockAnomalySummary);
}

export async function fetchSensorHealth(): Promise<SensorHealth[]> {
  return Promise.resolve(mockSensorHealth);
}

export async function fetchSensorHealthSummary() {
  return Promise.resolve(mockSensorHealthSummary);
}

export async function fetchAnalytics(
  range: TimeRange,
): Promise<AnalyticsDataset> {
  return Promise.resolve(mockAnalyticsData[range]);
}
