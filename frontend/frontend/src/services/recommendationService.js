import { DEMO, ENDPOINTS, post, delay, toList } from "./api";
import { demoMatches } from "../data/demoMatches";

// Works out the most common missing skills from a list of matches (no backend needed).
export function fromMatches(matches = [], limit = 8) {
  const map = {};
  matches.forEach((m) =>
    m.missing.forEach((skill) => {
      map[skill] = map[skill] || { skill, count: 0, jobs: [] };
      map[skill].count += 1;
      map[skill].jobs.push(m.title);
    })
  );
  return Object.values(map)
    .sort((a, b) => b.count - a.count)
    .slice(0, limit)
    .map((r) => {
      const share = r.count / matches.length;
      return {
        skill: r.skill,
        count: r.count,
        impact: share >= 0.6 ? "High" : share >= 0.3 ? "Medium" : "Low",
        reason: `Missing in ${r.count} of ${matches.length} matches`,
        jobs: r.jobs,
      };
    });
}

// Asks the backend for recommendations (optional).
export async function fetchRecommendations({ resumeText, topK = 8 }) {
  if (DEMO) {
    await delay();
    return fromMatches(demoMatches, topK);
  }
  const data = await post(ENDPOINTS.recommendations, { resume_text: resumeText, top_k: topK });
  return toList(data).map((r) =>
    typeof r === "string"
      ? { skill: r, count: 0, impact: "", reason: "", jobs: [] }
      : {
          skill: r.skill || r.name || "",
          count: r.count || 0,
          impact: r.impact || "",
          reason: r.reason || "",
          jobs: r.jobs || [],
        }
  );
}