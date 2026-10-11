import Card from "../common/Card";
import Badge from "../common/Badge";
import { initials } from "../../utils/helpers";

export default function ProfileHeader({ profile }) {
  if (!profile) return null;
  return (
    <Card>
      <div style={{ display: "flex", gap: 18, alignItems: "center", flexWrap: "wrap" }}>
        <div style={{
          width: 72, height: 72, borderRadius: "50%", display: "grid", placeItems: "center",
          fontSize: 26, fontWeight: 800, background: "linear-gradient(135deg,#6c7bff,#b06cff)",
        }}>
          {initials(profile.name)}
        </div>
        <div>
          <h2 style={{ margin: 0 }}>{profile.name}</h2>
          {profile.email && <div style={{ color: "#8d98c4", fontSize: 14 }}>{profile.email}</div>}
          <div style={{ display: "flex", gap: 8, marginTop: 8 }}>
            <Badge variant="info">{profile.skills.length} skills</Badge>
            <Badge variant="neutral">{profile.projects.length} projects</Badge>
          </div>
        </div>
      </div>
    </Card>
  );
}