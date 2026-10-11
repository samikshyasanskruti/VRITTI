import Modal from "../common/Modal";
import MatchBreakdown from "../matching/MatchBreakdown";
import SkillGapCard from "../matching/SkillGapCard";

export default function CandidateDetails({ candidate, onClose }) {
  return (
    <Modal open={!!candidate} onClose={onClose} title={candidate?.name} width={620}>
      {candidate && (
        <div style={{ display: "grid", gap: 14 }}>
          <div style={{ fontSize: 28, fontWeight: 800 }}>{candidate.score}% match</div>
          {candidate.snippet && <p style={{ margin: 0, color: "#c3cbf0" }}>{candidate.snippet}</p>}
          <MatchBreakdown match={candidate} />
          <SkillGapCard have={candidate.have} missing={candidate.missing} />
        </div>
      )}
    </Modal>
  );
}