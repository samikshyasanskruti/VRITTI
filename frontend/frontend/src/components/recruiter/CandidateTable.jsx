import Card from "../common/Card";
import Badge from "../common/Badge";
import { scoreColor } from "../../utils/helpers";

const th = { textAlign: "left", padding: "10px 12px", color: "#8d98c4", fontSize: 12, fontWeight: 600 };
const td = { padding: "12px", borderTop: "1px solid #26305a", fontSize: 14 };

export default function CandidateTable({ candidates = [], onSelect }) {
  return (
    <Card title="Candidates">
      <div style={{ overflowX: "auto" }}>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr><th style={th}>#</th><th style={th}>Name</th><th style={th}>Score</th><th style={th}>Top skills</th><th style={th}></th></tr>
          </thead>
          <tbody>
            {candidates.map((c, i) => (
              <tr key={i}>
                <td style={td}>{i + 1}</td>
                <td style={td}><strong>{c.name}</strong></td>
                <td style={{ ...td, color: scoreColor(c.score), fontWeight: 700 }}>{c.score}%</td>
                <td style={td}>
                  <div style={{ display: "flex", gap: 6, flexWrap: "wrap" }}>
                    {c.have.slice(0, 3).map((s) => <Badge key={s} variant="good">{s}</Badge>)}
                  </div>
                </td>
                <td style={td}>
                  <button onClick={() => onSelect?.(c)}
                    style={{ background: "none", border: 0, color: "#8fa0ff", cursor: "pointer", fontWeight: 600 }}>
                    Details →
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {!candidates.length && <p style={{ color: "#8d98c4", textAlign: "center" }}>No candidates yet.</p>}
      </div>
    </Card>
  );
}