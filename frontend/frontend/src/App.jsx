import { useState } from "react";
import { useApp } from "./context/AppContext";
import Sidebar from "./components/common/Sidebar";
import Navbar from "./components/common/Navbar";

import Landing from "./pages/Landing";
import Dashboard from "./pages/Dashboard";
import UploadResume from "./pages/UploadResume";
import CareerProfile from "./pages/CareerProfile";
import Opportunities from "./pages/Opportunities";
import MatchDetails from "./pages/MatchDetails";
import SkillGap from "./pages/SkillGap";
import Roadmap from "./pages/Roadmap";
import Simulator from "./pages/Simulator";
import CareerChat from "./pages/CareerChat";
import RecruiterDashboard from "./pages/RecruiterDashboard";
import ModelPerformance from "./pages/ModelPerformance";

const PAGES = {
  dashboard: Dashboard, upload: UploadResume, profile: CareerProfile, opportunities: Opportunities,
  matching: MatchDetails, gap: SkillGap, roadmap: Roadmap, simulator: Simulator,
  chat: CareerChat, recruiter: RecruiterDashboard, performance: ModelPerformance,
};

const SIDE = [
  { id: "dashboard", label: "Dashboard", icon: "🏠" },
  { id: "upload", label: "Upload resume", icon: "📄" },
  { id: "profile", label: "Career profile", icon: "👤" },
  { id: "opportunities", label: "Opportunities", icon: "💼" },
  { id: "matching", label: "Match details", icon: "🎯" },
  { id: "gap", label: "Skill gap", icon: "📉" },
  { id: "roadmap", label: "Roadmap", icon: "🗺️" },
  { id: "simulator", label: "Simulator", icon: "🧪" },
  { id: "chat", label: "Career chat", icon: "💬" },
  { id: "recruiter", label: "Recruiter", icon: "🧑‍💼" },
  { id: "performance", label: "Model performance", icon: "📊" },
];

export default function App() {
  const { apiOnline, error } = useApp();
  const [page, setPage] = useState("landing");

  if (page === "landing") return <Landing go={setPage} />;

  const Page = PAGES[page] || Dashboard;
  return (
    <div style={{ display: "flex", minHeight: "100vh", background: "#0b1020", color: "#e8ecff", fontFamily: "Inter,system-ui,sans-serif" }}>
      <Sidebar items={SIDE} active={page} onSelect={setPage} />
      <div style={{ flex: 1, minWidth: 0 }}>
        <Navbar apiOnline={apiOnline} />
        <main style={{ display: "grid", gap: 18, padding: 24, maxWidth: 1000 }}>
          {error && (
            <div style={{ padding: 14, borderRadius: 12, background: "#3a1420", border: "1px solid #ff5d73" }}>
              ⚠️ {error}
            </div>
          )}
          <Page go={setPage} />
        </main>
      </div>
    </div>
  );
}