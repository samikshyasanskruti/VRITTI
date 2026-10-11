import Card from "../common/Card";
import Badge from "../common/Badge";

export default function ResumePreview({ text, fileName }) {
  if (!text) return null;
  return (
    <Card title="Resume preview" action={fileName ? <Badge variant="info">{fileName}</Badge> : null}>
      <pre style={{
        margin: 0, maxHeight: 280, overflow: "auto", whiteSpace: "pre-wrap", fontFamily: "inherit",
        fontSize: 13, lineHeight: 1.6, color: "#c3cbf0", background: "#0e1430", padding: 14, borderRadius: 12,
      }}>
        {text.slice(0, 2500)}{text.length > 2500 ? "\n…" : ""}
      </pre>
    </Card>
  );
}