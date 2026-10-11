import { BarChart, Bar, XAxis, YAxis, Tooltip, Cell, ResponsiveContainer } from "recharts";
import Card from "../common/Card";

const pct = (v) => { v = Number(v) || 0; return Math.round(v <= 1 ? v * 100 : v); };
const color = (p) => (p >= 70 ? "#2ecc8f" : p >= 45 ? "#f5b942" : "#ff5d73");

export default function MatchChart({ results = [] }) {
  const data = results.map((r) => ({
    name: r.title || r.name || "Untitled",
    score: pct(r.score ?? r.final_score),
  }));

  return (
    <Card title="Match ranking" subtitle="Final score for each result">
      <div style={{ width: "100%", height: Math.max(220, data.length * 38) }}>
        <ResponsiveContainer>
          <BarChart data={data} layout="vertical" margin={{ left: 10, right: 20 }}>
            <XAxis type="number" domain={[0, 100]} stroke="#8d98c4" />
            <YAxis type="category" dataKey="name" width={150} stroke="#8d98c4" tick={{ fontSize: 12 }} />
            <Tooltip
              formatter={(v) => `${v}%`}
              contentStyle={{ background: "#0e1430", border: "1px solid #26305a", borderRadius: 10 }}
            />
            <Bar dataKey="score" radius={[0, 8, 8, 0]}>
              {data.map((d, i) => <Cell key={i} fill={color(d.score)} />)}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}