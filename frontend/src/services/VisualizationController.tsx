import { createContext, useContext, useState, type ReactNode } from 'react';

type Tab = 'chat' | 'editor' | 'visualizer';

interface DualAgentPayload {
    ai_html?: string | null;
    fallback_html?: string | null;
    explanation?: string;
    type?: string;
    python_code?: string | null;
}

interface VisualizationContextType {
    activeTab: Tab;
    setActiveTab: (tab: Tab) => void;
    visualizationType: string | null;
    setVisualizationType: (type: string | null) => void;
    code: string;
    setCode: (code: string) => void;
    aiHtml: string | null;
    setAiHtml: (html: string | null) => void;
    fallbackHtml: string | null;
    setFallbackHtml: (html: string | null) => void;
    processBackendResponse: (data: DualAgentPayload) => void;
    error: string | null;
    setError: (error: string | null) => void;
    pythonCode: string | null;
    setPythonCode: (code: string | null) => void;
}

const VisualizationContext = createContext<VisualizationContextType | undefined>(undefined);

export const VisualizationProvider = ({ children }: { children: ReactNode }) => {
    const [activeTab, setActiveTab] = useState<Tab>('chat');
    const [visualizationType, setVisualizationType] = useState<string | null>(null);
    const [code, setCode] = useState<string>('// Start coding or ask the AI to generate code...');
    const [aiHtml, setAiHtml] = useState<string | null>(null);
    const [fallbackHtml, setFallbackHtml] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [pythonCode, setPythonCode] = useState<string | null>(null);

    const processBackendResponse = (data: DualAgentPayload) => {
        try {
            if (data.ai_html !== undefined) setAiHtml(data.ai_html ?? null);
            if (data.fallback_html !== undefined) setFallbackHtml(data.fallback_html ?? null);
            if (data.python_code !== undefined) setPythonCode(data.python_code ?? null);

            if (data.ai_html || data.fallback_html) {
                setVisualizationType('data_structure');
                setActiveTab('visualizer');
            }
            setError(null);
        } catch (err) {
            console.error('processBackendResponse error:', err);
            setError('Failed to process the response. Please try again.');
        }
    };

    return (
        <VisualizationContext.Provider value={{
            activeTab,
            setActiveTab,
            visualizationType,
            setVisualizationType,
            code,
            setCode,
            aiHtml,
            setAiHtml,
            fallbackHtml,
            setFallbackHtml,
            processBackendResponse,
            error,
            setError,
            pythonCode,
            setPythonCode,
        }}>
            {children}
        </VisualizationContext.Provider>
    );
};

// eslint-disable-next-line react-refresh/only-export-components
export const useVisualization = () => {
    const context = useContext(VisualizationContext);
    if (context === undefined) {
        throw new Error('useVisualization must be used within a VisualizationProvider');
    }
    return context;
};
