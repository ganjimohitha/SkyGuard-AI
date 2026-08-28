import { useMemo, useState } from "react";
import { AlertTriangle, CheckCircle2, ShieldAlert, Siren } from "lucide-react";
import { anomalySummary, mockAnomalies } from "../data/mockAnomalies";
import type { AnomalySeverity } from "../types/anomaly";

type SeverityFilter = "all" | AnomalySeverity;

const filters: { key: SeverityFilter; label: string }[] = [
  { key: "all", label: "All" },
  { key: "critical", label: "Critical" },
  { key: "warning", label: "Warning" },
  { key: "resolved", label: "Resolved" },
];

const severityLabel: Record<AnomalySeverity, string> = {
  critical: "Critical",
  warning: "Warning",
  resolved: "Resolved",
};

function Anomalies() {
  const [severityFilter, setSeverityFilter] = useState<SeverityFilter>("all");

  const filteredAnomalies = useMemo(() => {
    if (severityFilter === "all") return mockAnomalies;
    return mockAnomalies.filter((anomaly) => anomaly.severity === severityFilter);
  }, [severityFilter]);

  return (
    <div className="page">
      {/* HEADER */}
      <div className="page-header">
        <div>
          <div className="section-label">AI DETECTION ENGINE</div>
          <h1>Anomaly Detection</h1>
          <p>AI-powered detection of abnormal weather observations.</p>
        </div>
      </div>

      {/* SUMMARY CARDS */}
      <div className="stats-grid" style={{ marginBottom: 24 }}>
        <StatCard icon={<ShieldAlert />} title="Active Anomalies" value={String(anomalySummary.active)} />
        <StatCard icon={<Siren />} title="Critical" value={String(anomalySummary.critical)} />
        <StatCard icon={<AlertTriangle />} title="Warnings" value={String(anomalySummary.warnings)} />
        <StatCard icon={<CheckCircle2 />} title="Resolved" value={String(anomalySummary.resolved)} />
      </div>

      {/* FILTERS */}
      <div className="toolbar">
        <div className="filter-pills">
          {filters.map((filter) => (
            <button
              key={filter.key}
              type="button"
              className={`filter-pill ${severityFilter === filter.key ? "active" : ""}`}
              onClick={() => setSeverityFilter(filter.key)}
            >
              {filter.label}
            </button>
          ))}
        </div>
      </div>

      {/* ANOMALY LIST */}
      {filteredAnomalies.length === 0 ? (
        <div className="table-panel">
          <div className="empty-state">
            <div className="empty-icon">✅</div>
            <h3>No anomalies in this category</h3>
            <p>The network is behaving within expected parameters.</p>
          </div>
        </div>
      ) : (
        <div className="anomaly-detail-list">
          {filteredAnomalies.map((anomaly) => (
            <div key={anomaly.id} className={`anomaly-detail-card ${anomaly.severity}`}>
              <div className="anomaly-detail-main">
                <div className="anomaly-detail-head">
                  <strong>{anomaly.anomalyType}</strong>
                  <span className={`badge ${anomaly.severity}`}>
                    <span className="badge-dot" />
                    {severityLabel[anomaly.severity]}
                  </span>
                </div>

                <div className="anomaly-detail-station">
                  {anomaly.station} &middot; {anomaly.location}
                </div>

                <div className="anomaly-detail-values">
                  <span>
                    Parameter
                    <strong>{anomaly.parameter}</strong>
                  </span>
                  <span>
                    Current Value
                    <strong>{anomaly.currentValue}</strong>
                  </span>
                  <span>
                    Expected Value
                    <strong>{anomaly.expectedValue}</strong>
                  </span>
                </div>
              </div>

              <div className="anomaly-detail-side">
                <span className="anomaly-confidence">{anomaly.confidence}%</span>
                <span className="anomaly-time">{anomaly.detectedAt}</span>
              </div>
            </div>
          ))}
        </div>
      )}
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

export default Anomalies;
