import { useState } from "react"
import Sidebar, { Page } from "./components/Sidebar"
import Home from "./pages/Home"
import LearnDS from "./pages/LearnDS"
import SmartChat from "./pages/SmartChat"

function App() {
  const [currentPage, setCurrentPage] = useState<Page>("smart-chat")

  const renderPage = () => {
    switch (currentPage) {
      case "smart-chat":
        return <SmartChat />
      case "home":
        return <Home />
      case "learn-ds":
        return <LearnDS />
      default:
        return <SmartChat />
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
