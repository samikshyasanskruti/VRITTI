export default function Button({
  children,
  variant = "primary",
  loading = false,
  disabled = false,
  onClick,
  type = "button",
  style,
}) {
  const primary = variant === "primary";
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      style={{
        border: primary ? "none" : "1px solid var(--line,#26305a)",
        borderRadius: 12,
        padding: "11px 24px",
        fontWeight: 700,
        fontSize: 14,
        cursor: disabled || loading ? "not-allowed" : "pointer",
        opacity: disabled || loading ? 0.6 : 1,
        color: primary ? "#fff" : "var(--mute,#8d98c4)",
        background: primary
          ? "linear-gradient(90deg,#6c7bff,#b06cff)"
          : "transparent",
        ...style,
      }}
    >
      {loading ? "Please wait…" : children}
    </button>
  );
}