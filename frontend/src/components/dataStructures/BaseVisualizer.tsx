import type { ReactNode } from 'react';
import { AnimatePresence } from 'framer-motion';
import { Controls } from './Controls';

interface BaseVisualizerProps {
    title: string;
    description?: string;
    children: ReactNode;
    currentStep: number;
    totalSteps: number;
    isPlaying: boolean;
    onPlayPause: () => void;
    onNext: () => void;
    onPrev: () => void;
    onReset: () => void;
    speed: number;
    onSpeedChange: (speed: number) => void;
    explanation?: string; // Optional explanation for the current step
}

export const BaseVisualizer = ({
    title,
    description,
    children,
    currentStep,
    totalSteps,
    isPlaying,
    onPlayPause,
    onNext,
    onPrev,
    onReset,
    speed,
    onSpeedChange,
    explanation
}: BaseVisualizerProps) => {
    return (
        <div className="flex flex-col h-full bg-slate-50">
            {/* Header */}
            <div className="px-6 py-4 bg-white border-b border-gray-200">
                <h3 className="text-lg font-bold text-gray-800">{title}</h3>
                {description && (
                    <p className="text-sm text-gray-500 mt-1">{description}</p>
                )}
            </div>

            {/* Content Area */}
            <div className={`flex-1 p-6 overflow-hidden flex flex-col items-center justify-center relative ${explanation ? 'mb-20' : ''}`}>
                <AnimatePresence mode="wait">
                    {children}
                </AnimatePresence>
            </div>

            {/* Step Explanation Panel */}
            {explanation && (
                <div className="absolute bottom-0 left-0 w-full bg-blue-50 border-t border-blue-100 p-4 text-center">
                    <p className="text-blue-900 font-medium animate-pulse-once">
                        {explanation}
                    </p>
                </div>
            )}

            {/* Controls */}
            <Controls
                currentStep={currentStep}
                totalSteps={totalSteps}
                isPlaying={isPlaying}
                onPlayPause={onPlayPause}
                onNext={onNext}
                onPrev={onPrev}
                onReset={onReset}
                speed={speed}
                onSpeedChange={onSpeedChange}
            />
        </div>
    );
};
