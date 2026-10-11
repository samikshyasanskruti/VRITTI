import { useCallback, useEffect, useMemo, useState } from "react";
import { fromMatches, fetchRecommendations } from "../services/recommendationService";

// By default the recommendations are worked out from your matches.
// Pass { remote: true, resumeText } to ask the backend instead.
export default function useRecommendations(matches = [], { remote = false, resumeText = "" } = {}) {
  const local = useMemo(() => fromMatches(matches), [matches]);
  const [remoteData, setRemoteData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const refresh = useCallback(async () => {
    if (!resumeText) return;
    setLoading(true);
    setError("");
    try {
      setRemoteData(await fetchRecommendations({ resumeText }));
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, [resumeText]);

  useEffect(() => {
    if (remote) refresh();
  }, [remote, refresh]);

  return { recommendations: remote && remoteData ? remoteData : local, loading, error, refresh };
}