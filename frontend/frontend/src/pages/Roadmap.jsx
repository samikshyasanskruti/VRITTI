import { useState } from "react";
import { useApp } from "../context/AppContext";
import Card from "../components/common/Card";
import Button from "../components/common/Button";

export default function Roadmap({ go }) {
  const { selected, results } = useApp();
  const [done, setDone] = useState({});

  // Use the selected match's gaps; otherwise the most common gaps across all matches.
  let skills = selected?.missing || [];
  if (!skills.length) {
    const counts = {};
    results.forEach((r) => r.missing.forEach((s) => { counts[s] = (counts[s] || 0) + 1; }));
    skills = Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 5).map(([s]) => s);
  }
  if (!skills.length) {
    return (
      <Card title="Learning roadmap" subtitle="Find opportunities first so we know which skills to plan for">
        <Button onClick={() => go("opportunities")}>Find opportunities</Button>
      </Card>
    );
  }

  const tasks = skills.flatMap((s) => [
    { id: `${s}-1`, skill: s, text: `Learn the basics of ${s}` },
    { id: `${s}-2`, skill: s, text: `Build a small project using ${s}` },
    { id: `${s}-3`, skill: s, text: `Add ${s} and the project to your resume` },
  ]);
  const count = tasks.filter((t) => done[t.id]).length;
  const progress = Math.round((count / tasks.length) * 100);

  return (
    <>
      <h2 style={{ margin: 0 }}>Learning roadmap</h2>
      <Card title="Your progress" subtitle={selected ? `Plan for ${selected.title}` : "Plan for your most common gaps"}>
        <div style={{ height: 12, background: "#0e1430", borderRadius: 99, overflow: "hidden" }}>
          <div style={{ width: `${progress}%`, height: "100%", background: "linear-gradient(90deg,#6c7bff,#2ecc8f)", transition: "width .4s" }} />
        </div>
        <div style={{ color: "#8d98c4", fontSize: 13, marginTop: 6 }}>{count} of {tasks.length} steps done ({progress}%)</div>
      </Card>

      {skills.map((s, i) => (
        <Card key={s} title={`${i + 1}. ${s}`}>
          <div style={{ display: "grid", gap: 10 }}>
            {tasks.filter((t) => t.skill === s).map((t) => (
              <label key={t.id} style={{ display: "flex", gap: 10, alignItems: "center", cursor: "pointer",
                color: done[t.id] ? "#5b6694" : "#e8ecff", textDecoration: done[t.id] ? "line-through" : "none" }}>
                <input type="checkbox" checked={!!done[t.id]}
                  onChange={() => setDone((d) => ({ ...d, [t.id]: !d[t.id] }))} />
                {t.text}
              </label>
            ))}
          </div>
        </Card>
      ))}
    </>
  );
}