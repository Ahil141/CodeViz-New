import { useState, useEffect } from 'react';
import { Code2, Play, Loader2 } from 'lucide-react';
import { MonacoEditor } from '../../components/editor/MonacoEditor';
import { useVisualization } from '../../services/VisualizationController';

const LANGUAGES = [
    { id: 'python', name: 'Python' },
    { id: 'javascript', name: 'JavaScript' },
    { id: 'html', name: 'HTML' },
    { id: 'css', name: 'CSS' },
];

export const CodeEditor = () => {
    const { code, setCode, setOutput, setActiveTab, setVisualizationType, pythonCode } = useVisualization();
    const [language, setLanguage] = useState('python');
    const [localCode, setLocalCode] = useState(code);
    const [isRunning, setIsRunning] = useState(false);

    // Sync from global code (e.g. chat generated) to local editor
    useEffect(() => {
        setLocalCode(code);
        // Attempt auto-detection of language if simple
        if (code.trim().startsWith('<!DOCTYPE html>') || code.includes('<html>')) {
            setLanguage('html');
        }
    }, [code]);

    // When the AI returns python_code, populate the editor with it
    useEffect(() => {
        if (pythonCode !== null && pythonCode !== undefined) {
            setLocalCode(pythonCode);
            setCode(pythonCode);
            setLanguage('python');
        }
    }, [pythonCode, setCode]);

    const handleEditorChange = (val: string | undefined) => {
        const newValue = val || '';
        setLocalCode(newValue);
        setCode(newValue); // Keep global state in sync
    };

    const handleRun = async () => {
        setIsRunning(true);
        setActiveTab('visualizer'); // Switch view immediately

        try {
            const response = await fetch('http://localhost:8000/api/v1/execute', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    code: localCode,
                    language: language
                })
            });

            const data = await response.json();

            if (data.status === 'success' || data.status === 'error') {
                if (data.visualization_code) {
                    // It's a web visualization
                    setCode(data.visualization_code);
                    setVisualizationType('html');
                } else {
                    // It's text output
                    setOutput(data.output);
                    setVisualizationType('output');
                }
            }
        } catch (error) {
            console.error("Execution failed:", error);
            setOutput("Error: Failed to connect to execution server.");
            setVisualizationType('output');
        } finally {
            setIsRunning(false);
        }
    };

    return (
        <div className="flex flex-col h-full bg-[#1e1e1e] text-white">
            {/* Toolbar */}
            <div className="flex items-center justify-between px-4 py-2 bg-[#2d2d2d] border-b border-[#3e3e3e]">
                <div className="flex items-center gap-4">
                    <div className="flex items-center gap-2 text-gray-300">
                        <Code2 className="w-4 h-4 text-blue-400" />
                        <span className="text-sm font-semibold">Editor</span>
                    </div>

                    <select
                        value={language}
                        onChange={(e) => setLanguage(e.target.value)}
                        className="bg-[#3e3e3e] text-xs text-white px-2 py-1 rounded border border-gray-600 focus:outline-none focus:border-blue-500"
                    >
                        {LANGUAGES.map(lang => (
                            <option key={lang.id} value={lang.id}>{lang.name}</option>
                        ))}
                    </select>
                </div>

                <button
                    onClick={handleRun}
                    disabled={isRunning}
                    className="flex items-center gap-2 px-3 py-1.5 text-xs font-medium bg-green-600 hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed rounded text-white transition-colors"
                >
                    {isRunning ? <Loader2 className="w-3 h-3 animate-spin" /> : <Play className="w-3 h-3" />}
                    {isRunning ? 'Running...' : 'Run'}
                </button>
            </div>

            {/* Editor Area */}
            <div className="flex-1 overflow-hidden relative">
                <MonacoEditor
                    code={localCode || '# Python implementation will appear here...'}
                    language={language}
                    onChange={handleEditorChange}
                />
            </div>
        </div>
    );
};
