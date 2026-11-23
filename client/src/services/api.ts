/**
 * API Service for Krishi Mitra Agricultural Advisory System.
 * Connects to offline local station over Wi-Fi hotspot using relative URLs.
 * Zero technical jargon in farmer-facing errors.
 */
import type {
  CropAnalysisResult,
  SampleImageInfo,
  AdvisoryResult,
  SoilReportInput,
  SoilReportOutput,
  ChatResponse,
  SystemHealthResponse,
} from '../types/index.ts';

// Relative base URL ensures seamless communication whether accessed locally or from Raspberry Pi 5
const API_BASE = '';

/**
 * Standard error formatter stripping technical details into farmer-friendly guidance.
 */
function handleApiError(error: unknown, fallbackMessage: string): never {
  if (error instanceof TypeError && error.message.includes('fetch')) {
    throw new Error('Local station not responding. Check Wi-Fi hotspot connection.');
  }
  if (error instanceof Error) {
    throw error;
  }
  throw new Error(fallbackMessage);
}

/**
 * Check local station health and readiness.
 */
export async function checkHealth(): Promise<SystemHealthResponse> {
  try {
    const res = await fetch(`${API_BASE}/api/system/health`);
    if (!res.ok) {
      throw new Error(`Station health check returned status ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    return handleApiError(err, 'Local station status unavailable.');
  }
}

/**
 * Retrieve curated sample images for demonstration.
 */
export async function getSampleImages(): Promise<SampleImageInfo[]> {
  try {
    const res = await fetch(`${API_BASE}/api/vision/samples`);
    if (!res.ok) {
      throw new Error(`Failed to load sample images: ${res.status}`);
    }
    const data = await res.json();
    if (Array.isArray(data)) {
      return data;
    }
    if (data && Array.isArray(data.samples)) {
      return data.samples;
    }
    return [];
  } catch (err) {
    return handleApiError(err, 'Unable to load sample crop images.');
  }
}

/**
 * Analyze an uploaded crop or flower image for condition and quality.
 */
export async function analyzeImage(file: File, cropHint?: string, language?: string): Promise<CropAnalysisResult> {
  try {
    const formData = new FormData();
    formData.append('file', file);
    if (cropHint && cropHint.trim()) {
      formData.append('crop_hint', cropHint.trim());
    }
    if (language && language.trim()) {
      formData.append('language', language.trim());
    }

    const res = await fetch(`${API_BASE}/api/vision/predict`, {
      method: 'POST',
      body: formData,
    });

    if (!res.ok) {
      const errBody = await res.json().catch(() => null);
      const detail = errBody?.detail || 'Failed to analyze crop image.';
      throw new Error(detail);
    }

    return await res.json();
  } catch (err) {
    return handleApiError(err, 'Crop image analysis failed.');
  }
}

/**
 * Analyze a curated sample image directly from station disk.
 */
export async function analyzeSampleImage(filename: string, cropHint?: string): Promise<CropAnalysisResult> {
  try {
    const formData = new FormData();
    if (cropHint && cropHint.trim()) {
      formData.append('crop_hint', cropHint.trim());
    }

    const res = await fetch(`${API_BASE}/api/vision/analyze-sample/${encodeURIComponent(filename)}`, {
      method: 'POST',
      body: formData,
    });

    if (!res.ok) {
      const errBody = await res.json().catch(() => null);
      const detail = errBody?.detail || 'Failed to analyze sample crop image.';
      throw new Error(detail);
    }

    return await res.json();
  } catch (err) {
    return handleApiError(err, 'Sample crop image analysis failed.');
  }
}

/**
 * Submit an agricultural question to the advisory assistant.
 */
export async function askAdvisory(
  query: string,
  cropName?: string,
  visionContext?: string,
  language?: string
): Promise<AdvisoryResult> {
  try {
    const res = await fetch(`${API_BASE}/api/advisory/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: query.trim(),
        crop_name: cropName?.trim() || undefined,
        vision_context: visionContext?.trim() || undefined,
        language: language || 'en',
      }),
    });

    if (!res.ok) {
      const errBody = await res.json().catch(() => null);
      const detail = errBody?.detail || 'Failed to retrieve agricultural advisory.';
      throw new Error(detail);
    }

    return await res.json();
  } catch (err) {
    return handleApiError(err, 'Advisory query failed.');
  }
}

