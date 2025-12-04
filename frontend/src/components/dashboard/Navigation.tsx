'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

type TabType = 'artists' | 'tracks' | 'albums' | 'recent'

interface NavigationProps {
  activeTab?: TabType
  onTabChange?: (tab: TabType) => void
  accessToken?: string
}

const tabs: { id: TabType; label: string; icon: string }[] = [
  { id: 'artists', label: 'Top Artyści', icon: '🎤' },
  { id: 'tracks', label: 'Top Utwory', icon: '🎵' },
  { id: 'albums', label: 'Top Albumy', icon: '💿' },
  { id: 'recent', label: 'Ostatnio słuchane', icon: '🕐' },
]

export function Navigation({ activeTab, onTabChange, accessToken }: NavigationProps) {
  const pathname = usePathname();
  const isAnalytics = pathname === '/analytics';
  const isDashboard = pathname === '/dashboard';

  return (
    <nav className="border-b border-gray-800 bg-gray-900/50 backdrop-blur-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between">
          {/* Main navigation */}
          <div className="flex gap-1">
            <Link
              href={accessToken ? `/dashboard?access_token=${accessToken}` : '/dashboard'}
              className={`px-4 py-3 text-sm font-medium whitespace-nowrap transition-colors ${
                isDashboard
                  ? 'text-white border-b-2 border-spotify-green'
                  : 'text-spotify-lightgray hover:text-white'
              }`}
            >
              🏠 Dashboard
            </Link>
            <Link
              href={accessToken ? `/analytics?access_token=${accessToken}` : '/analytics'}
              className={`px-4 py-3 text-sm font-medium whitespace-nowrap transition-colors ${
                isAnalytics
                  ? 'text-white border-b-2 border-spotify-green'
                  : 'text-spotify-lightgray hover:text-white'
              }`}
            >
              📊 Analityka
            </Link>
          </div>

          {/* Tab navigation (only on dashboard) */}
          {isDashboard && onTabChange && (
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
          )}
        </div>
      </div>
    </nav>
  )
}
