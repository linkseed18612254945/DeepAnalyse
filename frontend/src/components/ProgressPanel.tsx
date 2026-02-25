import { useEffect, useState, useRef } from "react";
import { subscribeProgress, getStatus } from "../services/api";

interface Props {
  sessionId: string;
  onDone: (status: string) => void;
  onBack: () => void;
}

export default function ProgressPanel({ sessionId, onDone, onBack }: Props) {
  const [messages, setMessages] = useState<string[]>([]);
  const [status, setStatus] = useState<string>("pending");
  const logEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Try SSE first, fall back to polling
    let cleanup: (() => void) | null = null;
    let polling: ReturnType<typeof setInterval> | null = null;

    try {
      cleanup = subscribeProgress(
        sessionId,
        (msg) => setMessages((prev) => [...prev, msg]),
        (s) => {
          setStatus(s);
          onDone(s);
        }
      );
    } catch {
      // Fallback: poll status
      polling = setInterval(async () => {
        try {
          const res = await getStatus(sessionId);
          setMessages(res.progress_messages);
          setStatus(res.status);
          if (res.status === "completed" || res.status === "failed") {
            onDone(res.status);
            if (polling) clearInterval(polling);
          }
        } catch { /* ignore */ }
      }, 2000);
    }

    return () => {
      cleanup?.();
      if (polling) clearInterval(polling);
    };
  }, [sessionId, onDone]);

  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const statusLabel =
    status === "completed"
      ? "Complete"
      : status === "failed"
      ? "Failed"
      : "In Progress...";

  return (
    <div style={styles.container}>
      <div style={styles.headerRow}>
        <h2 style={styles.heading}>Analysis {statusLabel}</h2>
        <button onClick={onBack} style={styles.backBtn}>
          Back
        </button>
      </div>

      <div style={styles.progressBar}>
        <div
          style={{
            ...styles.progressFill,
            width: status === "completed" ? "100%" : status === "failed" ? "100%" : "60%",
            background: status === "failed" ? "#f85149" : "#238636",
          }}
        />
      </div>

      <div style={styles.logBox}>
        {messages.map((msg, i) => (
          <div key={i} style={styles.logLine}>
            <span style={styles.logIndex}>{String(i + 1).padStart(2, "0")}</span>
            {msg}
          </div>
        ))}
        <div ref={logEndRef} />
      </div>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    background: "#161b22",
    border: "1px solid #30363d",
    borderRadius: 8,
    padding: 24,
  },
  headerRow: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 16,
  },
  heading: {
    margin: 0,
    fontSize: 18,
    color: "#c9d1d9",
  },
  backBtn: {
    padding: "6px 14px",
    fontSize: 13,
    background: "#21262d",
    border: "1px solid #30363d",
    borderRadius: 6,
    color: "#8b949e",
    cursor: "pointer",
  },
  progressBar: {
    height: 4,
    background: "#30363d",
    borderRadius: 2,
    overflow: "hidden",
    marginBottom: 16,
  },
  progressFill: {
    height: "100%",
    borderRadius: 2,
    transition: "width 0.5s ease",
  },
  logBox: {
    background: "#0d1117",
    border: "1px solid #21262d",
    borderRadius: 6,
    padding: 16,
    maxHeight: 420,
    overflowY: "auto" as const,
    fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
    fontSize: 13,
    lineHeight: 1.6,
  },
  logLine: {
    color: "#8b949e",
  },
  logIndex: {
    color: "#484f58",
    marginRight: 12,
  },
};
