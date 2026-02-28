import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Home } from './Home';
import { CodeViz } from './CodeViz';
import { VisualizationProvider } from './VisualizationController';

function App() {
  return (
    <Router>
      <VisualizationProvider>
        <div className="min-h-screen">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/chat" element={<CodeViz />} />
          </Routes>
        </div>
      </VisualizationProvider>
    </Router>
  );
}

export default App;
