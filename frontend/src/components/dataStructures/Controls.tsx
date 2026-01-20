import { Play, Pause, ChevronLeft, ChevronRight, RotateCcw } from 'lucide-react';

interface ControlsProps {
    currentStep: number;
    totalSteps: number;
    isPlaying: boolean;
    onPlayPause: () => void;
    onNext: () => void;
    onPrev: () => void;
    onReset: () => void;
    speed: number;
    onSpeedChange: (speed: number) => void;
}

export const Controls = ({
    currentStep,
    totalSteps,
    isPlaying,
    onPlayPause,
    onNext,
    onPrev,
    onReset,
    speed,
    onSpeedChange,
}: ControlsProps) => {
    return (
        <div className="flex flex-col gap-2 p-4 bg-white border-t border-gray-200">
            {/* Progress Bar */}
            <div className="w-full h-1.5 bg-gray-100 rounded-full overflow-hidden">
                <div
                    className="h-full bg-blue-600 transition-all duration-300 ease-out"
                    style={{ width: `${((currentStep + 1) / totalSteps) * 100}%` }}
                />
            </div>

            <div className="flex items-center justify-between mt-2">
                {/* Playback Controls */}
                <div className="flex items-center gap-2">
                    <button
                        onClick={onReset}
                        className="p-1.5 hover:bg-gray-100 rounded-md text-gray-600 transition-colors"
                        title="Reset"
                    >
                        <RotateCcw className="w-4 h-4" />
                    </button>

                    <div className="w-px h-4 bg-gray-200 mx-1" />

                    <button
                        onClick={onPrev}
                        disabled={currentStep === 0}
                        className="p-1.5 hover:bg-gray-100 rounded-md text-gray-600 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                    >
                        <ChevronLeft className="w-5 h-5" />
                    </button>

                    <button
                        onClick={onPlayPause}
                        className="p-2 bg-blue-600 hover:bg-blue-700 rounded-full text-white shadow-sm transition-colors"
                    >
                        {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4 ml-0.5" />}
                    </button>

                    <button
                        onClick={onNext}
                        disabled={currentStep === totalSteps - 1}
                        className="p-1.5 hover:bg-gray-100 rounded-md text-gray-600 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                    >
                        <ChevronRight className="w-5 h-5" />
                    </button>
                </div>

                {/* Speed Control */}
                <div className="flex items-center gap-2">
                    <span className="text-xs text-gray-400 font-medium">SPEED</span>
                    <select
                        value={speed}
                        onChange={(e) => onSpeedChange(Number(e.target.value))}
                        className="text-xs bg-gray-50 border border-gray-200 rounded px-2 py-1 outline-none focus:border-blue-400"
                    >
                        <option value={2000}>Slow</option>
                        <option value={1000}>Normal</option>
                        <option value={500}>Fast</option>
                    </select>
                </div>
            </div>

            <div className="text-center">
                <span className="text-xs text-gray-400">
                    Step {currentStep + 1} of {totalSteps}
                </span>
            </div>
        </div>
    );
};
