import {
  Activity,
  AlertTriangle,
  CheckCircle2,
  Radio,
} from "lucide-react";

const anomalies = [
  {
    station: "AWS-017",
    issue: "Temperature Spike",
    confidence: "97%",
    type: "critical",
  },
  {
    station: "AWS-009",
    issue: "Sensor Drift",
    confidence: "84%",
    type: "warning",
  },
  {
    station: "AWS-021",
    issue: "Frozen Value",
    confidence: "91%",
    type: "warning",
  },
];

function Overview() {
  return (
    <div className="dashboard">

      {/* HEADER */}
      <div className="dashboard-header">
        <div>
          <div className="section-label">
            WEATHER OBSERVATION NETWORK
          </div>

          <h1>Network Overview</h1>

          <p>
            Real-time monitoring and intelligent anomaly detection.
          </p>
        </div>

        <div className="live-status">
          <span className="live-dot"></span>
          LIVE
        </div>
      </div>

      {/* STAT CARDS */}
      <div className="stats-grid">

        <StatCard
          icon={<Radio />}
          title="Total Stations"
          value="24"
        />

        <StatCard
          icon={<CheckCircle2 />}
          title="Healthy"
          value="21"
        />

        <StatCard
          icon={<AlertTriangle />}
          title="Warnings"
          value="2"
        />

        <StatCard
          icon={<Activity />}
          title="Critical"
          value="1"
        />

      </div>

      {/* MAIN CONTENT */}
      <div className="main-grid">

        {/* AWS NETWORK */}
        <div className="panel network-panel">

          <div className="panel-title">
            <div>
              <h2>AWS Network</h2>
              <p>Live status of weather stations</p>
            </div>
          </div>

          <div className="network-map">

            <div className="map-placeholder">

              <div className="map-icon">
                🗺️
              </div>

              <h3>AWS Network Map</h3>

              <p>
                Interactive map coming next
              </p>

            </div>

          </div>

        </div>

        {/* RECENT ANOMALIES */}
        <div className="panel anomalies-panel">

          <div className="panel-title">

            <div>
              <h2>Recent Anomalies</h2>
              <p>Latest intelligent alerts</p>
            </div>

          </div>

          <div className="anomaly-list">

            {anomalies.map((anomaly) => (

              <div
                key={anomaly.station}
                className={`anomaly-card ${anomaly.type}`}
              >

                <div className="anomaly-left">

                  <span className="anomaly-dot"></span>

                  <div>
                    <strong>
                      {anomaly.station}
                    </strong>

                    <p>
                      {anomaly.issue}
                    </p>
                  </div>

                </div>

                <strong className="confidence">
                  {anomaly.confidence}
                </strong>

              </div>

            ))}

          </div>

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

      <div className="stat-icon">
        {icon}
      </div>

      <div className="stat-info">

        <span>{title}</span>

        <strong>{value}</strong>

      </div>

    </div>
  );
}

export default Overview;