/**
 * Stream an agricultural advisory query with Server-Sent Events (SSE).
 */
export function streamAdvisory(
  query: string,
  cropName: string | undefined,
  visionContext: string | undefined,
  onToken: (token: string) => void,
  onComplete: () => void,
  onError: (error: Error) => void
): () => void {
  const controller = new AbortController();

  (async () => {
    try {
      const params = new URLSearchParams({ query });
      if (cropName) params.append('crop_name', cropName);
      if (visionContext) params.append('vision_context', visionContext);

      const res = await fetch(`${API_BASE}/api/advisory/stream?${params.toString()}`, {
        signal: controller.signal,
        headers: { Accept: 'text/event-stream' },
      });

      if (!res.ok) {
        throw new Error(`Streaming failed with status: ${res.status}`);
      }

      if (!res.body) {
        throw new Error('Streaming response body is unavailable.');
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          const trimmed = line.trim();
          if (trimmed.startsWith('data:')) {
            const dataStr = trimmed.slice(5).trim();
            if (dataStr === '[DONE]') {
              onComplete();
              return;
            }
            try {
              const parsed = JSON.parse(dataStr);
              if (parsed.token) {
                onToken(parsed.token);
              }
              if (parsed.done) {
                onComplete();
                return;
              }
            } catch {
              // Raw text chunk fallback
              onToken(dataStr);
            }
          }
        }
      }
      onComplete();
    } catch (err) {
      if ((err as Error)?.name === 'AbortError') {
        return;
      }
      onError(err instanceof Error ? err : new Error(String(err)));
    }
  })();

  return () => {
    controller.abort();
  };
}

/**
 * Send a multi-turn chat message to the advisory assistant.
 */
export async function sendChatMessage(
  message: string,
  cropName?: string,
  history?: Array<{ role: string; content: string }>,
  language?: string
): Promise<ChatResponse> {
  try {
    const res = await fetch(`${API_BASE}/api/chat/message`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: message.trim(),
        crop_name: cropName?.trim() || undefined,
        history: history || [],
        language: language || 'en',
      }),
    });

    if (!res.ok) {
      const errBody = await res.json().catch(() => null);
      const detail = errBody?.detail || 'Failed to send chat message.';
      throw new Error(detail);
    }

    return await res.json();
  } catch (err) {
    return handleApiError(err, 'Chat consultation failed.');
  }
}

/**
 * Transcribe recorded farmer speech using on-device Whisper model.
 */
export async function transcribeAudio(
  audioBlob: Blob,
  language: string = 'hi'
): Promise<{ text: string; language: string; success: boolean }> {
  try {
    const formData = new FormData();
    formData.append('file', audioBlob, 'recording.webm');
    formData.append('language', language);

    const res = await fetch(`${API_BASE}/api/voice/transcribe`, {
      method: 'POST',
      body: formData,
    });

    if (!res.ok) {
      throw new Error(`Voice transcription failed with status ${res.status}`);
    }

    return await res.json();
  } catch (err) {
    return handleApiError(err, 'Voice recognition unavailable.');
  }
}

/**
 * Format advisory text for smooth speech pronunciation.
 */
export async function formatSpeechText(
  text: string,
  language: string = 'en'
): Promise<{ speakable_text: string; bcp47_code: string; language_name: string; native_name: string }> {
  try {
    const res = await fetch(`${API_BASE}/api/voice/format-speech`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, language }),
    });

    if (!res.ok) {
      throw new Error(`Speech formatting failed: ${res.status}`);
    }

    return await res.json();
  } catch (err) {
    return handleApiError(err, 'Voice readout formatting failed.');
  }
}

/**
 * Calculate Soil Health Card fertilizer dosages and schedule.
 */
