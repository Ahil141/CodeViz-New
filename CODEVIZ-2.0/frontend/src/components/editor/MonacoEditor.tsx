import Editor, { type OnMount } from '@monaco-editor/react';
import { useRef } from 'react';

interface MonacoEditorProps {
    code: string;
    language: string;
    onChange?: (value: string | undefined) => void;
    readOnly?: boolean;
}

export const MonacoEditor = ({
    code,
    language,
    onChange,
    readOnly = false
}: MonacoEditorProps) => {
    const editorRef = useRef(null);

    const handleEditorDidMount: OnMount = (editor) => {
        // @ts-ignore
        editorRef.current = editor;
    };

    return (
        <div className="h-full w-full overflow-hidden rounded-md border border-gray-700 shadow-inner">
            <Editor
                height="100%"
                defaultLanguage="python"
                language={language}
                value={code}
                onChange={onChange}
                onMount={handleEditorDidMount}
                theme="vs-dark"
                options={{
                    readOnly: readOnly,
                    minimap: { enabled: false },
                    scrollBeyondLastLine: false,
                    fontSize: 14,
                    wordWrap: 'on',
                    automaticLayout: true,
                    padding: { top: 16 }
                }}
                loading={
                    <div className="flex items-center justify-center h-full text-gray-400">
                        Loading Editor...
                    </div>
                }
            />
        </div>
    );
};
