import Loader from "../common/Loader";
import InternshipCard from "./InternshipCard";

export default function OpportunityList({ items = [], loading, onSelect }) {
  if (loading) return <Loader text="Finding your best matches…" />;
  if (!items.length) {
    return <p style={{ color: "#8d98c4", textAlign: "center", padding: 24 }}>
      No matches yet. Upload your resume, then press “Find matches”.
    </p>;
  }
  return (
    <div style={{ display: "grid", gap: 14 }}>
      {[...items].sort((a, b) => b.score - a.score).map((it, i) => (
        <InternshipCard key={i} item={it} onSelect={onSelect} />
      ))}
    </div>
  );
}