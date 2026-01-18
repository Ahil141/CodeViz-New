import { useEffect, useRef } from 'react';

interface LivePreviewProps {
    code: string;
}

export const LivePreview = ({ code }: LivePreviewProps) => {
    const iframeRef = useRef<HTMLIFrameElement>(null);

    useEffect(() => {
        if (iframeRef.current) {
            // We write directly to the document to allow immediate rendering
            // In a real production app, we might use srcDoc, but writing to doc is often more reliable for immediate updates
            const doc = iframeRef.current.contentDocument;
            if (doc) {
                doc.open();
                doc.write(code);
                doc.close();
            }
        }
    }, [code]);

    return (
        <div className="w-full h-full bg-white rounded-lg overflow-hidden border border-gray-200 shadow-sm">
            <div className="bg-gray-100 px-4 py-2 border-b border-gray-200 flex items-center justify-between">
                <span className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Live Preview</span>
                <div className="flex gap-1">
                    <div className="w-2 h-2 rounded-full bg-red-400"></div>
                    <div className="w-2 h-2 rounded-full bg-yellow-400"></div>
                    <div className="w-2 h-2 rounded-full bg-green-400"></div>
                </div>
            </div>
            <iframe
                ref={iframeRef}
                title="Live Preview"
                className="w-full h-full border-none"
                sandbox="allow-scripts" // Allow scripts but BLOCK forms, top-navigation, popups, and same-origin access
            // sandbox="allow-scripts allow-modals" -> If we wanted alerts
            // Security: Missing 'allow-same-origin' prevents the iframe from accessing cookies/localStorage of the parent
            />
        </div>
    );
};
