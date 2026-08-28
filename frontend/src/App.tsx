import Sidebar from "./components/Sidebar";
import Overview from "./pages/Overview";
import "./App.css";

function App() {
  return (
    <div className="app-shell">
      <Sidebar />

      <main className="app-main">
        <Overview />
      </main>
    </div>
  );
}

export default App;