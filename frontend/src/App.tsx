import { useState } from "react";
import AnalysisForm from "./components/AnalysisForm";
import ProgressPanel from "./components/ProgressPanel";
import ReportView from "./components/ReportView";
import GraphView from "./components/GraphView";
import SessionList from "./components/SessionList";
import type { AnalysisStatus, ReportResponse, GraphResponse } from "./types";
import { getReport, getGraph } from "./services/api";

type View = "form" | "progress" | "report";

export default function App() {
  const [view, setView] = useState<View>("form");
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [reportData, setReportData] = useState<ReportResponse | null>(null);
  const [graphData, setGraphData] = useState<GraphResponse | null>(null);
  const [activeTab, setActiveTab] = useState<"report" | "graph">("report");

  const handleStarted = (sid: string) => {
    setSessionId(sid);
    setView("progress");
  };

  const handleDone = async (status: string) => {
    if (status === "completed" && sessionId) {
      try {
        const [report, graph] = await Promise.all([
          getReport(sessionId),
          getGraph(sessionId),
        ]);
        setReportData(report);
        setGraphData(graph);
        setView("report");
      } catch {
        /* stay on progress view to show error */
      }
    }
  };

  const handleReset = () => {
    setView("form");
    setSessionId(null);
    setReportData(null);
    setGraphData(null);
  };

  const handleSelectSession = async (sid: string) => {
    setSessionId(sid);
    try {
      const [report, graph] = await Promise.all([
        getReport(sid),
        getGraph(sid),
      ]);
      setReportData(report);
      setGraphData(graph);
      setView("report");
    } catch {
      setView("progress");
    }
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.title} onClick={handleReset}>
          Deep Intelligence Analysis Platform
        </h1>
        <span style={styles.version}>v1.0 MVP</span>
      </header>

      <main style={styles.main}>
        {view === "form" && (
          <div style={styles.formLayout}>
            <AnalysisForm onStarted={handleStarted} />
            <SessionList onSelect={handleSelectSession} />
          </div>
        )}

        {view === "progress" && sessionId && (
          <ProgressPanel
            sessionId={sessionId}
            onDone={handleDone}
            onBack={handleReset}
          />
        )}

        {view === "report" && reportData && (
          <div>
            <div style={styles.tabs}>
              <button
                style={activeTab === "report" ? styles.tabActive : styles.tab}
                onClick={() => setActiveTab("report")}
              >
                Report
              </button>
              <button
                style={activeTab === "graph" ? styles.tabActive : styles.tab}
                onClick={() => setActiveTab("graph")}
              >
                Knowledge Graph
              </button>
              <button style={styles.tab} onClick={handleReset}>
                New Analysis
              </button>
            </div>

            {activeTab === "report" && (
              <ReportView report={reportData} />
            )}
            {activeTab === "graph" && graphData && (
              <GraphView data={graphData} />
            )}
          </div>
        )}
      </main>
    </div>
  );
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    fontFamily:
      "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    maxWidth: 1100,
    margin: "0 auto",
    padding: "0 24px",
    color: "#e0e0e0",
    background: "#0d1117",
    minHeight: "100vh",
  },
  header: {
    display: "flex",
    alignItems: "baseline",
    gap: 12,
    padding: "24px 0 16px",
    borderBottom: "1px solid #21262d",
  },
  title: {
    margin: 0,
    fontSize: 22,
    fontWeight: 700,
    color: "#58a6ff",
    cursor: "pointer",
  },
  version: {
    fontSize: 12,
    color: "#8b949e",
  },
  main: {
    paddingTop: 24,
    paddingBottom: 48,
  },
  formLayout: {
    display: "flex",
    flexDirection: "column",
    gap: 32,
  },
  tabs: {
    display: "flex",
    gap: 8,
    marginBottom: 24,
  },
  tab: {
    padding: "8px 16px",
    background: "#161b22",
    border: "1px solid #30363d",
    borderRadius: 6,
    color: "#8b949e",
    cursor: "pointer",
    fontSize: 14,
  },
  tabActive: {
    padding: "8px 16px",
    background: "#1f6feb",
    border: "1px solid #1f6feb",
    borderRadius: 6,
    color: "#fff",
    cursor: "pointer",
    fontSize: 14,
  },
};
