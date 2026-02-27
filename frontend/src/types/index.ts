export type Role = 'user' | 'assistant';

export interface Message {
    id: string;
    role: Role;
    content: string;
    timestamp: number;
}

export type VisualizationType = 'none' | 'html' | 'data_structure' | 'algorithm';

export interface CodeBlock {
    language: string;
    code: string;
    title?: string;
}

/** Legacy response shape (kept for internal compatibility). */
export interface ChatResponse {
    text_response: string;
    visualization_type: VisualizationType;
    code_blocks: CodeBlock[];
    visualization_data?: unknown;
}

/**
 * New Dual-Agent response shape returned by POST /api/v1/chat/
 */
export interface DualAgentResponse {
    /** Always "data_structure" for now. */
    type: string;
    /** Full AI-generated HTML string, or null if unavailable / crashed. */
    ai_html: string | null;
    /** Reliable hardcoded fallback HTML, or null if no keyword matched. */
    fallback_html: string | null;
    /** Plain-text explanation from the AI (always present). */
    explanation: string;
}
