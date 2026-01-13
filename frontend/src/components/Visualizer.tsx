import { useState, useEffect, useRef } from 'react'
import { Loader2, Code, X } from 'lucide-react'

interface VisualizerProps {
  visualizerCode: string | null
  isLoadingVisualizer: boolean
}

type CodeSection = 'html' | 'css' | 'js'

interface ParsedCode {
  html: string
  css: string
  js: string
}

function Visualizer({
  visualizerCode,
  isLoadingVisualizer,
}: VisualizerProps) {
  const [code, setCode] = useState<string | null>(null)
  const [iframeSrc, setIframeSrc] = useState<string | null>(null)
  const [showCodeModal, setShowCodeModal] = useState(false)
  const [parsedCode, setParsedCode] = useState<ParsedCode>({
    html: '',
    css: '',
    js: '',
  })
  const [activeTab, setActiveTab] = useState<CodeSection>('html')
  const iframeRef = useRef<HTMLIFrameElement>(null)
  const blobUrlRef = useRef<string | null>(null)

  // Store visualizer code in component state when it changes
  useEffect(() => {
    if (visualizerCode) {
      setCode(visualizerCode)
    } else {
      setCode(null)
      setIframeSrc(null)
    }
  }, [visualizerCode])

  // Parse code to extract HTML, CSS, and JS
  const parseCode = (codeContent: string): ParsedCode => {
    const result: ParsedCode = { html: '', css: '', js: '' }

    // Check if it's a complete HTML document
    const isCompleteHTML =
      codeContent.trim().toLowerCase().startsWith('<!doctype') ||
      codeContent.trim().toLowerCase().startsWith('<html')

    if (isCompleteHTML) {
      // Extract CSS from <style> tags
      const styleMatch = codeContent.match(/<style[^>]*>([\s\S]*?)<\/style>/gi)
      if (styleMatch) {
        result.css = styleMatch
          .map((match) => {
            const content = match.replace(/<style[^>]*>|<\/style>/gi, '')
            return content.trim()
          })
          .join('\n\n')
      }

      // Extract JS from <script> tags
      const scriptMatch = codeContent.match(
        /<script[^>]*>([\s\S]*?)<\/script>/gi
      )
      if (scriptMatch) {
        result.js = scriptMatch
          .map((match) => {
            const content = match.replace(/<script[^>]*>|<\/script>/gi, '')
            return content.trim()
          })
          .join('\n\n')
      }

      // Extract HTML body content
      const bodyMatch = codeContent.match(/<body[^>]*>([\s\S]*?)<\/body>/i)
      if (bodyMatch) {
        result.html = bodyMatch[1].trim()
      } else {
        // If no body tag, try to extract content between head and script/style
        let htmlContent = codeContent
        // Remove DOCTYPE and html tag
        htmlContent = htmlContent.replace(/<!DOCTYPE[^>]*>/gi, '')
        htmlContent = htmlContent.replace(/<html[^>]*>/gi, '')
        htmlContent = htmlContent.replace(/<\/html>/gi, '')
        // Remove head section
        htmlContent = htmlContent.replace(/<head[^>]*>[\s\S]*?<\/head>/gi, '')
        // Remove style tags
        htmlContent = htmlContent.replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
        // Remove script tags
        htmlContent = htmlContent.replace(
          /<script[^>]*>[\s\S]*?<\/script>/gi,
          ''
        )
        result.html = htmlContent.trim()
      }
    } else {
      // If it's not a complete HTML document, treat it as HTML content
      result.html = codeContent
    }

    return result
  }

  // Update parsed code when code changes
  useEffect(() => {
    if (code) {
      setParsedCode(parseCode(code))
    }
  }, [code])

  // Create iframe content from code
  useEffect(() => {
    if (!code) {
      // Clean up previous blob URL
      if (blobUrlRef.current) {
        URL.revokeObjectURL(blobUrlRef.current)
        blobUrlRef.current = null
      }
      setIframeSrc(null)
      return
    }

    // Check if code is already a complete HTML document
    const isCompleteHTML =
      code.trim().toLowerCase().startsWith('<!doctype') ||
      code.trim().toLowerCase().startsWith('<html')

    let htmlContent: string

    if (isCompleteHTML) {
      // Use code as-is if it's already a complete HTML document
      htmlContent = code
    } else {
      // Wrap code in a complete HTML document
      htmlContent = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Data Structure Visualizer</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    body {
      width: 100%;
      height: 100vh;
      overflow: auto;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
        'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
        sans-serif;
    }
  </style>
</head>
<body>
  ${code}
</body>
</html>`
    }

    // Clean up previous blob URL
    if (blobUrlRef.current) {
      URL.revokeObjectURL(blobUrlRef.current)
    }

    // Create blob and URL
    const blob = new Blob([htmlContent], { type: 'text/html' })
    const url = URL.createObjectURL(blob)
    blobUrlRef.current = url
    setIframeSrc(url)

    // Cleanup function
    return () => {
      if (blobUrlRef.current) {
        URL.revokeObjectURL(blobUrlRef.current)
        blobUrlRef.current = null
      }
    }
  }, [code])

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (blobUrlRef.current) {
        URL.revokeObjectURL(blobUrlRef.current)
        blobUrlRef.current = null
      }
    }
  }, [])

  if (isLoadingVisualizer) {
    return (
      <div className="h-full bg-white flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-8 h-8 text-indigo-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Loading visualizer...</p>
        </div>
      </div>
    )
  }

  if (!code || !iframeSrc) {
    return (
      <div className="h-full bg-white flex items-center justify-center">
        <div className="text-center p-8">
          <div className="w-24 h-24 mx-auto mb-4 bg-indigo-100 rounded-full flex items-center justify-center">
            <svg
              className="w-12 h-12 text-indigo-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
              />
            </svg>
          </div>
          <h2 className="text-2xl font-semibold text-gray-800 mb-2">
            Data Structure Visualizer
          </h2>
          <p className="text-gray-600 mb-4">
            Select a data structure to view its interactive visualizer.
          </p>
          <p className="text-sm text-gray-500">
            You can also ask questions about it in the chat!
          </p>
        </div>
      </div>
    )
  }

  return (
    <>
      <div className="h-full bg-white flex flex-col">
        <div className="border-b border-gray-200 px-4 py-3 bg-gray-50 flex items-center justify-between">
          <h3 className="text-sm font-semibold text-gray-700">
            Data Structure Visualizer
          </h3>
          <button
            onClick={() => setShowCodeModal(true)}
            className="flex items-center gap-2 px-3 py-1.5 text-sm text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors"
          >
            <Code className="w-4 h-4" />
            <span>Show Code</span>
          </button>
        </div>
        <div className="flex-1 overflow-hidden">
          <iframe
            ref={iframeRef}
            src={iframeSrc}
            className="w-full h-full border-0"
            title="Data Structure Visualizer"
            sandbox="allow-scripts allow-same-origin allow-forms allow-popups allow-modals"
            allow="accelerometer; camera; encrypted-media; geolocation; gyroscope; microphone; midi; payment; usb; vr; xr-spatial-tracking"
          />
        </div>
      </div>

      {/* Code Modal */}
      {showCodeModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] flex flex-col">
            {/* Modal Header */}
            <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-800">View Code</h2>
              <button
                onClick={() => setShowCodeModal(false)}
                className="text-gray-400 hover:text-gray-600 transition-colors"
              >
                <X className="w-6 h-6" />
              </button>
            </div>

            {/* Tabs */}
            <div className="flex border-b border-gray-200">
              {(['html', 'css', 'js'] as CodeSection[]).map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`px-6 py-3 text-sm font-medium transition-colors ${
                    activeTab === tab
                      ? 'text-indigo-600 border-b-2 border-indigo-600'
                      : 'text-gray-600 hover:text-gray-800'
                  }`}
                >
                  {tab.toUpperCase()}
                </button>
              ))}
            </div>

            {/* Code Content */}
            <div className="flex-1 overflow-auto bg-gray-900">
              <pre className="p-4 text-sm">
                <code className="text-gray-100">
                  {activeTab === 'html' && parsedCode.html
                    ? parsedCode.html
                    : activeTab === 'css' && parsedCode.css
                      ? parsedCode.css
                      : activeTab === 'js' && parsedCode.js
                        ? parsedCode.js
                        : `// No ${activeTab.toUpperCase()} code found`}
                </code>
              </pre>
            </div>

            {/* Modal Footer */}
            <div className="px-6 py-4 border-t border-gray-200 bg-gray-50">
              <p className="text-xs text-gray-500">
                Code is read-only. This is the visualizer code retrieved from the
                backend.
              </p>
            </div>
          </div>
        </div>
      )}
    </>
  )
}

export default Visualizer
