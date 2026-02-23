import type { ChatResponse } from '../types';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

export const api = {
    async sendMessage(prompt: string): Promise<ChatResponse> {
        try {
            const response = await fetch(`${API_BASE_URL}/chat/`, {

                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt }),
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Failed to send message:', error);
            throw error;
        }
    },

    async *sendMessageStream(prompt: string): AsyncGenerator<{
        type: 'text' | 'complete' | 'error';
        content?: string;
        visualization_type?: string;
        code_blocks?: Array<{ language: string; code: string }>;
        visualization_data?: any;
        implementation_code?: { language: string; code: string } | null;
        message?: string;
    }> {
        const response = await fetch(`${API_BASE_URL}/chat/stream`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt }),
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`);
        }

        const reader = response.body?.getReader();
        const decoder = new TextDecoder();

        if (!reader) {
            throw new Error('Response body is not readable');
        }

        let buffer = '';

        while (true) {
            const { done, value } = await reader.read();

            if (done) break;

            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');

            // Keep the last incomplete line in the buffer
            buffer = lines.pop() || '';

            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = line.slice(6);
                    try {
                        const parsed = JSON.parse(data);
                        yield parsed;
                    } catch (e) {
                        console.error('Failed to parse SSE data:', e);
                    }
                }
            }
        }
    },
};
