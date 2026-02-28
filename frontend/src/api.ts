import type { DualAgentResponse } from './types';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

export const api = {
    async sendMessage(prompt: string): Promise<DualAgentResponse> {
        const response = await fetch(`${API_BASE_URL}/chat/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt }),
        });

        if (!response.ok) {
            throw new Error(`API Error: ${response.status} ${response.statusText}`);
        }

        return await response.json() as DualAgentResponse;
    },
};
