import { useEffect, useState } from "react";
import { listSessions } from "../services/api";
import type { SessionSummary } from "../types";

interface Props {
  onSelect: (sessionId: string) => void;
}

export default function SessionList({ onSelect }: Props) {
  const [sessions, setSessions] = useState<SessionSummary[]>([]);

  useEffect(() => {
    listSessions()
      .then(setSessions)
      .catch(() => {});
  }, []);

  if (sessions.length === 0) return null;

  return (
    <div style={styles.container}>
      <h3 style={styles.heading}>Previous Analyses</h3>
      {sessions.map((s) => (
        <div
          key={s.id}
          style={styles.row}
          onClick={() => onSelect(s.id)}
        >
          <span style={styles.topic}>{s.user_input}</span>
          <span
            style={{
              ...styles.status,
              color: s.status === "completed" ? "#3fb950" : "#f0883e",
            }}
          >
            {s.status}
          </span>
        </div>
      ))}
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    background: "#161b22",
    border: "1px solid #30363d",
    borderRadius: 8,
    padding: 16,
  },
  heading: {
    margin: "0 0 12px",
    fontSize: 15,
    color: "#8b949e",
  },
  row: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "8px 12px",
    borderRadius: 6,
    cursor: "pointer",
    borderBottom: "1px solid #21262d",
  },
  topic: {
    fontSize: 13,
    color: "#c9d1d9",
    overflow: "hidden",
    textOverflow: "ellipsis",
    whiteSpace: "nowrap" as const,
    maxWidth: "75%",
  },
  status: {
    fontSize: 12,
    fontWeight: 600,
  },
};
