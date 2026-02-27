import { createContext, useContext, useState, type ReactNode } from 'react';

type Tab = 'chat' | 'editor' | 'visualizer';

interface DualAgentPayload {
    ai_html?: string | null;
    fallback_html?: string | null;
    explanation?: string;
    type?: string;
}

interface VisualizationContextType {
    activeTab: Tab;
    setActiveTab: (tab: Tab) => void;
    visualizationType: string | null;
    setVisualizationType: (type: string | null) => void;
    code: string;
    setCode: (code: string) => void;
    /** AI-generated HTML from the Dual-Agent (may be null). */
    aiHtml: string | null;
    setAiHtml: (html: string | null) => void;
    /** Reliable hardcoded fallback HTML (may be null if no keyword matched). */
    fallbackHtml: string | null;
    setFallbackHtml: (html: string | null) => void;
    processBackendResponse: (data: DualAgentPayload) => void;
    error: string | null;
    setError: (error: string | null) => void;
    output: string | null;
    setOutput: (output: string | null) => void;
    implementationCode: string | null;
    setImplementationCode: (code: string | null) => void;
}

const VisualizationContext = createContext<VisualizationContextType | undefined>(undefined);

export const VisualizationProvider = ({ children }: { children: ReactNode }) => {
    const [activeTab, setActiveTab] = useState<Tab>('chat');
    const [visualizationType, setVisualizationType] = useState<string | null>(null);
    const [code, setCode] = useState<string>('// Start coding or ask the AI to generate code...');
    const [aiHtml, setAiHtml] = useState<string | null>(null);
    const [fallbackHtml, setFallbackHtml] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [output, setOutput] = useState<string | null>(null);
    const [implementationCode, setImplementationCode] = useState<string | null>(null);

    const processBackendResponse = (data: DualAgentPayload) => {
        try {
            console.log('DEBUG: processBackendResponse received:', JSON.stringify(data, null, 2));

            // Store ai_html and fallback_html in state for VisualizerPanel
            if (data.ai_html !== undefined) {
                setAiHtml(data.ai_html ?? null);
            }
            if (data.fallback_html !== undefined) {
                setFallbackHtml(data.fallback_html ?? null);
            }

            // Switch to visualizer tab whenever we have something to show
            if (data.ai_html || data.fallback_html) {
                setVisualizationType('data_structure');
                setActiveTab('visualizer');
            }

            setError(null);
        } catch (err) {
            console.error('Error processing backend response:', err);
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
            output,
            setOutput,
            implementationCode,
            setImplementationCode,
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
