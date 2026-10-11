
import { pct } from "../utils/helpers";

export const BASE_URL = (
  import.meta.env?.VITE_API_URL || "http://127.0.0.1:8000"
).replace(/\/+$/, "");

export const DEMO = import.meta.env?.VITE_DEMO === "true";

export const ENDPOINTS = {
  health: "/api/health",
  analyze: "/api/resume/upload",
  resumes: "/api/resume",
  internships: "/api/matching/run",
  candidates: "/api/recruiter/rank-candidates",
  jobs: "/api/jobs",
  recommendations: "/api/recommendations",
  roadmap: "/api/roadmap",
  simulator: "/api/simulator/what-if",
};

export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function request(path, options = {}) {
  let response;

  try {
    response = await fetch(`${BASE_URL}${path}`, options);
  } catch {
    throw new ApiError(
      "Cannot connect to the backend. Check that Uvicorn is running on port 8000.",
      0
    );
  }

  const raw = await response.text();
  let data;

  try {
    data = raw ? JSON.parse(raw) : null;
  } catch {
    data = raw;
  }

  if (!response.ok) {
    const detail =
      data?.detail ||
      data?.message ||
      (typeof data === "string" ? data : "");

    throw new ApiError(
      `Server returned ${response.status}${detail ? `: ${detail}` : ""}`,
      response.status
    );
  }

  return data;
}

export const get = (path, params = {}) => {
  const query = new URLSearchParams();

  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      query.set(key, String(value));
    }
  });

  const suffix = query.toString();
  return request(`${path}${suffix ? `?${suffix}` : ""}`);
};

export const post = (path, body, params = {}) => {
  const query = new URLSearchParams();

  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      query.set(key, String(value));
    }
  });

  const suffix = query.toString();
  const isForm = body instanceof FormData;
  const hasBody = body !== undefined && body !== null;

  return request(`${path}${suffix ? `?${suffix}` : ""}`, {
    method: "POST",
    headers: isForm || !hasBody
      ? undefined
      : { "Content-Type": "application/json" },
    body: !hasBody ? undefined : isForm ? body : JSON.stringify(body),
  });
};

export const delay = (ms = 600) =>
  new Promise((resolve) => setTimeout(resolve, ms));

export const toList = (data) =>
  Array.isArray(data)
    ? data
    : data?.results ||
      data?.matches ||
      data?.candidates ||
      data?.recommendations ||
      [];

export function normalizeMatch(result) {
  const percentage = (value) =>
    value == null ? 0 : pct(value);

  return {
    ...result,
    title:
      result.title ||
      result.job_title ||
      result.name ||
      result.candidate_name ||
      "Untitled",
    name:
      result.name ||
      result.candidate_name ||
      result.title ||
      "Candidate",
    company: result.company || result.organization || "",
    location: result.location || "",
    workType: result.work_type || result.workType || "",
    level: result.experience_level || result.level || "",
    score: percentage(
      result.final_score ?? result.score ?? result.match_score
    ),
    semantic: percentage(
      result.semantic_score ?? result.semantic
    ),
    skills: percentage(
      result.skill_score ?? result.skills_score
    ),
    evidence: percentage(
      result.evidence_score ?? result.evidence
    ),
    have: result.matched_skills || result.have_skills || [],
    missing:
      result.missing_skills ||
      result.skills_to_learn ||
      [],
    rec: result.recommendation || result.explanation || "",
    reasons: result.reasons || [],
    snippets:
      result.evidence_snippets ||
      result.evidence_texts ||
      [],
    snippet: result.snippet || result.summary || "",
    url:
      result.url ||
      result.link ||
      result.apply_url ||
      result.source_url ||
      "",
  };
}
