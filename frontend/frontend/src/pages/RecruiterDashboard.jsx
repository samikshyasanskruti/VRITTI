import { useState } from "react";
import { useApp } from "../context/AppContext";
import Card from "../components/common/Card";
import Button from "../components/common/Button";
import CandidateRanking from "../components/recruiter/CandidateRanking";
import CandidateTable from "../components/recruiter/CandidateTable";
import CandidateDetails from "../components/recruiter/CandidateDetails";

export default function RecruiterDashboard() {
  const { candidates, findCandidates, loading } = useApp();
  const [jd, setJd] = useState("");
  const [cand, setCand] = useState(null);

  return (
    <>
      <h2 style={{ margin: 0 }}>Recruiter dashboard</h2>
      <Card title="Job description" subtitle="Paste a job description to rank candidates">
        <textarea rows={7} value={jd} onChange={(e) => setJd(e.target.value)} placeholder="Paste the job description…"
          style={{ width: "100%", padding: 12, borderRadius: 12, font: "inherit",
            background: "#0e1430", color: "#e8ecff", border: "1px solid #26305a" }} />
        <div style={{ display: "flex", justifyContent: "flex-end", marginTop: 14 }}>
          <Button loading={loading} disabled={!jd.trim()} onClick={() => findCandidates(jd)}>Rank candidates</Button>
        </div>
      </Card>
      <CandidateRanking candidates={candidates} />
      <CandidateTable candidates={candidates} onSelect={setCand} />
      <CandidateDetails candidate={cand} onClose={() => setCand(null)} />
    </>
  );
}