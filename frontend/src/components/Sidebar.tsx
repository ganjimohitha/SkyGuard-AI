import {
  Activity,
  AlertTriangle,
  BarChart3,
  HeartPulse,
  LayoutDashboard,
  Settings,
} from "lucide-react";
import type { Page } from "../types/navigation";

interface NavItem {
  page: Page;
  label: string;
  icon: React.ReactNode;
}

const navItems: NavItem[] = [
  { page: "overview", label: "Overview", icon: <LayoutDashboard size={19} /> },
  { page: "stations", label: "Stations", icon: <Activity size={19} /> },
  { page: "anomalies", label: "Anomalies", icon: <AlertTriangle size={19} /> },
  { page: "analytics", label: "Analytics", icon: <BarChart3 size={19} /> },
  { page: "sensor-health", label: "Sensor Health", icon: <HeartPulse size={19} /> },
];

interface SidebarProps {
  activePage: Page;
  onNavigate: (page: Page) => void;
}

function Sidebar({ activePage, onNavigate }: SidebarProps) {
  return (
    <aside className="w-64 min-h-screen bg-slate-950 text-white flex flex-col">
      {/* Logo */}
      <div className="px-6 py-6 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center">
            🛡️
          </div>

          <div>
            <h1 className="text-lg font-bold">SkyGuard AI</h1>
            <p className="text-xs text-slate-400">
              Weather Intelligence
            </p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-6 space-y-2">
        {navItems.map((item) => {
          const isActive = activePage === item.page;

          return (
            <button
              key={item.page}
              type="button"
              onClick={() => onNavigate(item.page)}
              className={
                isActive
                  ? "w-full flex items-center gap-3 px-4 py-3 rounded-lg bg-blue-600 text-white"
                  : "w-full flex items-center gap-3 px-4 py-3 rounded-lg text-slate-400 hover:bg-slate-800 hover:text-white"
              }
            >
              {item.icon}
              {item.label}
            </button>
          );
        })}
      </nav>

      {/* Settings */}
      <div className="px-4 pb-5">
        <button
          type="button"
          onClick={() => onNavigate("settings")}
          className={
            activePage === "settings"
              ? "w-full flex items-center gap-3 px-4 py-3 rounded-lg bg-blue-600 text-white"
              : "w-full flex items-center gap-3 px-4 py-3 rounded-lg text-slate-400 hover:bg-slate-800 hover:text-white"
          }
        >
          <Settings size={19} />
          Settings
        </button>

        <div className="mt-4 px-4 py-3 rounded-lg bg-slate-900">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-green-500" />
            <span className="text-xs font-medium">System Online</span>
          </div>

          <p className="text-[10px] text-slate-500 mt-1">
            All services operational
          </p>
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
