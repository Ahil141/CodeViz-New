import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import homeBg from './assets/Home.jpeg';

export const Home = () => {
    const navigate = useNavigate();

    return (
        <div className="min-h-screen bg-[#020617] text-white overflow-hidden relative selection:bg-blue-500/30 flex flex-col justify-center items-center font-sans">
            {/* Cinematic Background Layer */}
            <div className="absolute inset-0 z-0 overflow-hidden pointer-events-none select-none">
                {/* Background Image */}
                <div
                    className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-40 blur-[1px]"
                    style={{ backgroundImage: `url(${homeBg})` }}
                ></div>

                {/* Cinematic Overlays */}
                <div className="absolute inset-0 bg-[#020617]/60"></div>
                <div className="absolute inset-0 bg-gradient-to-b from-[#020617]/50 via-transparent to-[#020617]"></div>

                {/* Grid for tech feel */}
                <div className="absolute inset-0 bg-grid-slate-900/[0.04] bg-[bottom_1px_center]"></div>

                {/* Subtle Neon Aura around center */}
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-blue-600/10 rounded-full blur-[120px]"></div>
            </div>

            {/* Main Content (Centered) */}
            <main className="relative z-10 flex flex-col items-center justify-center text-center px-4 -mt-10">
                {/* Title Section */}
                <motion.div
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ duration: 1.2, ease: "easeOut" }}
                >
                    <h1
                        className="text-[6rem] md:text-[10rem] font-normal tracking-tight mb-4 select-none leading-none"
                        style={{
                            fontFamily: "var(--font-futuristic)",
                            color: "#ffffff",
                            filter: "drop-shadow(0 0 10px rgba(59, 130, 246, 0.8)) drop-shadow(0 0 30px rgba(59, 130, 246, 0.4)) drop-shadow(0 0 60px rgba(59, 130, 246, 0.2))"
                        }}
                    >
                        CodeViz
                    </h1>
                </motion.div>

                {/* Subtitle Section */}
                <motion.p
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, delay: 0.6 }}
                    className="text-lg md:text-2xl text-slate-200/90 font-light tracking-wide max-w-3xl mb-16"
                >
                    Ask. Explain. Visualize. Your AI-powered code companion.
                </motion.p>

                {/* Button Section */}
                <motion.div
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.8, delay: 1.0 }}
                >
                    <button
                        onClick={() => navigate('/chat')}
                        className="group relative px-12 py-5 rounded-3xl font-normal text-xl tracking-wider transition-all duration-500 overflow-hidden"
                    >
                        {/* Glassmorphism Background */}
                        <div className="absolute inset-0 bg-blue-500/5 backdrop-blur-md border border-white/20 rounded-3xl transition-all group-hover:bg-blue-500/10 group-hover:border-white/40"></div>

                        {/* Glow effect */}
                        <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500 shadow-[0_0_30px_rgba(59,130,246,0.3)] rounded-3xl"></div>

                        <span className="relative z-10 text-white group-hover:text-blue-200 transition-colors flex items-center gap-3">
                            Start Chatting
                        </span>
                    </button>
                </motion.div>
            </main>

            {/* Micro-footer for extra cinematic feel */}
            <div className="absolute bottom-10 left-0 right-0 z-10 flex flex-col items-center gap-2 opacity-30 select-none hidden md:flex">
                <div className="w-0.5 h-12 bg-gradient-to-b from-blue-500/50 to-transparent"></div>
                <span className="text-[10px] tracking-[0.4em] font-light uppercase">State of the Art AI</span>
            </div>

            <style>{`
                .font-futuristic {
                    font-family: var(--font-futuristic);
                }
            `}</style>
        </div>
    );
};
