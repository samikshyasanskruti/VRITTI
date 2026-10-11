import Card from "../common/Card";
import Badge from "../common/Badge";
import { skillName } from "../../utils/helpers";

export default function SkillGapCard({ have = [], missing = [] }) {
  const group = (label, list, variant, mark) => (
    <div style={{ marginBottom: 14 }}>
      <div style={{ fontSize: 13, color: "#8d98c4", marginBottom: 8 }}>{label} ({list.length})</div>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
        {list.map((s, i) => <Badge key={i} variant={variant}>{mark} {skillName(s)}</Badge>)}
        {!list.length && <span style={{ color: "#5b6694", fontSize: 13 }}>None</span>}
      </div>
    </div>
  );
  return (
    <Card title="Skill gap">
      {group("You have", have, "good", "✓")}
      {group("To learn", missing, "bad", "+")}
    </Card>
  );
}