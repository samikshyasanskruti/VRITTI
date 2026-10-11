import { useApp } from "../context/AppContext";
import ProfileHeader from "../components/profile/ProfileHeader";
import SkillBars from "../components/profile/SkillBars";
import DomainChart from "../components/profile/DomainChart";
import ProjectCards from "../components/profile/ProjectCards";
import Card from "../components/common/Card";
import Button from "../components/common/Button";

export default function CareerProfile({ go }) {
  const { profile } = useApp();
  if (!profile) {
    return (
      <Card title="Career profile" subtitle="No profile yet">
        <Button onClick={() => go("upload")}>Upload your resume</Button>
      </Card>
    );
  }
  return (
    <>
      <ProfileHeader profile={profile} />
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(340px,1fr))", gap: 18 }}>
        <SkillBars skills={profile.skills} />
        <DomainChart domains={profile.domains} />
      </div>
      <ProjectCards projects={profile.projects} />
    </>
  );
}