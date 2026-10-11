import Card from "../common/Card";
import { skillName } from "../../utils/helpers";

// Uses s.level (0-100) when the backend provides it; otherwise an ESTIMATE by list order.
export default function SkillBars({ skills = [], max = 8 }) {
  const rows = skills.slice(0, max).map((s, i) => ({
    name: skillName(s),
    level: typeof s === "object" && s.level != null ? Number(s.level) : Math.max(40, 92 - i * 7),
  }));
  return (
    <Card title="Top skills" subtitle="Levels are estimated unless your backend returns them">
      <div style={{ display: "grid", gap: 12 }}>
        {rows.map((r) => (
          <div key={r.name}>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: 13, marginBottom: 4 }}>
              <span>{r.name}</span><span style={{ color: "#8d98c4" }}>{r.level}%</span>
            </div>
            <div style={{ height: 10, background: "#0e1430", borderRadius: 99, overflow: "hidden" }}>
              <div style={{ width: `${r.level}%`, height: "100%", background: "linear-gradient(90deg,#6c7bff,#b06cff)" }} />
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}