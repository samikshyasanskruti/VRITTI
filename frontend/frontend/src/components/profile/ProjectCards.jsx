import Card from "../common/Card";
import Badge from "../common/Badge";

export default function ProjectCards({ projects = [] }) {
  return (
    <Card title="Projects">
      {projects.length === 0 && <p style={{ color: "#8d98c4" }}>No projects detected.</p>}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(240px,1fr))", gap: 14 }}>
        {projects.map((p, i) => {
          const proj = typeof p === "string" ? { title: p } : p;
          return (
            <div key={i} style={{ background: "#0e1430", border: "1px solid #26305a", borderRadius: 14, padding: 16 }}>
              <strong>{proj.title || proj.name || `Project ${i + 1}`}</strong>
              {proj.description && (
                <p style={{ margin: "6px 0 10px", fontSize: 13, color: "#8d98c4" }}>{proj.description}</p>
              )}
              <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginTop: 8 }}>
                {(proj.tech || []).map((t) => <Badge key={t} variant="info">{t}</Badge>)}
              </div>
            </div>
          );
        })}
      </div>
    </Card>
  );
}