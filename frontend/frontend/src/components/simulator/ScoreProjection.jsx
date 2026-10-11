import Card from "../common/Card";
import { scoreColor } from "../../utils/helpers";

// ESTIMATE: set this to the real weight of the skills score in your backend's final score.
export const SKILL_WEIGHT = 0.4;

export function projectScore(match, selectedCount) {
  const have = match.have.length;
  const total = have + match.missing.length;
  if (!total) return match.score;
  const oldSkill = (have / total) * 100;
  const newSkill = ((have + selectedCount) / total) * 100;
  return Math.min(100, Math.round(match.score + SKILL_WEIGHT * (newSkill - oldSkill)));
}

export default function ScoreProjection({ match, selectedCount }) {
  const projected = projectScore(match, selectedCount);
  const gain = projected - match.score;
  return (
    <Card title="Projected score">
      <div style={{ display: "flex", alignItems: "center", gap: 24, flexWrap: "wrap" }}>
        <div><div style={{ color: "#8d98c4", fontSize: 13 }}>Now</div>
          <div style={{ fontSize: 34, fontWeight: 800, color: scoreColor(match.score) }}>{match.score}%</div></div>
        <div style={{ fontSize: 28, color: "#8d98c4" }}>→</div>
        <div><div style={{ color: "#8d98c4", fontSize: 13 }}>After learning</div>
          <div style={{ fontSize: 34, fontWeight: 800, color: scoreColor(projected) }}>{projected}%</div></div>
        <div style={{ color: "#2ecc8f", fontWeight: 700 }}>{gain > 0 ? `+${gain} points` : "No change yet"}</div>
      </div>
      <p style={{ color: "#8d98c4", fontSize: 12, marginBottom: 0 }}>
        This is an estimate based on the skills weight, not a guarantee.
      </p>
    </Card>
  );
}