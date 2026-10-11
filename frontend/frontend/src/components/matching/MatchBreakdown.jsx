import Card from "../common/Card";
import { scoreColor } from "../../utils/helpers";

export default function MatchBreakdown({ match }) {
  if (!match) return null;
  const rows = [
    ["Semantic similarity", match.semantic, "How close the meaning of the texts is"],
    ["Skills overlap", match.skills, "Required skills you already have"],
    ["Evidence", match.evidence, "Proof of skills in projects and experience"],
  ];
  return (
    <Card title="Score breakdown">
      <div style={{ display: "grid", gap: 14 }}>
        {rows.map(([label, v, hint]) => (
          <div key={label}>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: 14 }}>
              <strong>{label}</strong><span>{v}%</span>
            </div>
            <div style={{ fontSize: 12, color: "#8d98c4", marginBottom: 5 }}>{hint}</div>
            <div style={{ height: 10, background: "#0e1430", borderRadius: 99, overflow: "hidden" }}>
              <div style={{ width: `${v}%`, height: "100%", background: scoreColor(v), transition: "width .8s" }} />
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}