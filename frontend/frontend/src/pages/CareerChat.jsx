import { useEffect, useRef, useState } from "react";
import { useApp } from "../context/AppContext";
import Card from "../components/common/Card";
import Button from "../components/common/Button";

const SUGGESTIONS = [
  "Which skills should I learn first?",
  "How can I improve my resume?",
  "What roles fit my profile?",
];

export default function CareerChat() {
  const { messages, sendChat, chatLoading } = useApp();
  const [text, setText] = useState("");
  const end = useRef(null);

  useEffect(() => { end.current?.scrollIntoView({ behavior: "smooth" }); }, [messages, chatLoading]);

  const send = (t) => {
    const msg = (t ?? text).trim();
    if (!msg || chatLoading) return;
    setText("");
    sendChat(msg);
  };

  return (
    <>
      <h2 style={{ margin: 0 }}>Career chat</h2>
      <Card>
        <div style={{ height: 380, overflowY: "auto", display: "grid", gap: 10, alignContent: "start", paddingRight: 4 }}>
          {messages.map((m, i) => (
            <div key={i} style={{
              justifySelf: m.role === "user" ? "end" : "start", maxWidth: "80%", padding: "10px 14px",
              borderRadius: 14, fontSize: 14, whiteSpace: "pre-wrap",
              background: m.role === "user" ? "linear-gradient(90deg,#6c7bff,#b06cff)" : "#0e1430",
              border: m.role === "user" ? "none" : "1px solid #26305a",
            }}>
              {m.text}
            </div>
          ))}
          {chatLoading && <div style={{ color: "#8d98c4", fontSize: 13 }}>Typing…</div>}
          <div ref={end} />
        </div>

        <div style={{ display: "flex", flexWrap: "wrap", gap: 8, margin: "14px 0 10px" }}>
          {SUGGESTIONS.map((s) => (
            <button key={s} onClick={() => send(s)} style={{
              padding: "6px 12px", borderRadius: 99, border: "1px solid #26305a",
              background: "transparent", color: "#8d98c4", cursor: "pointer", fontSize: 12,
            }}>{s}</button>
          ))}
        </div>

        <div style={{ display: "flex", gap: 10 }}>
          <input value={text} onChange={(e) => setText(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && send()} placeholder="Ask about your career…"
            style={{ flex: 1, padding: 12, borderRadius: 12, font: "inherit",
              background: "#0e1430", color: "#e8ecff", border: "1px solid #26305a" }} />
          <Button onClick={() => send()} disabled={!text.trim() || chatLoading}>Send</Button>
        </div>
      </Card>
    </>
  );
}