import { useApp } from "../context/AppContext";
import ResumeUploader from "../components/resume/ResumeUploader";
import ProcessingAnimation from "../components/resume/ProcessingAnimation";
import ResumePreview from "../components/resume/ResumePreview";
import SkillCloud from "../components/resume/SkillCloud";
import Button from "../components/common/Button";

export default function UploadResume({ go }) {
  const { analyzeResume, loading, resumeText, fileName, profile } = useApp();
  return (
    <>
      <h2 style={{ margin: 0 }}>Upload resume</h2>
      <ResumeUploader loading={loading} onSubmit={analyzeResume} />
      <ProcessingAnimation active={loading} />
      {!loading && <ResumePreview text={resumeText} fileName={fileName} />}
      {!loading && profile && (
        <>
          <SkillCloud skills={profile.skills} />
          <div style={{ display: "flex", gap: 10, justifyContent: "flex-end" }}>
            <Button variant="ghost" onClick={() => go("profile")}>View profile</Button>
            <Button onClick={() => go("opportunities")}>Find opportunities →</Button>
          </div>
        </>
      )}
    </>
  );
}