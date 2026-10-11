
import {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";

import { pct } from "../utils/helpers";

const CONFIG = {
  BASE_URL: (
    import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"
  ).replace(/\/+$/, ""),

  health: "/api/health",
  analyze: "/api/resume/upload",
  internships: "/api/matching/run",
  candidates: "/api/recruiter/rank-candidates",
  jobs: "/api/jobs",
};

const AppContext = createContext(null);

export const useApp = () => useContext(AppContext);

export function normalize(r) {
  return {
    ...r,
    title:
      r.title ||
      r.job_title ||
      r.name ||
      r.candidate_name ||
      "Untitled",

    name: r.name || r.candidate_name || r.title || "Candidate",
    company: r.company || r.organization || "",
    location: r.location || "",
    workType: r.work_type || r.workType || "",
    level: r.experience_level || r.level || "",

    score: pct(r.final_score ?? r.score ?? r.match_score),
    semantic: pct(r.semantic_score ?? r.semantic),
    skills: pct(r.skill_score ?? r.skills_score),
    evidence: pct(r.evidence_score ?? r.evidence),

    have: r.matched_skills || r.have_skills || [],
    missing: r.missing_skills || r.skills_to_learn || [],
    rec: r.recommendation || r.explanation || "",
    reasons: r.reasons || [],
    snippets: r.evidence_snippets || r.evidence_texts || [],
    snippet: r.snippet || r.summary || "",
    url: r.url || r.link || r.apply_url || r.source_url || "",
  };
}

async function request(path, options = {}) {
  let response;

  try {
    response = await fetch(`${CONFIG.BASE_URL}${path}`, options);
  } catch {
    throw new Error(
      "Cannot connect to the backend. Check that Uvicorn is running on port 8000."
    );
  }

  const raw = await response.text();
  let data;

  try {
    data = raw ? JSON.parse(raw) : {};
  } catch {
    data = { detail: raw };
  }

  if (!response.ok) {
    throw new Error(
      data.detail ||
      data.message ||
      `Server returned HTTP ${response.status}`
    );
  }

  return data;
}

async function post(path, body, query = {}) {
  const params = new URLSearchParams();

  Object.entries(query).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      params.set(key, String(value));
    }
  });

  const queryString = params.toString();
  const url = `${path}${queryString ? `?${queryString}` : ""}`;

  const isForm = body instanceof FormData;

  return request(url, {
    method: "POST",
    headers:
      body == null || isForm
        ? undefined
        : { "Content-Type": "application/json" },
    body:
      body == null
        ? undefined
        : isForm
          ? body
          : JSON.stringify(body),
  });
}

function toList(data) {
  const rows = Array.isArray(data)
    ? data
    : data.matches ||
      data.results ||
      data.candidates ||
      data.recommendations ||
      [];

  return rows.map(normalize);
}

export function AppProvider({ children }) {
  const [apiOnline, setApiOnline] = useState(undefined);

  const [resumeText, setResumeText] = useState("");
  const [resumeId, setResumeId] = useState(null);
  const [fileName, setFileName] = useState("");
  const [profile, setProfile] = useState(null);

  const [results, setResults] = useState([]);
  const [candidates, setCandidates] = useState([]);

  const [filters, setFilters] = useState({
    level: "",
    workType: "",
    location: "",
    topK: 10,
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    request("/api/health")
      .then(() => setApiOnline(true))
      .catch(() => setApiOnline(false));
  }, []);

  async function guarded(fn) {
    setLoading(true);
    setError("");

    try {
      return await fn();
    } catch (e) {
      setError(e.message || "An unexpected error occurred.");
      return null;
    } finally {
      setLoading(false);
    }
  }

  // Upload a resume file and save it in the backend database.
  const analyzeResume = ({ text = "", file = null }) =>
    guarded(async () => {
      if (!file) {
        throw new Error(
          "Please select a PDF, DOCX, or TXT resume. " +
          "Pasted text is not supported by the current upload endpoint."
        );
      }

      const form = new FormData();
      form.append("file", file);

      const data = await post(CONFIG.analyze, form);

      if (!data.resume_id) {
        throw new Error(
          "Upload response did not contain a resume_id."
        );
      }

      const extractedProfile = data.profile || {};
      const candidate = extractedProfile.candidate || {};

      setResumeId(data.resume_id);
      setResumeText(data.text_preview || text || "");
      setFileName(data.filename || file.name);

      const domains =
        extractedProfile.domains ||
        extractedProfile.domain_scores ||
        [];

      setProfile({
        name: candidate.name || "Your profile",
        email: candidate.email || "",
        skills: extractedProfile.skills || [],
        projects: extractedProfile.projects || [],
        domains: Array.isArray(domains)
          ? domains
          : Object.entries(domains).map(([name, value]) => ({
              name,
              value: pct(value),
            })),
      });

      setResults([]);

      return data;
    });

  // Match the saved resume against the existing real job dataset.
  const findInternships = () =>
    guarded(async () => {
      if (!resumeId) {
        throw new Error(
          "Upload your resume first, then click Find Matches."
        );
      }

      const topK = Math.min(
        100,
        Math.max(1, Number(filters.topK) || 10)
      );

      const data = await post(
        CONFIG.internships,
        null,
        {
          resume_id: resumeId,
          top_k: topK,
        }
      );

      let matches = toList(data);

      if (filters.location) {
        const location = filters.location.toLowerCase();

        matches = matches.filter((item) =>
          (item.location || "").toLowerCase().includes(location)
        );
      }

      setResults(matches);

      return data;
    });

  // Recruiter ranking requires an existing job_id.
  const findCandidates = (jobId) =>
    guarded(async () => {
      if (!jobId || !Number.isInteger(Number(jobId))) {
        throw new Error(
          "Recruiter ranking requires an existing numeric job ID. " +
          "Load jobs from GET /api/jobs and select a job first."
        );
      }

      const data = await post(CONFIG.candidates, {
        job_id: Number(jobId),
        top_k: 10,
      });

      setCandidates(toList(data));

      return data;
    });

  return (
    <AppContext.Provider
      value={{
        apiOnline,
        resumeText,
        resumeId,
        fileName,
        profile,
        results,
        candidates,
        filters,
        setFilters,
        loading,
        error,
        setError,
        analyzeResume,
        findInternships,
        findCandidates,
      }}
    >
      {children}
    </AppContext.Provider>
  );
}
