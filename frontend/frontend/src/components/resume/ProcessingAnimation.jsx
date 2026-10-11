import { useEffect, useState } from "react";
import Card from "../common/Card";

const STEPS = ["Reading your resume", "Extracting skills", "Detecting projects & domains", "Building your profile"];

export default function ProcessingAnimation({ active }) {
  const [step, setStep] = useState(0);

  useEffect(() => {
    if (!active) { setStep(0); return; }
    const t = setInterval(() => setStep((s) => Math.min(s + 1, STEPS.length - 1)), 1200);
    return () => clearInterval(t);
  }, [active]);

  if (!active) return null;
  return (
    <Card title="Analyzing…">
      <style>{`@keyframes cm-pulse{0%,100%{opacity:.4}50%{opacity:1}}`}</style>
      <div style={{ display: "grid", gap: 12 }}>
        {STEPS.map((s, i) => (
          <div key={s} style={{
            display: "flex", gap: 10, alignItems: "center",
            color: i <= step ? "#e8ecff" : "#5b6694",
            animation: i === step ? "cm-pulse 1.2s infinite" : "none",
          }}>
            <span>{i < step ? "✅" : i === step ? "⏳" : "○"}</span>{s}
          </div>
        ))}
      </div>
    </Card>
  );
}