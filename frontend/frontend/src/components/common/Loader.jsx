export default function Loader({ text = "Loading…", size = 36 }) {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 12,
        padding: 30,
        color: "var(--mute,#8d98c4)",
      }}
    >
      <style>{`@keyframes cm-spin{to{transform:rotate(360deg)}}`}</style>
      <div
        style={{
          width: size,
          height: size,
          borderRadius: "50%",
          border: "3px solid #26305a",
          borderTopColor: "#6c7bff",
          animation: "cm-spin .8s linear infinite",
        }}
      />
      <span style={{ fontSize: 14 }}>{text}</span>
    </div>
  );
}