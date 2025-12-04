type TabType = 'artists' | 'tracks' | 'albums' | 'recent'

interface NavigationProps {
  activeTab: TabType
  onTabChange: (tab: TabType) => void
}

const tabs: { id: TabType; label: string; icon: string }[] = [
  { id: 'artists', label: 'Top Artyści', icon: '🎤' },
  { id: 'tracks', label: 'Top Utwory', icon: '🎵' },
  { id: 'albums', label: 'Top Albumy', icon: '💿' },
  { id: 'recent', label: 'Ostatnio słuchane', icon: '🕐' },
]

export function Navigation({ activeTab, onTabChange }: NavigationProps) {
  return (
    <nav className="border-b border-gray-800">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex gap-1 overflow-x-auto">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`px-4 py-3 text-sm font-medium whitespace-nowrap transition-colors ${
                activeTab === tab.id
                  ? 'text-white border-b-2 border-spotify-green'
                  : 'text-spotify-lightgray hover:text-white'
              }`}
            >
              <span className="mr-2">{tab.icon}</span>
              {tab.label}
            </button>
          ))}
        </div>
      </div>
    </nav>
  )
}
