import { useMemo, useState } from "react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { mockAnalyticsData } from "../data/mockAnalytics";
import type { TimeRange } from "../types/analytics";

const rangeOptions: { key: TimeRange; label: string }[] = [
  { key: "24h", label: "24 Hours" },
  { key: "7d", label: "7 Days" },
  { key: "30d", label: "30 Days" },
];

const axisStyle = { fontSize: 11, fill: "#64748b" };
const tooltipStyle = {
  borderRadius: 10,
  border: "1px solid #e2e8f0",
  fontSize: 12,
};

function Analytics() {
  const [range, setRange] = useState<TimeRange>("24h");

  const data = useMemo(() => mockAnalyticsData[range], [range]);

  return (
    <div className="page">
      {/* HEADER */}
      <div className="page-header">
        <div>
          <div className="section-label">NETWORK INTELLIGENCE</div>
          <h1>Analytics</h1>
          <p>Analyze atmospheric patterns and anomaly behavior across the AWS network.</p>
        </div>

        <div className="range-toggle">
          {rangeOptions.map((option) => (
            <button
              key={option.key}
              type="button"
              className={range === option.key ? "active" : ""}
              onClick={() => setRange(option.key)}
            >
              {option.label}
            </button>
          ))}
        </div>
      </div>

      {/* CHARTS */}
      <div className="charts-grid">
        <div className="panel chart-panel">
          <h2>Temperature Trend</h2>
          <p>Average network temperature (°C)</p>
          <ResponsiveContainer width="100%" height={220}>
            <AreaChart data={data.temperatureTrend}>
              <defs>
                <linearGradient id="tempGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#2563eb" stopOpacity={0.25} />
                  <stop offset="95%" stopColor="#2563eb" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid stroke="#f1f5f9" vertical={false} />
              <XAxis dataKey="label" tick={axisStyle} axisLine={false} tickLine={false} />
              <YAxis tick={axisStyle} axisLine={false} tickLine={false} width={36} />
              <Tooltip contentStyle={tooltipStyle} />
              <Area
                type="monotone"
                dataKey="value"
                stroke="#2563eb"
                strokeWidth={2}
                fill="url(#tempGradient)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="panel chart-panel">
          <h2>Pressure Trend</h2>
          <p>Average atmospheric pressure (hPa)</p>
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={data.pressureTrend}>
              <CartesianGrid stroke="#f1f5f9" vertical={false} />
              <XAxis dataKey="label" tick={axisStyle} axisLine={false} tickLine={false} />
              <YAxis tick={axisStyle} axisLine={false} tickLine={false} width={44} domain={["auto", "auto"]} />
              <Tooltip contentStyle={tooltipStyle} />
              <Line type="monotone" dataKey="value" stroke="#0ea5e9" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="panel chart-panel">
          <h2>Humidity Trend</h2>
          <p>Average relative humidity (%)</p>
          <ResponsiveContainer width="100%" height={220}>
            <AreaChart data={data.humidityTrend}>
              <defs>
                <linearGradient id="humidityGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#16a34a" stopOpacity={0.25} />
                  <stop offset="95%" stopColor="#16a34a" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid stroke="#f1f5f9" vertical={false} />
              <XAxis dataKey="label" tick={axisStyle} axisLine={false} tickLine={false} />
              <YAxis tick={axisStyle} axisLine={false} tickLine={false} width={36} />
              <Tooltip contentStyle={tooltipStyle} />
              <Area
                type="monotone"
                dataKey="value"
                stroke="#16a34a"
                strokeWidth={2}
                fill="url(#humidityGradient)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="panel chart-panel">
          <h2>Anomaly Frequency</h2>
          <p>Critical vs. warning detections over time</p>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={data.anomalyFrequency}>
              <CartesianGrid stroke="#f1f5f9" vertical={false} />
              <XAxis dataKey="label" tick={axisStyle} axisLine={false} tickLine={false} />
              <YAxis tick={axisStyle} axisLine={false} tickLine={false} width={24} allowDecimals={false} />
              <Tooltip contentStyle={tooltipStyle} />
              <Bar dataKey="critical" stackId="a" fill="#ef4444" radius={[0, 0, 0, 0]} />
              <Bar dataKey="warning" stackId="a" fill="#f59e0b" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="panel chart-panel">
          <h2>Sensor Status Distribution</h2>
          <p>Share of sensors by condition</p>
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Tooltip contentStyle={tooltipStyle} />
              <Pie
                data={data.sensorStatusDistribution}
                dataKey="value"
                nameKey="name"
                innerRadius={55}
                outerRadius={80}
                paddingAngle={2}
              >
                {data.sensorStatusDistribution.map((slice) => (
                  <Cell key={slice.name} fill={slice.color} />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
          <div className="filter-pills" style={{ justifyContent: "center", marginTop: 8 }}>
            {data.sensorStatusDistribution.map((slice) => (
              <span key={slice.name} style={{ display: "flex", alignItems: "center", gap: 6, fontSize: 11, color: "#64748b" }}>
                <span style={{ width: 8, height: 8, borderRadius: "50%", background: slice.color, display: "inline-block" }} />
                {slice.name} ({slice.value}%)
              </span>
            ))}
          </div>
        </div>

        <div className="panel chart-panel">
          <h2>Detection Confidence</h2>
          <p>Average ML model confidence score</p>
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={data.detectionConfidence}>
              <CartesianGrid stroke="#f1f5f9" vertical={false} />
              <XAxis dataKey="label" tick={axisStyle} axisLine={false} tickLine={false} />
              <YAxis tick={axisStyle} axisLine={false} tickLine={false} width={30} domain={[0, 100]} />
              <Tooltip contentStyle={tooltipStyle} />
              <Line type="monotone" dataKey="confidence" stroke="#7c3aed" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

export default Analytics;
