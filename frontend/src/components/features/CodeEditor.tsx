import { useState, useEffect } from 'react';
import { Code2 } from 'lucide-react';
import { MonacoEditor } from '../../components/editor/MonacoEditor';
import { useVisualization } from '../../services/VisualizationController';

const LANGUAGES = [
    { id: 'python', name: 'Python' },
    { id: 'javascript', name: 'JavaScript' },
    { id: 'html', name: 'HTML' },
    { id: 'css', name: 'CSS' },
];

export const CodeEditor = () => {
    const { code, setCode, pythonCode } = useVisualization();
    const [language, setLanguage] = useState('python');
    const [localCode, setLocalCode] = useState(code);

    useEffect(() => {
        setLocalCode(code);
        if (code.trim().startsWith('<!DOCTYPE html>') || code.includes('<html>')) {
            setLanguage('html');
        }
    }, [code]);

    // populate editor when AI returns python code
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
        setCode(newValue);
    };

    return (
        <div className="flex flex-col h-full bg-[#1e1e1e] text-white">
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
            </div>

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
