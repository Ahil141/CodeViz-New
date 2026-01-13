import { Home, BookOpen, Menu } from "lucide-react"

export type Page = "home" | "learn-ds"

interface SidebarProps {
  currentPage: Page
  onPageChange: (page: Page) => void
}

function Sidebar({ currentPage, onPageChange }: SidebarProps) {
  const menuItems = [
    { id: "home" as Page, label: "Home", icon: Home },
    { id: "learn-ds" as Page, label: "Learn DS", icon: BookOpen },
  ]

  return (
    <aside className="w-64 bg-white border-r border-gray-200 flex flex-col h-screen sticky top-0">
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center gap-2">
          <Menu className="w-6 h-6 text-indigo-600" />
          <h1 className="text-xl font-bold text-gray-800">
            CodeViz
          </h1>
        </div>
      </div>

      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          {menuItems.map((item) => {
            const Icon = item.icon
            const isActive = currentPage === item.id

            return (
              <li key={item.id}>
                <button
                  onClick={() => onPageChange(item.id)}
                  className={`
                    w-full flex items-center gap-3 px-4 py-3 rounded-lg
                    transition-colors duration-200
                    ${isActive
                      ? "bg-indigo-50 text-indigo-700 font-medium"
                      : "text-gray-700 hover:bg-gray-50"
                    }
                  `}
                >
                  <Icon
                    className={`w-5 h-5 ${isActive ? "text-indigo-600" : "text-gray-500"
                      }`}
                  />
                  <span>{item.label}</span>
                </button>
              </li>
            )
          })}
        </ul>
      </nav>
    </aside>
  )
}

export default Sidebar
