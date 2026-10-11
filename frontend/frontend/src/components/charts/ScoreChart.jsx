import {
  BarChart, Bar, XAxis, YAxis, Tooltip, Legend, CartesianGrid, ResponsiveContainer,
} from "recharts";
import Card from "../common/Card";

const pct = (v) => { v = Number(v) || 0; return Math.round(v <= 1 ? v * 100 : v); };

export default function ScoreChart({ results = [] }) {
  const data = results.slice(0, 6).map((r) => ({
    name: (r.title || "Untitled").slice(0, 16),
    Semantic: pct(r.semantic ?? r.semantic_score),
    Skills: pct(r.skills ?? r.skill_score),
    Evidence: pct(r.evidence ?? r.evidence_score),
  }));

  return (
    <Card title="Score breakdown" subtitle="Why the top matches rank where they do">
      <div style={{ width: "100%", height: 300 }}>
        <ResponsiveContainer>
          <BarChart data={data}>
            <CartesianGrid stroke="#26305a" strokeDasharray="3 3" />
            <XAxis dataKey="name" stroke="#8d98c4" tick={{ fontSize: 12 }} />
            <YAxis domain={[0, 100]} stroke="#8d98c4" />
            <Tooltip contentStyle={{ background: "#0e1430", border: "1px solid #26305a", borderRadius: 10 }} />
            <Legend />
            <Bar dataKey="Semantic" fill="#6c7bff" radius={[6, 6, 0, 0]} />
            <Bar dataKey="Skills" fill="#b06cff" radius={[6, 6, 0, 0]} />
            <Bar dataKey="Evidence" fill="#2ecc8f" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}