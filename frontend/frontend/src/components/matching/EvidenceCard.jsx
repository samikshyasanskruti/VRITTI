import Card from "../common/Card";
import Badge from "../common/Badge";

export default function EvidenceCard({ score = 0, snippets = [] }) {
  return (
    <Card
      title="Evidence"
      subtitle="Parts of your resume that support this match"
      action={<Badge variant={score >= 60 ? "good" : "warn"}>{score}%</Badge>}
    >
      {snippets.length === 0 ? (
        <p style={{ color: "#8d98c4", margin: 0 }}>No supporting text returned by the backend.</p>
      ) : (
        <div style={{ display: "grid", gap: 10 }}>
          {snippets.map((s, i) => (
            <blockquote key={i} style={{
              margin: 0, padding: "10px 14px", fontSize: 14, color: "#c3cbf0",
              background: "#0e1430", borderLeft: "3px solid #6c7bff", borderRadius: 8,
            }}>
              {typeof s === "string" ? s : s.text}
            </blockquote>
          ))}
        </div>
      )}
    </Card>
  );
}