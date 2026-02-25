/* API client for the DIAP backend. */

import type {
  AnalysisStatusResponse,
  GraphResponse,
  ReportResponse,
  SessionSummary,
} from "../types";

const BASE = "";

export async function startAnalysis(
  topic: string,
  maxRounds: number = 3,
  outputFormats: string[] = ["markdown", "json"]
): Promise<AnalysisStatusResponse> {
  const res = await fetch(`${BASE}/api/analyse`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      topic,
      max_rounds: maxRounds,
      output_formats: outputFormats,
    }),
  });
  if (!res.ok) throw new Error(`Start failed: ${res.statusText}`);
  return res.json();
}

export async function getStatus(
  sessionId: string
): Promise<AnalysisStatusResponse> {
  const res = await fetch(`${BASE}/api/analyse/${sessionId}`);
  if (!res.ok) throw new Error(`Status fetch failed: ${res.statusText}`);
  return res.json();
}

export async function getReport(sessionId: string): Promise<ReportResponse> {
  const res = await fetch(`${BASE}/api/analyse/${sessionId}/report`);
  if (!res.ok) throw new Error(`Report fetch failed: ${res.statusText}`);
  return res.json();
}

export async function getGraph(sessionId: string): Promise<GraphResponse> {
  const res = await fetch(`${BASE}/api/analyse/${sessionId}/graph`);
  if (!res.ok) throw new Error(`Graph fetch failed: ${res.statusText}`);
  return res.json();
}

export async function listSessions(): Promise<SessionSummary[]> {
  const res = await fetch(`${BASE}/api/sessions`);
  if (!res.ok) throw new Error(`Sessions fetch failed: ${res.statusText}`);
  return res.json();
}

/**
 * Subscribe to SSE progress events for a session.
 * Returns a cleanup function.
 */
export function subscribeProgress(
  sessionId: string,
  onMessage: (msg: string) => void,
  onDone: (status: string) => void
): () => void {
  const evtSource = new EventSource(
    `${BASE}/api/analyse/${sessionId}/stream`
  );

  evtSource.addEventListener("progress", (e) => {
    onMessage((e as MessageEvent).data);
  });

  evtSource.addEventListener("done", (e) => {
    onDone((e as MessageEvent).data);
    evtSource.close();
  });

  evtSource.onerror = () => {
    evtSource.close();
  };

  return () => evtSource.close();
}
