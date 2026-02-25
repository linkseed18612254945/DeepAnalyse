/* Domain types matching the backend models. */

export type AnalysisStatus =
  | "pending"
  | "framing"
  | "retrieving"
  | "extracting"
  | "analyzing"
  | "generating_report"
  | "completed"
  | "failed";

export interface AnalysisStatusResponse {
  session_id: string;
  status: AnalysisStatus;
  progress_messages: string[];
  error: string | null;
}

export interface Source {
  url: string;
  title: string;
  domain: string;
  tier: number;
  snippet: string;
  retrieved_at: string;
}

export interface Entity {
  id: string;
  name: string;
  entity_type: string;
  description: string;
  attributes: Record<string, unknown>;
  sources: Source[];
}

export interface Relationship {
  id: string;
  source_entity_id: string;
  target_entity_id: string;
  relationship_type: string;
  description: string;
  confidence: string;
  sources: Source[];
}

export interface IntelligenceReport {
  id: string;
  title: string;
  executive_summary: string;
  event_overview: string;
  key_actors_analysis: string;
  deep_background: string;
  hidden_connections: string;
  analytical_assessment: string;
  scenarios_and_implications: string;
  confidence_assessment: string;
  key_questions_remaining: string;
  sources_and_citations: string;
  generated_at: string;
}

export interface ReportResponse {
  report: IntelligenceReport;
  report_markdown: string;
}

export interface GraphResponse {
  entities: Entity[];
  relationships: Relationship[];
}

export interface SessionSummary {
  id: string;
  user_input: string;
  status: AnalysisStatus;
  created_at: string;
}
