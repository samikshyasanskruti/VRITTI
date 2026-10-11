const COLORS = {
  good:    { bg: "#12382c", fg: "#2ecc8f" },
  warn:    { bg: "#3d3114", fg: "#f5b942" },
  bad:     { bg: "#3a1420", fg: "#ff5d73" },
  info:    { bg: "#1d2750", fg: "#8fa0ff" },
  neutral: { bg: "#1b2344", fg: "#8d98c4" },
};

export default function Badge({ children, variant = "neutral", style }) {
  const c = COLORS[variant] || COLORS.neutral;
  return (
    <span
      style={{
        display: "inline-block",
        padding: "4px 10px",
        borderRadius: 99,
        fontSize: 12,
        fontWeight: 600,
        background: c.bg,
        color: c.fg,
        ...style,
      }}
    >
      {children}
    </span>
  );
}