import React, { useEffect, useState } from 'react';

interface VisualizerProps {
    code: string | null;
    title?: string;
}

const Visualizer: React.FC<VisualizerProps> = ({ code, title }) => {
    const [iframeSrc, setIframeSrc] = useState<string>('');

    // This effect handles the generation of the iframe source whenever the 'code' prop changes.
    useEffect(() => {
        if (!code) {
            // Clear the iframe source if there's no code, and revoke any existing URL.
            if (iframeSrc) {
                URL.revokeObjectURL(iframeSrc);
            }
            // setIframeSrc(''); // Remove synchronous setIframeSrc within effect to avoid cascading renders
            return;
        }

        // Create a separate document structure if code doesn't have it?
        // The RAG docs we seeded are just the body relevant parts inside markdown blocks.
        // We probably need to strip the markdown blocks if they exist, or the backend does it.
        // The current backend endpoint returns 'visualizer_code' which is the raw content of the doc.
        // The doc content in seed_visualizers.py is:
        // "Here is ... \n ```html ... ``` \n ```css ... ```"
        // The logic in Chat endpoint `chat.py` extracts code blocks. 
        // Our new RAG endpoint returns the raw doc. 
        // We should parse it on the frontend OR backend.
        // The user request said: "It parses the raw string to separate HTML, CSS, and JS [...]"

        // Let's implement a simple parser here to construct a full HTML file.
        const constructHtml = (rawCode: string) => {
            // 1. naive check if it's already a full HTML
            if (rawCode.trim().startsWith('<!DOCTYPE html>') || rawCode.trim().startsWith('<html')) {
                return rawCode;
            }

            // 2. Extract blocks
            const htmlMatch = rawCode.match(/```html\n([\s\S]*?)```/i);
            const cssMatch = rawCode.match(/```css\n([\s\S]*?)```/i);
            const jsMatch = rawCode.match(/```(?:javascript|js)\n([\s\S]*?)```/i);

            const html = htmlMatch ? htmlMatch[1] : '';
            const css = cssMatch ? cssMatch[1] : '';
            const js = jsMatch ? jsMatch[1] : '';

            if (!html && !css && !js) {
                // Determine if rawCode is just HTML
                return rawCode;
            }

            return `
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        body { font-family: sans-serif; padding: 10px; }
                        ${css}
                    </style>
                </head>
                <body>
                    ${html}
                    <script>
                        try {
                            ${js}
                        } catch(e) {
                            console.error("Visualization Error:", e);
                            document.body.innerHTML += '<div style="color:red">Runtime Error: ' + e.message + '</div>';
                        }
                    </script>
                </body>
                </html>
            `;
        };

        const finalHtml = constructHtml(code);
        const blob = new Blob([finalHtml], { type: 'text/html' });
        const url = URL.createObjectURL(blob);

        setIframeSrc(url);

        return () => {
            URL.revokeObjectURL(url);
            // setIframeSrc(''); // Avoid synchronous reset in cleanup if not necessary to prevent render loops
        };
    }, [code]);

    if (!code) {
        return (
            <div className="flex items-center justify-center h-full bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-10 text-gray-400">
                <p>Select a data structure to view its visualization.</p>
            </div>
        );
    }

    return (
        <div className="w-full h-full flex flex-col bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
            {title && (
                <div className="bg-[#030712]/50 backdrop-blur-md px-4 py-2 border-b border-white/10 flex justify-between items-center">
                    <span
                        className="text-xs font-normal text-white select-none"
                        style={{
                            fontFamily: "var(--font-futuristic)",
                            filter: "drop-shadow(0 0 5px rgba(255, 255, 255, 0.5))"
                        }}
                    >
                        {title.toUpperCase()}
                    </span>
                </div>
            )}
            <div className="flex-1 relative bg-white">
                <iframe
                    src={iframeSrc}
                    className="w-full h-full border-0"
                    sandbox="allow-scripts allow-modals allow-popups allow-forms"
                    title="Data Structure Visualization"
                />
            </div>
        </div>
    );
};

export default Visualizer;
