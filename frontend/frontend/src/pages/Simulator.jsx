import { useState } from "react";
import { useApp } from "../context/AppContext";
import SkillSelector from "../components/simulator/SkillSelector";
import ScoreProjection, { projectScore } from "../components/simulator/ScoreProjection";
import WhatIfChart from "../components/simulator/WhatIfChart";
import Card from "../components/common/Card";
import Button from "../components/common/Button";

export default function Simulator({ go }) {
  const { selected } = useApp();
  const [chosen, setChosen] = useState([]);
  if (!selected) {
    return (
      <Card title="What-if simulator" subtitle="Choose an opportunity first">
        <Button onClick={() => go("opportunities")}>Browse opportunities</Button>
      </Card>
    );
  }
  const toggle = (s) => setChosen((c) => (c.includes(s) ? c.filter((x) => x !== s) : [...c, s]));
  return (
    <>
      <h2 style={{ margin: 0 }}>What-if simulator</h2>
      <p style={{ margin: 0, color: "#8d98c4" }}>For: {selected.title}</p>
      <SkillSelector missing={selected.missing} selected={chosen} onToggle={toggle} />
      <ScoreProjection match={selected} selectedCount={chosen.length} />
      <WhatIfChart current={selected.score} projected={projectScore(selected, chosen.length)} />
    </>
  );
}