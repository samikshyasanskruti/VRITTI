import { useCallback, useState } from "react";
import { analyzeResume } from "../services/resumeService";

export default function useResume() {
  const [profile, setProfile] = useState(null);
  const [resumeText, setResumeText] = useState("");
  const [fileName, setFileName] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const analyze = useCallback(async ({ text, file }) => {
    setLoading(true);
    setError("");
    try {
      const p = await analyzeResume({ text, file });
      setProfile(p);
      setResumeText(p.text || text || "");
      setFileName(file?.name || "");
      return p;
    } catch (e) {
      setError(e.message);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const reset = useCallback(() => {
    setProfile(null);
    setResumeText("");
    setFileName("");
    setError("");
  }, []);

  return { profile, resumeText, fileName, loading, error, analyze, reset };
}