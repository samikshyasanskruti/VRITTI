import React,{useState} from "react";import {Link} from "react-router-dom";import {ArrowRight,BrainCircuit,RefreshCw,Target} from "lucide-react";import {useApp} from "../context/AppContext.jsx";import {useMatching} from "../hooks/useMatching.js";
export default function MatchDetails(){const {matches,setMatches,activeResumeId}=useApp();const {run,loading,error,setError}=useMatching();const [summary,setSummary]=useState(null);async function calculate(){try{const r=await run(30);setMatches(r.matches||[]);setSummary(r)}catch{}}return <><div className="page-heading"><div><div className="eyebrow">EXPLAINABLE MATCHING</div><h1>Understand your fit.</h1><p className="page-subtitle">Rankings are generated from your resume, FAISS semantic retrieval and required-skill coverage. Scores represent alignment, not hiring probability.</p></div><button className="btn btn-primary" disabled={!activeResumeId||loading} onClick={calculate}><RefreshCw size={14}/>{loading?"Analyzing…":"Run matching"}</button></div>{!activeResumeId&&<div className="alert alert-info" style={{marginBottom:16}}>Upload a resume before running the matching pipeline. <Link to="/upload"><b>Upload resume →</b></Link></div>}{error&&<div className="alert" style={{marginBottom:16}}>{error}</div>}{summary&&<div className="alert alert-success" style={{marginBottom:16}}>Ranked {summary.count} results from a semantic shortlist of {summary.candidate_shortlist_count} postings. {summary.retrieval}. <strong>{summary.score_note}</strong></div>}{matches.length?<div className="grid" style={{gap:12}}>{matches.map((m,i)=><article className="card card-pad" key={m.job_id||i}><div style={{display:"flex",gap:16,alignItems:"flex-start"}}><div className="score-ring" style={{"--score":`${Math.min(100,Math.max(0,Number(m.score)||0))}%`}}><span>{Math.round(Number(m.score)||0}</span></div><div style={{flex:1,minWidth:0}}><div style={{display:"flex",justifyContent:"space-between",gap:10,flexWrap:"wrap"}}><div><span className="badge badge-gray">RANK #{i+1}</span><h2 style={{marginTop:8}}>{m.title||"Untitled posting"}</h2><p className="muted small">{m.company||"Company not supplied"} · {m.location||"Location not supplied"}</p></div><Link className="btn btn-secondary" to={`/skill-gap?job=${m.job_id}`}>Explore skill gap <ArrowRight size={14}/></Link></div><p className="muted small" style={{lineHeight:1.7}}>{m.explanation||"The matching API did not return a written explanation."}</p><div className="grid grid-3"><Mini label="Semantic similarity" value={`${Number(m.semantic_similarity||0).toFixed(1)}%`}/><Mini label="Required skills matched" value={`${(m.matched_skills||[]).length}`}/><Mini label="Missing required skills" value={`${(m.missing_skills||[]).length}`}/></div>{m.matched_skills?.length>0&&<div style={{marginTop:13}}><div className="muted small" style={{marginBottom:7}}>Matched skills</div><div className="skill-list">{m.matched_skills.map(s=><span className="skill-chip matched" key={s}>{s}</span>)}</div></div>}{m.missing_skills?.length>0&&<div style={{marginTop:12}}><div className="muted small" style={{marginBottom:7}}>Skills to strengthen</div><div className="skill-list">{m.missing_skills.map(s=><span className="skill-chip missing" key={s}>{s}</span>)}</div></div>}</div></div></article>)}</div>:<div className="card empty-state"><div className="empty-icon"><BrainCircuit size={24}/></div><h3>No match analysis yet</h3><p>Run the live matching API to retrieve postings from the Sentence Transformers + FAISS pipeline. If the index is missing, build it on the backend first.</p><button className="btn btn-primary" onClick={calculate} disabled={!activeResumeId||loading}><Target size={15}/> {loading?"Analyzing…":"Calculate matches"}</button></div>}</>}
function Mini({label,value}){return <div style={{padding:12,background:"#f8f9fc",borderRadius:9}}><div className="muted small">{label}</div><strong style={{display:"block",fontSize:17,marginTop:6}}>{value}</strong></div>}
import { useApp } from "../context/AppContext";
import MatchScoreCard from "../components/matching/MatchScoreCard";
import WhyMatch from "../components/matching/WhyMatch";
import MatchBreakdown from "../components/matching/MatchBreakdown";
import SkillGapCard from "../components/matching/SkillGapCard";
import EvidenceCard from "../components/matching/EvidenceCard";
import Card from "../components/common/Card";
import Button from "../components/common/Button";

export default function MatchDetails({ go }) {
  const { selected: m } = useApp();
  if (!m) {
    return (
      <Card title="Match details" subtitle="Choose an opportunity to see why it matches">
        <Button onClick={() => go("opportunities")}>Browse opportunities</Button>
      </Card>
    );
  }
  return (
    <>
      <MatchScoreCard title={m.title} subtitle={[m.company, m.location].filter(Boolean).join(" · ")} score={m.score} />
      <WhyMatch match={m} />
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(320px,1fr))", gap: 18 }}>
        <MatchBreakdown match={m} />
        <SkillGapCard have={m.have} missing={m.missing} />
      </div>
      <EvidenceCard score={m.evidence} snippets={m.snippets} />
      <div style={{ display: "flex", gap: 10, justifyContent: "flex-end", flexWrap: "wrap" }}>
        {m.url && (
          <a href={m.url} target="_blank" rel="noopener noreferrer"
             style={{ alignSelf: "center", color: "#8fa0ff", fontWeight: 600, textDecoration: "none" }}>
            View posting →
          </a>
        )}
        <Button variant="ghost" onClick={() => go("roadmap")}>Learning roadmap</Button>
        <Button onClick={() => go("simulator")}>Try the simulator</Button>
      </div>
    </>
  );
}