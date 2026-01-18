import { createContext, useContext, useState, type ReactNode } from 'react';

type Tab = 'chat' | 'editor' | 'visualizer';

interface VisualizationContextType {
    activeTab: Tab;
    setActiveTab: (tab: Tab) => void;
    visualizationType: string | null;
    setVisualizationType: (type: string | null) => void;
    code: string;
    setCode: (code: string) => void;
    processBackendResponse: (data: any) => void;
    error: string | null;
    setError: (error: string | null) => void;
    output: string | null;
    setOutput: (output: string | null) => void;
}

const VisualizationContext = createContext<VisualizationContextType | undefined>(undefined);

export const VisualizationProvider = ({ children }: { children: ReactNode }) => {
    const [activeTab, setActiveTab] = useState<Tab>('chat');
    const [visualizationType, setVisualizationType] = useState<string | null>(null);
    const [code, setCode] = useState<string>('// Start coding or ask the AI to generate code...');
    const [error, setError] = useState<string | null>(null);
    const [output, setOutput] = useState<string | null>(null);

    const processBackendResponse = (data: any) => {
        try {
            console.log("DEBUG: processBackendResponse received:", JSON.stringify(data, null, 2));

            // 1. Handle Code

            // 1. Handle Code
            if (data.code_blocks && data.code_blocks.length > 0) {
                // Check if we have HTML/CSS/JS blocks
                let html = '';
                let css = '';
                let js = '';
                let hasWebCode = false;

                data.code_blocks.forEach((block: any) => {
                    const lang = block.language.toLowerCase();
                    if (lang === 'html') { html = block.code; hasWebCode = true; }
                    else if (lang === 'css') { css = block.code; hasWebCode = true; }
                    else if (lang === 'javascript' || lang === 'js') { js = block.code; hasWebCode = true; }
                });


                if (hasWebCode) {
                    // Assemble into a single HTML string for LivePreview
                    const assembledCode = `
<!DOCTYPE html>
<html>
<head>
<style>
${css}
</style>
</head>
<body>
${html}
<script>
${js}
</script>
</body>
</html>`;
                    setCode(assembledCode.trim());

                    // Force switch to visualizer if logic is missing from backend response (double safety)
                    if (!data.visualization_type || data.visualization_type === 'none') {
                        setVisualizationType('html');
                        setActiveTab('visualizer');
                    }
                } else {
                    // Fallback to simple join for other languages (e.g. Python)
                    const combinedCode = data.code_blocks.map((block: any) =>
                        `// [${block.language.toUpperCase()}]\n${block.code}`
                    ).join('\n\n');
                    setCode(combinedCode);
                }
            }
            else if (data.code) {
                setCode(data.code);
            }



            // 2. Handle Visualization
            if (data.visualization_type && data.visualization_type !== 'none') {
                setVisualizationType(data.visualization_type);
                setActiveTab('visualizer');
            } else if (data.code && (!data.visualization_type || data.visualization_type === 'none')) {
                // If only code is returned, maybe switch to editor?
                // User might prefer to stay in chat, so let's check
                // For now, let's keep user in current tab unless explicit visualizer
            }

            // 3. Clear errors if successful
            setError(null);

        } catch (err) {
            console.error("Error processing backend response:", err);
            setError("Failed to process the response. Please try again.");
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
            processBackendResponse,
            error,
            setError,
            output,
            setOutput
        }}>
            {children}
        </VisualizationContext.Provider>
    );
};

export const useVisualization = () => {
    const context = useContext(VisualizationContext);
    if (context === undefined) {
        throw new Error('useVisualization must be used within a VisualizationProvider');
    }
    return context;
};
