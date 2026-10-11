import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from "recharts";
import Card from "../common/Card";

const COLORS = ["#6c7bff", "#b06cff", "#2ecc8f", "#f5b942", "#ff7ab6", "#4cc9f0"];

export default function DomainChart({ domains = [] }) {
  return (
    <Card title="Domain strengths" subtitle="Where your profile fits best">
      {domains.length === 0 ? (
        <p style={{ color: "#8d98c4" }}>No domain data available.</p>
      ) : (
        <div style={{ width: "100%", height: 280 }}>
          <ResponsiveContainer>
            <PieChart>
              <Pie data={domains} dataKey="value" nameKey="name" innerRadius={60} outerRadius={95} paddingAngle={3}>
                {domains.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Pie>
              <Tooltip contentStyle={{ background: "#0e1430", border: "1px solid #26305a", borderRadius: 10 }} />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      )}
    </Card>
  );
}