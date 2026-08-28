import { HeartPulse, ShieldCheck, Wrench, AlertOctagon } from "lucide-react";
import { mockSensorHealth, sensorHealthSummary } from "../data/mockSensorHealth";
import type { SensorCondition, SensorOverallStatus } from "../types/sensor";

const conditionToStatus: Record<SensorCondition, SensorOverallStatus> = {
  Excellent: "healthy",
  Good: "healthy",
  Warning: "warning",
  Critical: "critical",
};

const statusColor: Record<SensorOverallStatus, string> = {
  healthy: "#16a34a",
  warning: "#f59e0b",
  critical: "#ef4444",
};

function ConditionBadge({ condition }: { condition: SensorCondition }) {
  const status = conditionToStatus[condition];
  return (
    <span className={`badge ${status}`}>
      <span className="badge-dot" />
      {condition}
    </span>
  );
}

function SensorHealth() {
  return (
    <div className="page">
      {/* HEADER */}
      <div className="page-header">
        <div>
          <div className="section-label">SENSOR DIAGNOSTICS</div>
          <h1>Sensor Health</h1>
          <p>Monitor sensor reliability, degradation, and maintenance requirements.</p>
        </div>
      </div>

      {/* SUMMARY CARDS */}
      <div className="stats-grid" style={{ marginBottom: 24 }}>
        <StatCard icon={<ShieldCheck />} title="Healthy Sensors" value={String(sensorHealthSummary.healthy)} />
        <StatCard icon={<HeartPulse />} title="Sensors at Risk" value={String(sensorHealthSummary.atRisk)} />
        <StatCard icon={<Wrench />} title="Maintenance Required" value={String(sensorHealthSummary.maintenanceRequired)} />
        <StatCard icon={<AlertOctagon />} title="Network Health" value={`${sensorHealthSummary.networkHealth}%`} />
      </div>

      {/* TABLE */}
      <div className="table-panel">
        <div className="table-scroll">
          <table className="data-table">
            <thead>
              <tr>
                <th>Station</th>
                <th>Health Score</th>
                <th>Temperature</th>
                <th>Pressure</th>
                <th>Humidity</th>
                <th>Last Calibration</th>
                <th>Status</th>
                <th>Recommendation</th>
              </tr>
            </thead>
            <tbody>
              {mockSensorHealth.map((sensor) => (
                <tr key={sensor.station}>
                  <td className="cell-strong">
                    {sensor.station}
                    <div className="cell-muted" style={{ fontSize: 11, marginTop: 2 }}>
                      {sensor.location}
                    </div>
                  </td>
                  <td>
                    <div className="health-score-cell">
                      <span className="health-score-value">{sensor.healthScore}%</span>
                      <div className="health-bar-track">
                        <div
                          className="health-bar-fill"
                          style={{
                            width: `${sensor.healthScore}%`,
                            background: statusColor[sensor.status],
                          }}
                        />
                      </div>
                    </div>
                  </td>
                  <td>
                    <ConditionBadge condition={sensor.temperatureCondition} />
                  </td>
                  <td>
                    <ConditionBadge condition={sensor.pressureCondition} />
                  </td>
                  <td>
                    <ConditionBadge condition={sensor.humidityCondition} />
                  </td>
                  <td className="cell-muted">{sensor.lastCalibration}</td>
                  <td>
                    <span className={`badge ${sensor.status}`}>
                      <span className="badge-dot" />
                      {sensor.status === "healthy"
                        ? "Healthy"
                        : sensor.status === "warning"
                          ? "Warning"
                          : "Critical"}
                    </span>
                  </td>
                  <td className="cell-muted">{sensor.maintenanceRecommendation}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
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

export default SensorHealth;
