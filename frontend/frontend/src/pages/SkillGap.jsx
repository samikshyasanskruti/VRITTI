import { useApp } from "../context/AppContext";
import Card from "../components/common/Card";
import Button from "../components/common/Button";
import SkillRadar from "../components/charts/SkillRadar";

export default function SkillGap({ go }) {
  const { results } = useApp();
  if (!results.length) {
    return (
      <Card title="Skill gap" subtitle="Run a search to see which skills you are missing most often">
        <Button onClick={() => go("opportunities")}>Find opportunities</Button>
      </Card>
    );
  }

  const counts = {};
  results.forEach((r) => r.missing.forEach((s) => { counts[s] = (counts[s] || 0) + 1; }));
  const rows = Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 10);

  return (
    <>
      <h2 style={{ margin: 0 }}>Skill gap</h2>
      <Card title="Most requested missing skills" subtitle={`Across your ${results.length} matches`}>
        {rows.length === 0 && <p style={{ color: "#8d98c4", margin: 0 }}>No missing skills found. Nice!</p>}
        <div style={{ display: "grid", gap: 12 }}>
          {rows.map(([skill, n]) => (
            <div key={skill}>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: 14, marginBottom: 4 }}>
                <strong>{skill}</strong><span style={{ color: "#8d98c4" }}>in {n} of {results.length}</span>
              </div>
              <div style={{ height: 10, background: "#0e1430", borderRadius: 99, overflow: "hidden" }}>
                <div style={{ width: `${(n / results.length) * 100}%`, height: "100%", background: "linear-gradient(90deg,#ff5d73,#f5b942)" }} />
              </div>
            </div>
          ))}
        </div>
      </Card>
      <SkillRadar results={results} />
    </>
  );
}