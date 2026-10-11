import Card from "../common/Card";
import { skillName } from "../../utils/helpers";

export default function SkillSelector({ missing = [], selected = [], onToggle }) {
  return (
    <Card title="Pick skills to learn" subtitle="Select skills to see how your score could change">
      <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
        {missing.map((s) => {
          const name = skillName(s);
          const on = selected.includes(name);
          return (
            <button key={name} onClick={() => onToggle(name)} style={{
              padding: "8px 14px", borderRadius: 99, cursor: "pointer", fontSize: 13, fontWeight: 600,
              border: `1px solid ${on ? "#2ecc8f" : "#26305a"}`,
              background: on ? "#12382c" : "transparent", color: on ? "#2ecc8f" : "#8d98c4",
            }}>
              {on ? "✓ " : "+ "}{name}
            </button>
          );
        })}
        {!missing.length && <span style={{ color: "#8d98c4" }}>No missing skills for this match.</span>}
      </div>
    </Card>
  );
}