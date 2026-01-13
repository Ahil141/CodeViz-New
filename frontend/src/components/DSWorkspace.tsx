import DSChat from './DSChat'
import Visualizer from './Visualizer'

interface DSWorkspaceProps {
  visualizerCode: string | null
  isLoadingVisualizer: boolean
}

function DSWorkspace({
  visualizerCode,
  isLoadingVisualizer,
}: DSWorkspaceProps) {
  return (
    <div className="flex h-full overflow-hidden">
      {/* Left: LLM Chat */}
      <div className="w-1/2 flex-shrink-0">
        <DSChat />
      </div>

      {/* Right: Visualizer */}
      <div className="w-1/2 flex-shrink-0 border-l border-gray-200">
        <Visualizer
          visualizerCode={visualizerCode}
          isLoadingVisualizer={isLoadingVisualizer}
        />
      </div>
    </div>
  )
}

export default DSWorkspace
