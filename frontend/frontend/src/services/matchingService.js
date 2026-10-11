
import {
  DEMO,
  ENDPOINTS,
  post,
  delay,
  normalizeMatch,
} from "./api";
import { demoMatches } from "../data/demoMatches";

export async function findInternships({
  resumeId,
  resumeText,
  filters = {},
}) {
  const topK = Math.min(
    100,
    Math.max(1, Number(filters.topK) || 10)
  );

  if (DEMO) {
    await delay();

    const location = (filters.location || "").toLowerCase();

    return demoMatches
      .filter((item) =>
        !filters.level || item.level === filters.level
      )
      .filter((item) =>
        !filters.workType || item.workType === filters.workType
      )
      .filter((item) =>
        !location ||
        (item.location || "").toLowerCase().includes(location)
      )
      .slice(0, topK);
  }

  if (!resumeId) {
    throw new Error(
      "Please upload your resume before finding matches."
    );
  }

  const data = await post(
    ENDPOINTS.internships,
    undefined,
    {
      resume_id: resumeId,
      top_k: topK,
    }
  );

  let results = (data.matches || []).map(normalizeMatch);

  if (filters.location) {
    const location = filters.location.toLowerCase();

    results = results.filter((item) =>
      (item.location || "").toLowerCase().includes(location)
    );
  }

  return results;
}
