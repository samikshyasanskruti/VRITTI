import {
  BarChart, Bar, XAxis, YAxis, Tooltip, Legend, CartesianGrid, ResponsiveContainer,
} from "recharts";
import Card from "../common/Card";
import Badge from "../common/Badge";

// Illustrative numbers shown only until real evaluation metrics are passed in.
const SAMPLE = [
  { method: "BM25", precision: 0.52, ndcg: 0.55 },
  { method: "Semantic", precision: 0.64, ndcg: 0.68 },
  { method: "Hybrid", precision: 0.73, ndcg: 0.77 },
];

export default function PerformanceChart({ metrics }) {
  const isSample = !metrics || metrics.length === 0;
  const data = (isSample ? SAMPLE : metrics).map((m) => ({
    method: m.method,
    "Precision@10": Number(m.precision),
    "nDCG@10": Number(m.ndcg),
  }));

  return (
    <Card
      title="Model performance"
      subtitle="Search methods compared on the evaluation set"
      action={isSample ? <Badge variant="warn">Sample data</Badge> : null}
    >
      <div style={{ width: "100%", height: 300 }}>
        <ResponsiveContainer>
          <BarChart data={data}>
            <CartesianGrid stroke="#26305a" strokeDasharray="3 3" />
            <XAxis dataKey="method" stroke="#8d98c4" />
            <YAxis domain={[0, 1]} stroke="#8d98c4" />
            <Tooltip contentStyle={{ background: "#0e1430", border: "1px solid #26305a", borderRadius: 10 }} />
            <Legend />
            <Bar dataKey="Precision@10" fill="#6c7bff" radius={[6, 6, 0, 0]} />
            <Bar dataKey="nDCG@10" fill="#b06cff" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}