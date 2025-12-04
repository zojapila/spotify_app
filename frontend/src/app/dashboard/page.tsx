'use client'

import { useEffect, useState, Suspense } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import { UserProfile } from '@/components/dashboard/UserProfile'
import { TopArtists } from '@/components/dashboard/TopArtists'
import { TopTracks } from '@/components/dashboard/TopTracks'
import { TopAlbums } from '@/components/dashboard/TopAlbums'
import { RecentlyPlayed } from '@/components/dashboard/RecentlyPlayed'
import { Navigation } from '@/components/dashboard/Navigation'
import { SettingsModal } from '@/components/ui/SettingsModal'
import { ISpotifyUser } from '@/types/spotify'
import { getApiUrl, getApiHeaders } from '@/lib/api'

type TabType = 'artists' | 'tracks' | 'albums' | 'recent'

function DashboardContent() {
  const searchParams = useSearchParams()
  const router = useRouter()
  
  const [accessToken, setAccessToken] = useState<string | null>(null)
  const [user, setUser] = useState<ISpotifyUser | null>(null)
  const [activeTab, setActiveTab] = useState<TabType>('artists')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showSettings, setShowSettings] = useState(false)

  useEffect(() => {
    // Get tokens from URL params (from OAuth callback)
    const token = searchParams.get('access_token')
    const refreshToken = searchParams.get('refresh_token')
    
    if (token) {
      // Store tokens
      localStorage.setItem('spotify_access_token', token)
      if (refreshToken) {
        localStorage.setItem('spotify_refresh_token', refreshToken)
      }
      setAccessToken(token)
      
      // Clean URL
      router.replace('/dashboard')
    } else {
      // Try to get from localStorage
      const storedToken = localStorage.getItem('spotify_access_token')
      if (storedToken) {
        setAccessToken(storedToken)
      } else {
        router.push('/login')
      }
    }
  }, [searchParams, router])

  useEffect(() => {
    if (!accessToken) return

    const fetchUser = async () => {
      const apiUrl = getApiUrl()
      try {
        const response = await fetch(`${apiUrl}/api/spotify/me`, {
          headers: getApiHeaders(accessToken),
        })

        if (!response.ok) {
          if (response.status === 401) {
            // Token expired
            localStorage.removeItem('spotify_access_token')
            router.push('/login')
            return
          }
          throw new Error('Failed to fetch user')
        }

        const data = await response.json()
        setUser(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setLoading(false)
      }
    }

    fetchUser()
  }, [accessToken, router])

  const handleLogout = () => {
    localStorage.removeItem('spotify_access_token')
    localStorage.removeItem('spotify_refresh_token')
    router.push('/login')
  }

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-spotify-green mx-auto mb-4"></div>
          <p className="text-spotify-lightgray">Ładowanie...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <p className="text-red-500 mb-4">Błąd: {error}</p>
          <button
            onClick={() => router.push('/login')}
            className="bg-spotify-green text-white py-2 px-4 rounded-full"
          >
            Zaloguj ponownie
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-spotify-black to-gray-900">
      {/* Settings Modal */}
      <SettingsModal isOpen={showSettings} onClose={() => setShowSettings(false)} />
      
      {/* Header */}
      <header className="bg-spotify-black/90 backdrop-blur-sm z-10 border-b border-gray-800">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold text-white">🎵 Spotify Stats</h1>
          <div className="flex items-center gap-4">
            {user && <UserProfile user={user} />}
            <button
              onClick={() => setShowSettings(true)}
              className="text-spotify-lightgray hover:text-white transition-colors"
              title="Ustawienia"
            >
              ⚙️
            </button>
            <button
              onClick={handleLogout}
              className="text-spotify-lightgray hover:text-white transition-colors"
            >
              Wyloguj
            </button>
          </div>
        </div>
      </header>

      {/* Navigation */}
      <Navigation activeTab={activeTab} onTabChange={setActiveTab} accessToken={accessToken || undefined} />

      {/* Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {activeTab === 'artists' && accessToken && (
          <TopArtists accessToken={accessToken} />
        )}
        {activeTab === 'tracks' && accessToken && (
          <TopTracks accessToken={accessToken} />
        )}
        {activeTab === 'albums' && accessToken && (
          <TopAlbums accessToken={accessToken} />
        )}
        {activeTab === 'recent' && accessToken && (
          <RecentlyPlayed accessToken={accessToken} />
        )}
      </main>
    </div>
  )
}

export default function DashboardPage() {
  return (
    <Suspense fallback={
      <div className="flex min-h-screen items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-spotify-green"></div>
      </div>
    }>
      <DashboardContent />
    </Suspense>
  )
}
