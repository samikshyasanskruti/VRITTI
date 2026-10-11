import { useCallback, useState } from "react";
import { findInternships } from "../services/matchingService";

export default function useMatching() {
  const [results, setResults] = useState([]);
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const search = useCallback(async (resumeText, filters) => {
    setLoading(true);
    setError("");
    try {
      const list = await findInternships({ resumeText, filters });
      setResults(list);
      return list;
    } catch (e) {
      setError(e.message);
      return [];
    } finally {
      setLoading(false);
    }
  }, []);

  const clear = useCallback(() => {
    setResults([]);
    setSelected(null);
    setError("");
  }, []);

  return { results, selected, setSelected, loading, error, search, clear };
}