import Card from "../common/Card";
import Button from "../common/Button";

const field = {
  background: "#0e1430", color: "#e8ecff", border: "1px solid #26305a",
  borderRadius: 12, padding: 11, font: "inherit", width: "100%",
};

export default function OpportunityFilters({ filters, onChange, onApply, loading }) {
  const set = (k) => (e) => onChange({ ...filters, [k]: e.target.value });
  return (
    <Card title="Filters">
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(150px,1fr))", gap: 10 }}>
        <select style={field} value={filters.level} onChange={set("level")}>
          <option value="">Any experience</option><option>Entry</option><option>Mid</option><option>Senior</option>
        </select>
        <select style={field} value={filters.workType} onChange={set("workType")}>
          <option value="">Any work type</option><option>Remote</option><option>Hybrid</option><option>Onsite</option>
        </select>
        <input style={field} placeholder="Location" value={filters.location} onChange={set("location")} />
        <select style={field} value={filters.topK} onChange={set("topK")}>
          <option value={5}>Top 5</option><option value={10}>Top 10</option><option value={20}>Top 20</option>
        </select>
      </div>
      <div style={{ display: "flex", justifyContent: "flex-end", marginTop: 14 }}>
        <Button loading={loading} onClick={onApply}>Find matches</Button>
      </div>
    </Card>
  );
}