import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { CodeViz } from './pages/CodeViz';
import { VisualizationProvider } from './services/VisualizationController';

function App() {
  return (
    <Router>
      <VisualizationProvider>
        <div className="min-h-screen">
          <Routes>
            <Route path="/" element={<CodeViz />} />
          </Routes>
        </div>
      </VisualizationProvider>
    </Router>
  );
}

export default App;
