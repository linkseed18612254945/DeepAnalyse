import { useState } from "react";
import { startAnalysis } from "../services/api";

interface Props {
  onStarted: (sessionId: string) => void;
}

export default function AnalysisForm({ onStarted }: Props) {
  const [topic, setTopic] = useState("");
  const [maxRounds, setMaxRounds] = useState(3);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!topic.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const res = await startAnalysis(topic.trim(), maxRounds);
      onStarted(res.session_id);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Failed to start analysis");
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <h2 style={styles.heading}>Start Intelligence Analysis</h2>
      <p style={styles.subtitle}>
        Enter an event, topic, URL, or description to begin deep analysis.
      </p>

      <textarea
        value={topic}
        onChange={(e) => setTopic(e.target.value)}
        placeholder="e.g. 'Recent semiconductor export controls and their geopolitical implications'"
        rows={4}
        style={styles.textarea}
        disabled={loading}
      />

      <div style={styles.options}>
        <label style={styles.label}>
          Retrieval rounds:
          <select
            value={maxRounds}
            onChange={(e) => setMaxRounds(Number(e.target.value))}
            style={styles.select}
            disabled={loading}
          >
            {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12].map((n) => (
              <option key={n} value={n}>
                {n} round{n > 1 ? "s" : ""}
              </option>
            ))}
          </select>
        </label>
      </div>

      {error && <p style={styles.error}>{error}</p>}

      <button type="submit" disabled={loading || !topic.trim()} style={styles.button}>
        {loading ? "Starting..." : "Begin Analysis"}
      </button>
    </form>
  );
}

const styles: Record<string, React.CSSProperties> = {
  form: {
    background: "#161b22",
    border: "1px solid #30363d",
    borderRadius: 8,
    padding: 24,
  },
  heading: {
    margin: "0 0 4px",
    fontSize: 18,
    color: "#c9d1d9",
  },
  subtitle: {
    margin: "0 0 16px",
    fontSize: 14,
    color: "#8b949e",
  },
  textarea: {
    width: "100%",
    padding: 12,
    fontSize: 14,
    fontFamily: "inherit",
    background: "#0d1117",
    border: "1px solid #30363d",
    borderRadius: 6,
    color: "#c9d1d9",
    resize: "vertical",
    boxSizing: "border-box",
  },
  options: {
    display: "flex",
    gap: 16,
    margin: "12px 0",
  },
  label: {
    fontSize: 13,
    color: "#8b949e",
    display: "flex",
    alignItems: "center",
    gap: 8,
  },
  select: {
    padding: "4px 8px",
    background: "#0d1117",
    border: "1px solid #30363d",
    borderRadius: 4,
    color: "#c9d1d9",
    fontSize: 13,
  },
  error: {
    color: "#f85149",
    fontSize: 13,
    margin: "8px 0",
  },
  button: {
    padding: "10px 24px",
    fontSize: 14,
    fontWeight: 600,
    background: "#238636",
    border: "1px solid #2ea043",
    borderRadius: 6,
    color: "#fff",
    cursor: "pointer",
  },
};
