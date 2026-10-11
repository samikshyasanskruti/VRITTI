import Card from "../common/Card";

export default function WhyMatch({ match }) {
  if (!match) return null;
  // Uses backend reasons if given, otherwise builds simple statements from the scores.
  const reasons = match.reasons.length
    ? match.reasons
    : [
        match.skills >= 60 && `You already cover ${match.have.length} of the relevant skills.`,
        match.semantic >= 60 && "Your experience is close in meaning to this role's description.",
        match.evidence >= 60 && "Your projects back up your skills.",
        match.missing.length > 0 && `Learning ${match.missing.slice(0, 3).join(", ")} would raise your score.`,
      ].filter(Boolean);

  return (
    <Card title="Why this match?">
      {match.rec && <p style={{ marginTop: 0, color: "#c3cbf0" }}>{match.rec}</p>}
      <ul style={{ margin: 0, paddingLeft: 20, display: "grid", gap: 6, fontSize: 14 }}>
        {reasons.map((r, i) => <li key={i}>{r}</li>)}
      </ul>
    </Card>
  );
}