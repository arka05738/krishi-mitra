/**
 * TypeScript Type Definitions for Krishi Mitra Agricultural Advisory System
 * Conforms strictly to backend schemas (server/app/schemas/api_models.py)
 * Zero non-erasable syntax (no enums), strictly erasable union types.
 */

// Visual Plant Health Diagnosis Result
export interface CropAnalysisResult {
  crop_name: string;
  detected_condition: string;
  quality_grade: string;
  quality_score: number;
  confidence: number;
  severity: string;
  summary: string;
  recommended_action: string[];
  is_crop?: boolean;
  raw_label?: string;
}

// Curated Sample Images for Crop Health Scanner
export interface SampleImageInfo {
  id: string;
  name: string;
  filename: string;
  crop: string;
  condition: string;
  url: string;
}

export interface SampleImagesResponse {
  samples: SampleImageInfo[];
}

// Advisory Query Request & Result
export interface AdvisoryQueryRequest {
  query?: string;
  question?: string;
  crop_name?: string;
  vision_context?: string;
  language?: string;
}

export interface TranscriptionResponse {
  text: string;
  language?: string;
  success: boolean;
}

export interface AdvisoryResult {
  query: string;
  crop_name?: string;
  answer: string;
  sources: string[];
  urgency_level: string;
  helpline: string;
}

// Soil Health Card 12-Parameter Input
export interface SoilReportInput {
  crop: string;
  nitrogen: number;
  phosphorus: number;
  potassium: number;
  ph: number;
  electrical_conductivity: number;
  organic_carbon: number;
  area_acres: number;
  target_yield?: number;
  sulphur?: number;
  zinc?: number;
  boron?: number;
  iron?: number;
  manganese?: number;
  copper?: number;
}

// Soil Health Card Recommendation Output
export interface SoilReportOutput {
  ph_status: string;
  amendment_needed?: string;
  urea_kg: number;
  dap_kg: number;
  mop_kg: number;
  zinc_sulphate_kg?: number;
  application_schedule: string[];
  ssp_kg?: number;
  lime_kg?: number;
  gypsum_kg?: number;
  borax_kg?: number;
  nitrogen_status?: string;
  phosphorus_status?: string;
  potassium_status?: string;
  organic_carbon_status?: string;
  electrical_conductivity_status?: string;
  bags_summary?: Record<string, number>;
}

// Conversational Chat Messages and Payloads
export interface ChatMessage {
  id?: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
  sources?: string[];
  urgency_level?: string;
  helpline?: string;
}

export interface ChatRequest {
  message?: string;
  question?: string;
  crop_name?: string;
  language?: string;
  history?: Array<{ role: string; content: string }>;
}

export interface ChatResponse {
  reply: string;
  response?: string;
  sources: string[];
  urgency_level: string;
  helpline: string;
}

// Station Health & Diagnostics
export interface SystemHealthResponse {
  status: string;
  ollama_status: string;
  chromadb_status: string;
  vision_model_status: string;
  total_documents: number;
  server_mode: string;
  edge_access?: string;
}

// Government Schemes Directory Item
export interface GovernmentScheme {
  id: string;
  title: string;
  category: string;
  benefit: string;
  eligibility: string;
  key_actions: string[];
  helpline: string;
  notice_period?: string;
  portal_url?: string;
}

// Compatibility Aliases for Legacy Contracts
export type AdvisoryRequest = AdvisoryQueryRequest;
export type AdvisoryResponse = AdvisoryResult;
export type CropAnalysisResponse = CropAnalysisResult;
export type SoilReportRequest = SoilReportInput;
export type SoilReportResponse = SoilReportOutput;
export type HealthStatus = SystemHealthResponse;
