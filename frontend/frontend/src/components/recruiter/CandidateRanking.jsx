import { BarChart, Bar, XAxis, YAxis, Tooltip, Cell, ResponsiveContainer } from "recharts";
import Card from "../common/Card";
import { scoreColor } from "../../utils/helpers";

export default function CandidateRanking({ candidates = [] }) {
  if (!candidates.length) return null;
  const data = candidates.map((c) => ({ name: c.name, score: c.score }));
  return (
    <Card title="Candidate ranking" subtitle="Best fit for this job description">
      <div style={{ width: "100%", height: Math.max(200, data.length * 38) }}>
        <ResponsiveContainer>
          <BarChart data={data} layout="vertical" margin={{ left: 10, right: 20 }}>
            <XAxis type="number" domain={[0, 100]} stroke="#8d98c4" />
            <YAxis type="category" dataKey="name" width={130} stroke="#8d98c4" tick={{ fontSize: 12 }} />
            <Tooltip formatter={(v) => `${v}%`}
              contentStyle={{ background: "#0e1430", border: "1px solid #26305a", borderRadius: 10 }} />
            <Bar dataKey="score" radius={[0, 8, 8, 0]}>
              {data.map((d, i) => <Cell key={i} fill={scoreColor(d.score)} />)}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}