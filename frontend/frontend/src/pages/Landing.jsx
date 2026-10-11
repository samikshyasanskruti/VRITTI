import Button from "../components/common/Button";

const STEPS = [
  ["📄", "Upload", "Add your resume as a PDF, DOCX or plain text."],
  ["🎯", "Match", "Internships are ranked by meaning, skills and evidence."],
  ["🚀", "Grow", "See your skill gaps and a plan to close them."],
];

export default function Landing({ go }) {
  return (
    <div style={{
      minHeight: "100vh", color: "#e8ecff", padding: "0 6vw 60px", fontFamily: "Inter,system-ui,sans-serif",
      background: "radial-gradient(1200px 600px at 50% -10%,#232d6b,#0b1020 60%)",
    }}>
      <nav style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "20px 0" }}>
        <strong style={{ fontSize: 20 }}>Career<span style={{ color: "#6c7bff" }}>Match</span> AI</strong>
        <Button variant="ghost" onClick={() => go("dashboard")}>Open app</Button>
      </nav>

      <section style={{ textAlign: "center", padding: "70px 0 50px" }}>
        <h1 style={{ fontSize: "clamp(32px,6vw,58px)", margin: 0, fontWeight: 800 }}>
          Find the right internship,{" "}
          <span style={{ background: "linear-gradient(90deg,#6c7bff,#b06cff)", WebkitBackgroundClip: "text", color: "transparent" }}>
            instantly.
          </span>
        </h1>
        <p style={{ color: "#8d98c4", maxWidth: 580, margin: "16px auto 28px", fontSize: 18 }}>
          Upload your resume and see which opportunities fit you, why they fit, and what to learn next.
        </p>
        <div style={{ display: "flex", gap: 12, justifyContent: "center", flexWrap: "wrap" }}>
          <Button onClick={() => go("upload")} style={{ padding: "14px 30px", fontSize: 16 }}>Upload resume</Button>
          <Button variant="ghost" onClick={() => go("recruiter")} style={{ padding: "14px 30px", fontSize: 16 }}>
            I'm a recruiter
          </Button>
        </div>
      </section>

      <section style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(240px,1fr))", gap: 18, maxWidth: 960, margin: "0 auto" }}>
        {STEPS.map(([icon, title, text], i) => (
          <div key={title} style={{ background: "#141b34", border: "1px solid #26305a", borderRadius: 18, padding: 24 }}>
            <div style={{ fontSize: 30 }}>{icon}</div>
            <h3 style={{ margin: "10px 0 6px" }}>{i + 1}. {title}</h3>
            <p style={{ margin: 0, color: "#8d98c4", fontSize: 14 }}>{text}</p>
          </div>
        ))}
      </section>
    </div>
  );
}