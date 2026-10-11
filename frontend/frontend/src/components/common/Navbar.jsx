import Badge from "./Badge";

export default function Navbar({ title = "CareerMatch AI", apiOnline, onMenuClick }) {
  return (
    <header
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "14px 24px",
        borderBottom: "1px solid var(--line,#26305a)",
        background: "rgba(11,16,32,.8)",
        backdropFilter: "blur(8px)",
        position: "sticky",
        top: 0,
        zIndex: 50,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        {onMenuClick && (
          <button
            onClick={onMenuClick}
            aria-label="Menu"
            style={{ background: "none", border: 0, color: "#e8ecff", fontSize: 22, cursor: "pointer" }}
          >
            ☰
          </button>
        )}
        <strong style={{ fontSize: 18 }}>{title}</strong>
      </div>
      {apiOnline !== undefined && (
        <Badge variant={apiOnline ? "good" : "bad"}>
          ● {apiOnline ? "API online" : "API offline"}
        </Badge>
      )}
    </header>
  );
}