import { scoreColor } from "../../utils/helpers";

export default function MatchScore({ score = 0, size = 56 }) {
  return (
    <div style={{
      width: size, height: size, borderRadius: "50%", display: "grid", placeItems: "center", flexShrink: 0,
      background: `conic-gradient(${scoreColor(score)} ${score * 3.6}deg,#0e1430 0)`,
    }}>
      <div style={{
        width: size - 14, height: size - 14, borderRadius: "50%", background: "#141b34",
        display: "grid", placeItems: "center", fontSize: size / 4, fontWeight: 800,
      }}>
        {score}%
      </div>
    </div>
  );
}