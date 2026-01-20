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

export interface ChatResponse {
    text_response: string;
    visualization_type: VisualizationType;
    code_blocks: CodeBlock[];
    visualization_data?: any;
}
