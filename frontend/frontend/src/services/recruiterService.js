import { DEMO, ENDPOINTS, post, delay, toList, normalizeMatch } from "./api";
import { demoCandidates } from "../data/demoCandidates";

export async function rankCandidates({ jobDescription, topK = 10 }) {
  if (DEMO) {
    await delay();
    return demoCandidates.slice(0, topK);
  }
  const data = await post(ENDPOINTS.candidates, { job_description: jobDescription, top_k: topK });
  return toList(data).map(normalizeMatch);
}