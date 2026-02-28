export type Role = 'user' | 'assistant';

export interface Message {
    id: string;
    role: Role;
    content: string;
    timestamp: number;
    pythonCode?: string;
}

export type VisualizationType = 'none' | 'html' | 'data_structure' | 'algorithm';

export interface CodeBlock {
    language: string;
    code: string;
    title?: string;
}

export interface ChatResponse {
    text_response: string;
    visualization_type: VisualizationType;
    code_blocks: CodeBlock[];
    visualization_data?: unknown;
}

export interface DualAgentResponse {
    type: string;
    ai_html: string | null;
    fallback_html: string | null;
    explanation: string;
    python_code: string | null;
}
