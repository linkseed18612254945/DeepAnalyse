import ReactMarkdown from "react-markdown";
import type { ReportResponse } from "../types";

interface Props {
  report: ReportResponse;
}

export default function ReportView({ report }: Props) {
  const handleDownloadMd = () => {
    const blob = new Blob([report.report_markdown], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `report-${report.report.id}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleDownloadJson = () => {
    const blob = new Blob([JSON.stringify(report.report, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `report-${report.report.id}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div style={styles.container}>
      <div style={styles.toolbar}>
        <h2 style={styles.title}>{report.report.title}</h2>
        <div style={styles.actions}>
          <button onClick={handleDownloadMd} style={styles.btn}>
            Download .md
          </button>
          <button onClick={handleDownloadJson} style={styles.btn}>
            Download .json
          </button>
        </div>
      </div>

      <div style={styles.content}>
        <ReactMarkdown>{report.report_markdown}</ReactMarkdown>
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
  toolbar: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 16,
    flexWrap: "wrap",
    gap: 12,
  },
  title: {
    margin: 0,
    fontSize: 18,
    color: "#c9d1d9",
  },
  actions: {
    display: "flex",
    gap: 8,
  },
  btn: {
    padding: "6px 14px",
    fontSize: 13,
    background: "#21262d",
    border: "1px solid #30363d",
    borderRadius: 6,
    color: "#c9d1d9",
    cursor: "pointer",
  },
  content: {
    background: "#0d1117",
    border: "1px solid #21262d",
    borderRadius: 6,
    padding: 24,
    lineHeight: 1.7,
    fontSize: 15,
    color: "#c9d1d9",
  },
};
