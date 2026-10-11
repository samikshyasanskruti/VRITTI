import { useState } from "react";
import Card from "../common/Card";
import Button from "../common/Button";

export default function ResumeUploader({ onSubmit, loading }) {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [drag, setDrag] = useState(false);

  return (
    <Card title="Upload your resume" subtitle="PDF, DOCX or TXT, or paste the text">
      <label
        onDragOver={(e) => { e.preventDefault(); setDrag(true); }}
        onDragLeave={() => setDrag(false)}
        onDrop={(e) => { e.preventDefault(); setDrag(false); setFile(e.dataTransfer.files[0] || null); }}
        style={{
          display: "block", padding: 28, textAlign: "center", cursor: "pointer", borderRadius: 14,
          border: `2px dashed ${drag ? "#6c7bff" : "#26305a"}`, color: "#8d98c4",
        }}
      >
        {file ? `📎 ${file.name}` : "📄 Drag & drop a file here, or click to choose"}
        <input type="file" accept=".pdf,.docx,.txt" hidden onChange={(e) => setFile(e.target.files[0] || null)} />
      </label>
      <textarea
        rows={6}
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="…or paste your resume text here"
        style={{
          width: "100%", marginTop: 14, padding: 12, borderRadius: 12, font: "inherit",
          background: "#0e1430", color: "#e8ecff", border: "1px solid #26305a",
        }}
      />
      <div style={{ display: "flex", justifyContent: "flex-end", marginTop: 14 }}>
        <Button loading={loading} disabled={!file && !text.trim()} onClick={() => onSubmit({ text: text.trim(), file })}>
          Analyze resume
        </Button>
      </div>
    </Card>
  );
}