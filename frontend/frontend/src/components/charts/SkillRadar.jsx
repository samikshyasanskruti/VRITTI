import {
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Legend, Tooltip, ResponsiveContainer,
} from "recharts";
import Card from "../common/Card";

export default function SkillRadar({ results = [] }) {
  const map = {};
  results.forEach((r) => {
    (r.have || r.matched_skills || []).forEach((s) => {
      map[s] = map[s] || { skill: s, Have: 0, Missing: 0 };
      map[s].Have += 1;
    });
    (r.missing || r.missing_skills || []).forEach((s) => {
      map[s] = map[s] || { skill: s, Have: 0, Missing: 0 };
      map[s].Missing += 1;
    });
  });
  const data = Object.values(map)
    .sort((a, b) => b.Have + b.Missing - (a.Have + a.Missing))
    .slice(0, 8);

  return (
    <Card title="Skill radar" subtitle="Skills you have vs. skills you are missing">
      {data.length < 3 ? (
        <p style={{ color: "#8d98c4" }}>Not enough skills detected to draw the radar (need at least 3).</p>
      ) : (
        <div style={{ width: "100%", height: 320 }}>
          <ResponsiveContainer>
            <RadarChart data={data}>
              <PolarGrid stroke="#26305a" />
              <PolarAngleAxis dataKey="skill" stroke="#8d98c4" tick={{ fontSize: 12 }} />
              <PolarRadiusAxis stroke="#26305a" />
              <Radar name="Have" dataKey="Have" stroke="#2ecc8f" fill="#2ecc8f" fillOpacity={0.35} />
              <Radar name="Missing" dataKey="Missing" stroke="#ff5d73" fill="#ff5d73" fillOpacity={0.3} />
              <Legend />
              <Tooltip contentStyle={{ background: "#0e1430", border: "1px solid #26305a", borderRadius: 10 }} />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      )}
    </Card>
  );
}