import { useApp } from "../context/AppContext";
import Card from "../components/common/Card";
import Button from "../components/common/Button";
import MatchScore from "../components/opportunities/MatchScore";
import MatchChart from "../components/charts/MatchChart";

function Stat({ label, value, icon }) {
  return (
    <div style={{ background: "#141b34", border: "1px solid #26305a", borderRadius: 16, padding: 18 }}>
      <div style={{ fontSize: 22 }}>{icon}</div>
      <div style={{ fontSize: 30, fontWeight: 800 }}>{value}</div>
      <div style={{ color: "#8d98c4", fontSize: 13 }}>{label}</div>
    </div>
  );
}

export default function Dashboard({ go }) {
  const { profile, results, setSelected } = useApp();
  const best = results.length ? Math.max(...results.map((r) => r.score)) : "–";
  const gaps = new Set(results.flatMap((r) => r.missing)).size;
  const top = [...results].sort((a, b) => b.score - a.score).slice(0, 3);

  return (
    <>
      <h2 style={{ margin: 0 }}>Dashboard</h2>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(180px,1fr))", gap: 14 }}>
        <Stat icon="🧠" label="Skills detected" value={profile ? profile.skills.length : "–"} />
        <Stat icon="💼" label="Matches found" value={results.length || "–"} />
        <Stat icon="🏆" label="Best score" value={best === "–" ? best : `${best}%`} />
        <Stat icon="📚" label="Skills to learn" value={results.length ? gaps : "–"} />
      </div>

      {!profile && (
        <Card title="Get started" subtitle="Upload your resume to unlock matches and insights">
          <Button onClick={() => go("upload")}>Upload resume</Button>
        </Card>
      )}

      {top.length > 0 && (
        <Card title="Top matches">
          <div style={{ display: "grid", gap: 12 }}>
            {top.map((m, i) => (
              <div key={i} style={{ display: "flex", alignItems: "center", gap: 14 }}>
                <MatchScore score={m.score} size={48} />
                <div style={{ flex: 1 }}>
                  <strong>{m.title}</strong>
                  <div style={{ color: "#8d98c4", fontSize: 13 }}>{m.company}</div>
                </div>
                <Button variant="ghost" style={{ padding: "7px 14px" }}
                  onClick={() => { setSelected(m); go("matching"); }}>Details</Button>
              </div>
            ))}
          </div>
        </Card>
      )}
      {results.length > 0 && <MatchChart results={results} />}
    </>
  );
}