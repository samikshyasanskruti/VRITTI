const DEFAULT_ITEMS = [
  { id: "dashboard", label: "Dashboard", icon: "🏠" },
  { id: "matching", label: "Matching", icon: "🎯" },
  { id: "opportunities", label: "Opportunities", icon: "💼" },
  { id: "profile", label: "Profile", icon: "👤" },
  { id: "recruiter", label: "Recruiter", icon: "🧑‍💼" },
];

export default function Sidebar({ items = DEFAULT_ITEMS, active, onSelect }) {
  return (
    <aside
      style={{
        width: 230,
        minHeight: "100vh",
        padding: 16,
        borderRight: "1px solid var(--line,#26305a)",
        background: "#0e1430",
      }}
    >
      <div style={{ fontWeight: 800, fontSize: 20, margin: "6px 10px 22px" }}>
        Career<span style={{ color: "#6c7bff" }}>Match</span>
      </div>
      <nav style={{ display: "grid", gap: 6 }}>
        {items.map((it) => {
          const on = it.id === active;
          return (
            <button
              key={it.id}
              onClick={() => onSelect?.(it.id)}
              style={{
                display: "flex",
                alignItems: "center",
                gap: 10,
                textAlign: "left",
                padding: "11px 14px",
                borderRadius: 12,
                border: 0,
                cursor: "pointer",
                fontSize: 15,
                color: on ? "#fff" : "#8d98c4",
                background: on ? "linear-gradient(90deg,#6c7bff,#b06cff)" : "transparent",
              }}
            >
              <span>{it.icon}</span>
              {it.label}
            </button>
          );
        })}
      </nav>
    </aside>
  );
}