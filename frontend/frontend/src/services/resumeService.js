
import { DEMO, ENDPOINTS, post, delay } from "./api";
import { demoProfile } from "../data/demoMatches";

export async function analyzeResume({ text = "", file = null }) {
  if (DEMO) {
    await delay(500);
    return {
      ...demoProfile,
      text: text || demoProfile.text,
      resume_id: null,
    };
  }

  if (!file) {
    throw new Error(
      "The current backend accepts resume files. Upload a PDF, DOCX, or TXT file."
    );
  }

  const body = new FormData();
  body.append("file", file);

  const data = await post(ENDPOINTS.analyze, body);
  const profile = data.profile || {};

  return {
    resume_id: data.resume_id,
    name: profile.candidate?.name || "Your profile",
    email: profile.candidate?.email || "",
    text: data.text_preview || text,
    skills: profile.skills || [],
    projects: profile.projects || [],
    domains: profile.domains || profile.domain_scores || [],
    filename: data.filename || file.name,
  };
}
