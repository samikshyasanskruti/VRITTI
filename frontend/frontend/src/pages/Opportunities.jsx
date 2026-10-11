import { useApp } from "../context/AppContext";
import OpportunityFilters from "../components/opportunities/OpportunityFilters";
import OpportunityList from "../components/opportunities/OpportunityList";
import MatchChart from "../components/charts/MatchChart";
import ScoreChart from "../components/charts/ScoreChart";
import Card from "../components/common/Card";
import Button from "../components/common/Button";

export default function Opportunities({ go }) {
  const { filters, setFilters, findInternships, results, loading, resumeText, setSelected } = useApp();

  if (!resumeText) {
    return (
      <Card title="Opportunities" subtitle="Upload your resume first so we can match it">
        <Button onClick={() => go("upload")}>Upload resume</Button>
      </Card>
    );
  }
  return (
    <>
      <h2 style={{ margin: 0 }}>Opportunities</h2>
      <OpportunityFilters filters={filters} onChange={setFilters} onApply={findInternships} loading={loading} />
      {results.length > 0 && !loading && (
        <>
          <MatchChart results={results} />
          <ScoreChart results={results} />
        </>
      )}
      <OpportunityList items={results} loading={loading} onSelect={(m) => { setSelected(m); go("matching"); }} />
    </>
  );
}