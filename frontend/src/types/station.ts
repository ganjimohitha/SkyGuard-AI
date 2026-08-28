export type StationStatus = "healthy" | "warning" | "critical";

export interface Station {
  id: string;
  location: string;
  state: string;
  temperature: number; // °C
  pressure: number; // hPa
  humidity: number; // %
  status: StationStatus;
  lastUpdated: string; // human readable, e.g. "2 min ago"
}
