import Card from "../common/Card";
import { skillName } from "../../utils/helpers";

const PALETTE = ["#6c7bff", "#b06cff", "#2ecc8f", "#f5b942", "#ff7ab6"];

export default function SkillCloud({ skills = [] }) {
  return (
    <Card title="Skill cloud" subtitle={`${skills.length} skills detected`}>
      <div style={{ display: "flex", flexWrap: "wrap", gap: "10px 14px", alignItems: "center" }}>
        {skills.map((s, i) => (
          <span key={i} style={{
            fontSize: 13 + ((i * 7) % 4) * 3, fontWeight: 600, color: PALETTE[i % PALETTE.length],
          }}>
            {skillName(s)}
          </span>
        ))}
        {!skills.length && <span style={{ color: "#8d98c4" }}>No skills detected yet.</span>}
      </div>
    </Card>
  );
}