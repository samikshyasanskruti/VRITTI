import Card from "../common/Card";
import { scoreColor } from "../../utils/helpers";

export default function MatchScoreCard({ title, subtitle, score = 0 }) {
  const c = scoreColor(score);
  const label = score >= 70 ? "Strong match" : score >= 45 ? "Moderate match" : "Weak match";
  return (
    <Card>
      <div style={{ display: "flex", gap: 20, alignItems: "center" }}>
        <div style={{
          width: 96, height: 96, borderRadius: "50%", display: "grid", placeItems: "center", flexShrink: 0,
          background: `conic-gradient(${c} ${score * 3.6}deg,#0e1430 0)`,
        }}>
          <div style={{
            width: 76, height: 76, borderRadius: "50%", background: "#141b34",
            display: "grid", placeItems: "center", fontSize: 22, fontWeight: 800,
          }}>
            {score}%
          </div>
        </div>
        <div>
          <h3 style={{ margin: 0 }}>{title}</h3>
          {subtitle && <div style={{ color: "#8d98c4", fontSize: 14 }}>{subtitle}</div>}
          <div style={{ color: c, fontWeight: 700, marginTop: 6 }}>{label}</div>
        </div>
      </div>
    </Card>
  );
}