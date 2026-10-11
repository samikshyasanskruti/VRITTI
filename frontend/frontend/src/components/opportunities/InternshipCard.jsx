import React from "react";
import {BriefcaseBusiness,MapPin} from "lucide-react";
export default function InternshipCard({job,match}){return <article className="card job-card"><div className="job-card-head"><span className="company-mark"><BriefcaseBusiness size={17}/></span><div><div className="job-title">{job.title}</div><div className="job-company">{job.company||"Company not supplied"}</div></div></div><div className="job-meta"><span><MapPin size={12}/>{job.location||"Location not supplied"}</span></div><p className="muted small">{job.description||"No description provided."}</p>{match&&<span className="badge badge-blue">{Math.round(match.score||0)}% alignment</span>}</article>}
import Card from "../common/Card";
import Badge from "../common/Badge";
import Button from "../common/Button";
import MatchScore from "./MatchScore";

export default function InternshipCard({ item, onSelect }) {
  return (
    <Card>
      <div style={{ display: "flex", gap: 16, alignItems: "flex-start" }}>
        <MatchScore score={item.score} />
        <div style={{ flex: 1 }}>
          <h3 style={{ margin: 0 }}>{item.title}</h3>
          <div style={{ color: "#8d98c4", fontSize: 14 }}>
            {[item.company, item.location].filter(Boolean).join(" · ")}
          </div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 6, margin: "10px 0" }}>
            {item.workType && <Badge variant="info">{item.workType}</Badge>}
            {item.level && <Badge variant="neutral">{item.level}</Badge>}
            {item.have.slice(0, 3).map((s) => <Badge key={s} variant="good">✓ {s}</Badge>)}
            {item.missing.slice(0, 3).map((s) => <Badge key={s} variant="bad">+ {s}</Badge>)}
          </div>
          <div style={{ display: "flex", gap: 10 }}>
            <Button onClick={() => onSelect?.(item)} style={{ padding: "8px 16px" }}>Why this match?</Button>
            {item.url && (
              <a href={item.url} target="_blank" rel="noopener noreferrer"
                 style={{ alignSelf: "center", color: "#8fa0ff", fontWeight: 600, textDecoration: "none" }}>
                View posting →
              </a>
            )}
          </div>
        </div>
      </div>
    </Card>
  );
}