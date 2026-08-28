import { useMemo, useState } from "react";
import { Activity, AlertTriangle, CheckCircle2, Radio, Search } from "lucide-react";
import { mockStations, stationSummary } from "../data/mockStations";
import type { StationStatus } from "../types/station";

type StatusFilter = "all" | StationStatus;

const statusLabel: Record<StationStatus, string> = {
  healthy: "Healthy",
  warning: "Warning",
  critical: "Critical",
};

function StatusBadge({ status }: { status: StationStatus }) {
  return (
    <span className={`badge ${status}`}>
      <span className="badge-dot" />
      {statusLabel[status]}
    </span>
  );
}

function Stations() {
  const [query, setQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState<StatusFilter>("all");

  const filteredStations = useMemo(() => {
    return mockStations.filter((station) => {
      const matchesQuery =
        query.trim().length === 0 ||
        station.id.toLowerCase().includes(query.toLowerCase()) ||
        station.location.toLowerCase().includes(query.toLowerCase());

      const matchesStatus =
        statusFilter === "all" || station.status === statusFilter;

      return matchesQuery && matchesStatus;
    });
  }, [query, statusFilter]);

  return (
    <div className="page">
      {/* HEADER */}
      <div className="page-header">
        <div>
          <div className="section-label">WEATHER OBSERVATION NETWORK</div>
          <h1>Weather Stations</h1>
          <p>Monitor live observations from Automatic Weather Stations.</p>
        </div>
      </div>

      {/* SUMMARY CARDS */}
      <div className="stats-grid" style={{ marginBottom: 24 }}>
        <StatCard icon={<Radio />} title="Total Stations" value={String(stationSummary.total)} />
        <StatCard icon={<CheckCircle2 />} title="Healthy" value={String(stationSummary.healthy)} />
        <StatCard icon={<AlertTriangle />} title="Warnings" value={String(stationSummary.warnings)} />
        <StatCard icon={<Activity />} title="Critical" value={String(stationSummary.critical)} />
      </div>

      {/* TOOLBAR */}
      <div className="toolbar">
        <div className="search-box">
          <Search size={16} />
          <input
            type="text"
            placeholder="Search by station ID or location..."
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />
        </div>

        <select
          className="filter-select"
          value={statusFilter}
          onChange={(event) => setStatusFilter(event.target.value as StatusFilter)}
        >
          <option value="all">All Statuses</option>
          <option value="healthy">Healthy</option>
          <option value="warning">Warning</option>
          <option value="critical">Critical</option>
        </select>
      </div>

      {/* TABLE */}
      <div className="table-panel">
        {filteredStations.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">🔍</div>
            <h3>No stations found</h3>
            <p>Try adjusting your search or status filter.</p>
          </div>
        ) : (
          <div className="table-scroll">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Station ID</th>
                  <th>Location</th>
                  <th>Temperature</th>
                  <th>Pressure</th>
                  <th>Humidity</th>
                  <th>Status</th>
                  <th>Last Updated</th>
                </tr>
              </thead>
              <tbody>
                {filteredStations.map((station) => (
                  <tr key={station.id}>
                    <td className="cell-strong">{station.id}</td>
                    <td>{station.location}</td>
                    <td>{station.temperature.toFixed(1)}°C</td>
                    <td>{station.pressure.toFixed(1)} hPa</td>
                    <td>{station.humidity.toFixed(1)}%</td>
                    <td>
                      <StatusBadge status={station.status} />
                    </td>
                    <td className="cell-muted">{station.lastUpdated}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

function StatCard({
  icon,
  title,
  value,
}: {
  icon: React.ReactNode;
  title: string;
  value: string;
}) {
  return (
    <div className="stat-card">
      <div className="stat-icon">{icon}</div>
      <div className="stat-info">
        <span>{title}</span>
        <strong>{value}</strong>
      </div>
    </div>
  );
}

export default Stations;
