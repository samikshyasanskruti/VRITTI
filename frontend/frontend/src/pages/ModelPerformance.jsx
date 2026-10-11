import { useEffect } from "react";
import { useApp } from "../context/AppContext";
import PerformanceChart from "../components/charts/PerformanceChart";
import Card from "../components/common/Card";

export default function ModelPerformance() {
  const { metrics, loadMetrics } = useApp();
  useEffect(() => { loadMetrics(); }, []);

  return (
    <>
      <h2 style={{ margin: 0 }}>Model performance</h2>
      <PerformanceChart metrics={metrics} />
      <Card title="How to read this">
        <ul style={{ margin: 0, paddingLeft: 20, display: "grid", gap: 8, fontSize: 14, color: "#c3cbf0" }}>
          <li><strong>Precision@10:</strong> the share of the top 10 results that are actually relevant.</li>
          <li><strong>nDCG@10:</strong> like precision, but it rewards putting the most relevant results higher up.</li>
          <li><strong>BM25</strong> matches keywords, <strong>Semantic</strong> matches meaning, and <strong>Hybrid</strong> combines both.</li>
        </ul>
        {!metrics && (
          <p style={{ color: "#f5b942", fontSize: 13, marginBottom: 0 }}>
            No evaluation results found, so the chart shows sample numbers. Run{" "}
            <code>python scripts/05_evaluate.py</code> in the backend to get real ones.
          </p>
        )}
      </Card>
    </>
  );
}