export async function calculateSoilReport(data: SoilReportInput): Promise<SoilReportOutput> {
  try {
    const res = await fetch(`${API_BASE}/api/advisory/soil-report`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    if (!res.ok) {
      const errBody = await res.json().catch(() => null);
      const detail = errBody?.detail || 'Failed to calculate soil fertilizer schedule.';
      throw new Error(detail);
    }

    return await res.json();
  } catch (err) {
    return handleApiError(err, 'Soil health calculation failed.');
  }
}

export interface PestDetectionItem {
  pest_name: string;
  class_id: number;
  confidence: number;
  confidence_pct: number;
  box: [number, number, number, number];
  severity: string;
  action_threshold: string;
  organic_remedy: string;
  chemical_remedy: string;
  cultural_practice: string;
}

export interface PestDetectionResponse {
  model_type: string;
  total_detected: number;
  detections: PestDetectionItem[];
  latency_ms: number;
  status: string;
}

export async function detectPests(file: File, language: string = 'en'): Promise<PestDetectionResponse> {
  try {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE}/api/vision/pest/detect?lang=${encodeURIComponent(language || 'en')}`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) {
      throw new Error(`Pest detection failed: ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    return handleApiError(err, 'Pest detection failed.');
  }
}

/**
 * Retrieve curated sample pest images for demonstration.
 */
export async function getPestSampleImages(): Promise<SampleImageInfo[]> {
  try {
    const res = await fetch(`${API_BASE}/api/vision/pest-samples`);
    if (!res.ok) {
      throw new Error(`Failed to load pest sample images: ${res.status}`);
    }
    const data = await res.json();
    return Array.isArray(data) ? data : [];
  } catch (err) {
    return handleApiError(err, 'Unable to load sample pest images.');
  }
}

/**
 * Directly analyzes an on-disk sample pest image.
 */
export async function analyzePestSampleImage(
  filename: string,
  language: string = 'en'
): Promise<PestDetectionResponse> {
  try {
    const res = await fetch(
      `${API_BASE}/api/vision/analyze-pest-sample/${encodeURIComponent(filename)}?lang=${encodeURIComponent(language || 'en')}`,
      {
        method: 'POST',
      }
    );
    if (!res.ok) {
      const errBody = await res.json().catch(() => null);
      const detail = errBody?.detail || 'Failed to analyze sample pest image.';
      throw new Error(detail);
    }
    return await res.json();
  } catch (err) {
    return handleApiError(err, 'Sample pest image analysis failed.');
  }
}

/**
 * Dynamically re-localizes an existing CropAnalysisResult when the farmer switches language.
 */
export async function reLocalizeCropResult(
  result: CropAnalysisResult,
  language: string
): Promise<CropAnalysisResult> {
  try {
    const res = await fetch(`${API_BASE}/api/vision/localize`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ result, language }),
    });
    if (!res.ok) {
      throw new Error(`Re-localization failed with status: ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    return handleApiError(err, 'Failed to re-localize crop diagnosis.');
  }
}

/**
 * Dynamically re-localizes an existing pest detection result when the farmer switches language.
 */
export async function reLocalizePestResult(
  pestResult: PestDetectionResponse,
  language: string
): Promise<PestDetectionResponse> {
  try {
    const res = await fetch(`${API_BASE}/api/vision/pest-localize`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ pest_result: pestResult, language }),
    });
    if (!res.ok) {
      throw new Error(`Pest re-localization failed with status: ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    return handleApiError(err, 'Failed to re-localize pest result.');
  }
}

/**
 * Dynamically re-localizes previous chat conversation history into the newly selected language.
 */
export async function reLocalizeChatMessages(
  messages: Array<{ role: string; content: string; timestamp?: string; sources?: string[]; helpline?: string }>,
  language: string
): Promise<any[]> {
  try {
    const res = await fetch(`${API_BASE}/api/chat/re-localize`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messages, language }),
    });
    if (!res.ok) {
      throw new Error(`Chat re-localization failed with status: ${res.status}`);
    }
    const data = await res.json();
    return data.messages || [];
  } catch (err) {
    return handleApiError(err, 'Failed to re-localize chat messages.');
  }
}
