import { BarChart, Bar, XAxis, YAxis, Tooltip, Cell, ResponsiveContainer } from "recharts";
import Card from "../common/Card";

export default function WhatIfChart({ current = 0, projected = 0 }) {
  const data = [
    { name: "Current", score: current, fill: "#6c7bff" },
    { name: "If you learn them", score: projected, fill: "#2ecc8f" },
  ];
  return (
    <Card title="What-if comparison">
      <div style={{ width: "100%", height: 240 }}>
        <ResponsiveContainer>
          <BarChart data={data}>
            <XAxis dataKey="name" stroke="#8d98c4" />
            <YAxis domain={[0, 100]} stroke="#8d98c4" />
            <Tooltip formatter={(v) => `${v}%`}
              contentStyle={{ background: "#0e1430", border: "1px solid #26305a", borderRadius: 10 }} />
            <Bar dataKey="score" radius={[8, 8, 0, 0]}>
              {data.map((d) => <Cell key={d.name} fill={d.fill} />)}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}