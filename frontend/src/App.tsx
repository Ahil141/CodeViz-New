import { useState } from "react"
import Sidebar, { Page } from "./components/Sidebar"
import Home from "./pages/Home"
import LearnDS from "./pages/LearnDS"

function App() {
  const [currentPage, setCurrentPage] = useState<Page>("home")

  const renderPage = () => {
    switch (currentPage) {
      case "home":
        return <Home />
      case "learn-ds":
        return <LearnDS />
      default:
        return <Home />
    }
  }

  return (
    <div className="h-screen bg-gray-50 flex overflow-hidden">
      <Sidebar
        currentPage={currentPage}
        onPageChange={setCurrentPage}
      />
      <main className="flex-1 overflow-hidden">
        {renderPage()}
      </main>
    </div>
  )
}

export default App
