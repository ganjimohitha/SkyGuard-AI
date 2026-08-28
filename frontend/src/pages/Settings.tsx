import { useState } from "react";

function Toggle({
  checked,
  onChange,
}: {
  checked: boolean;
  onChange: (value: boolean) => void;
}) {
  return (
    <label className="toggle">
      <input
        type="checkbox"
        checked={checked}
        onChange={(event) => onChange(event.target.checked)}
      />
      <span className="toggle-slider" />
    </label>
  );
}

function Settings() {
  // Frontend-only state for now — will be wired to the backend
  // configuration API once it is available.
  const [refreshInterval, setRefreshInterval] = useState("30");
  const [defaultView, setDefaultView] = useState("overview");
  const [timeFormat, setTimeFormat] = useState("24h");

  const [criticalAlerts, setCriticalAlerts] = useState(true);
  const [warningAlerts, setWarningAlerts] = useState(true);
  const [confidenceThreshold, setConfidenceThreshold] = useState("80");
  const [notifications, setNotifications] = useState(true);

  const [sensitivity, setSensitivity] = useState("balanced");
  const [tempThreshold, setTempThreshold] = useState("5");
  const [pressureThreshold, setPressureThreshold] = useState("10");
  const [humidityThreshold, setHumidityThreshold] = useState("15");

  return (
    <div className="page">
      {/* HEADER */}
      <div className="page-header">
        <div>
          <div className="section-label">CONFIGURATION</div>
          <h1>Settings</h1>
          <p>Configure SkyGuard AI monitoring and detection preferences.</p>
        </div>
      </div>

      <div className="settings-grid">
        {/* GENERAL SETTINGS */}
        <div className="settings-section">
          <h2>General Settings</h2>
          <p className="settings-section-desc">
            Basic dashboard behaviour and display preferences.
          </p>

          <div className="settings-row">
            <div className="settings-row-label">
              <strong>Station Refresh Interval</strong>
              <span>How often live station data is refreshed</span>
            </div>
            <div className="settings-control">
              <select value={refreshInterval} onChange={(e) => setRefreshInterval(e.target.value)}>
                <option value="15">Every 15 seconds</option>
                <option value="30">Every 30 seconds</option>
                <option value="60">Every 1 minute</option>
                <option value="300">Every 5 minutes</option>
              </select>
            </div>
          </div>

          <div className="settings-row">
            <div className="settings-row-label">
              <strong>Default Dashboard View</strong>
              <span>Page shown when SkyGuard AI opens</span>
            </div>
            <div className="settings-control">
              <select value={defaultView} onChange={(e) => setDefaultView(e.target.value)}>
                <option value="overview">Overview</option>
                <option value="stations">Stations</option>
                <option value="anomalies">Anomalies</option>
                <option value="analytics">Analytics</option>
              </select>
            </div>
          </div>

          <div className="settings-row">
            <div className="settings-row-label">
              <strong>Time Format</strong>
              <span>Display format for timestamps</span>
            </div>
            <div className="settings-control">
              <select value={timeFormat} onChange={(e) => setTimeFormat(e.target.value)}>
                <option value="24h">24-hour</option>
                <option value="12h">12-hour (AM/PM)</option>
              </select>
            </div>
          </div>
        </div>

        {/* ALERT SETTINGS */}
        <div className="settings-section">
          <h2>Alert Settings</h2>
          <p className="settings-section-desc">
            Control which alerts are raised and how confident the model must be.
          </p>

          <div className="settings-row">
            <div className="settings-row-label">
              <strong>Critical Alerts</strong>
              <span>Notify immediately for critical anomalies</span>
            </div>
            <Toggle checked={criticalAlerts} onChange={setCriticalAlerts} />
          </div>

          <div className="settings-row">
            <div className="settings-row-label">
              <strong>Warning Alerts</strong>
              <span>Notify for lower-severity warnings</span>
            </div>
            <Toggle checked={warningAlerts} onChange={setWarningAlerts} />
          </div>

          <div className="settings-row">
            <div className="settings-row-label">
              <strong>Confidence Threshold</strong>
              <span>Minimum ML confidence (%) required to raise an alert</span>
            </div>
            <div className="settings-control">
              <input
                type="number"
                min={0}
                max={100}
                value={confidenceThreshold}
                onChange={(e) => setConfidenceThreshold(e.target.value)}
              />
            </div>
          </div>

          <div className="settings-row">
            <div className="settings-row-label">
              <strong>Notifications</strong>
              <span>Show in-app notification toasts for new alerts</span>
            </div>
            <Toggle checked={notifications} onChange={setNotifications} />
          </div>
        </div>

        {/* DETECTION SETTINGS */}
        <div className="settings-section">
          <h2>Detection Settings</h2>
          <p className="settings-section-desc">
            Tune how sensitive the anomaly detection model is per parameter.
          </p>

          <div className="settings-row">
            <div className="settings-row-label">
              <strong>Detection Sensitivity</strong>
              <span>Overall model sensitivity to deviations</span>
            </div>
            <div className="settings-control">
              <select value={sensitivity} onChange={(e) => setSensitivity(e.target.value)}>
                <option value="low">Low</option>
                <option value="balanced">Balanced</option>
                <option value="high">High</option>
              </select>
            </div>
          </div>

          <div className="settings-row">
            <div className="settings-row-label">
              <strong>Temperature Threshold</strong>
              <span>Deviation (°C) from expected value to flag</span>
            </div>
            <div className="settings-control">
              <input
                type="number"
                value={tempThreshold}
                onChange={(e) => setTempThreshold(e.target.value)}
              />
            </div>
          </div>

          <div className="settings-row">
            <div className="settings-row-label">
              <strong>Pressure Threshold</strong>
              <span>Deviation (hPa) from expected value to flag</span>
            </div>
            <div className="settings-control">
              <input
                type="number"
                value={pressureThreshold}
                onChange={(e) => setPressureThreshold(e.target.value)}
              />
            </div>
          </div>

          <div className="settings-row">
            <div className="settings-row-label">
              <strong>Humidity Threshold</strong>
              <span>Deviation (%) from expected value to flag</span>
            </div>
            <div className="settings-control">
              <input
                type="number"
                value={humidityThreshold}
                onChange={(e) => setHumidityThreshold(e.target.value)}
              />
            </div>
          </div>
        </div>

        {/* SYSTEM INFORMATION */}
        <div className="settings-section">
          <h2>System Information</h2>
          <p className="settings-section-desc">
            Read-only details about the currently deployed system.
          </p>

          <div className="system-info-grid">
            <div className="system-info-item">
              <span>Application Version</span>
              <strong>v1.0.0-beta</strong>
            </div>
            <div className="system-info-item">
              <span>ML Model Version</span>
              <strong>anomaly-detector-v0.3</strong>
            </div>
            <div className="system-info-item">
              <span>Last Model Update</span>
              <strong>Not yet deployed</strong>
            </div>
            <div className="system-info-item">
              <span>API Connection Status</span>
              <strong>Not connected (mock data)</strong>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Settings;
