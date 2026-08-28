import { useState } from "react";
import Sidebar from "./components/Sidebar";
import Overview from "./pages/Overview";
import Stations from "./pages/Stations";
import Anomalies from "./pages/Anomalies";
import Analytics from "./pages/Analytics";
import SensorHealth from "./pages/SensorHealth";
import Settings from "./pages/Settings";
import type { Page } from "./types/navigation";
import "./App.css";

function App() {
  const [activePage, setActivePage] = useState<Page>("overview");

  const renderPage = () => {
    switch (activePage) {
      case "overview":
        return <Overview />;
      case "stations":
        return <Stations />;
      case "anomalies":
        return <Anomalies />;
      case "analytics":
        return <Analytics />;
      case "sensor-health":
        return <SensorHealth />;
      case "settings":
        return <Settings />;
      default:
        return <Overview />;
    }
  };

  return (
    <div className="app-shell">
      <Sidebar activePage={activePage} onNavigate={setActivePage} />

      <main className="app-main">{renderPage()}</main>
    </div>
  );
}

export default App;
