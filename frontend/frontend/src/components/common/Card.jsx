export default function Card({ title, subtitle, action, children, style }) {
  return (
    <section
      style={{
        background: "var(--card,#141b34)",
        border: "1px solid var(--line,#26305a)",
        borderRadius: 18,
        padding: 22,
        boxShadow: "0 10px 40px #0006",
        ...style,
      }}
    >
      {(title || action) && (
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "flex-start",
            gap: 12,
            marginBottom: 14,
          }}
        >
          <div>
            <h3 style={{ margin: 0, fontSize: 18 }}>{title}</h3>
            {subtitle && (
              <p style={{ margin: "4px 0 0", fontSize: 13, color: "var(--mute,#8d98c4)" }}>
                {subtitle}
              </p>
            )}
          </div>
          {action}
        </div>
      )}
      {children}
    </section>
  );
}