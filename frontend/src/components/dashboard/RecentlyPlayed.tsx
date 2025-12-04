'use client'

import { useState, useEffect } from 'react'
import Image from 'next/image'
import { IPlayHistoryItem, IRecentlyPlayedResponse } from '@/types/spotify'
import { LoadingSpinner } from '@/components/ui/LoadingSpinner'
import { formatDuration, formatRelativeTime } from '@/lib/utils'
import { getApiUrl, getApiHeaders } from '@/lib/api'

interface RecentlyPlayedProps {
  accessToken: string
}

export function RecentlyPlayed({ accessToken }: RecentlyPlayedProps) {
  const [items, setItems] = useState<IPlayHistoryItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchRecentlyPlayed = async () => {
      setLoading(true)
      setError(null)

      try {
        const response = await fetch(
          `${getApiUrl()}/api/spotify/recently-played?limit=50`,
          {
            headers: getApiHeaders(accessToken),
          }
        )

        if (!response.ok) {
          throw new Error('Nie udało się pobrać historii')
        }

        const data: IRecentlyPlayedResponse = await response.json()
        setItems(data.items)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Nieznany błąd')
      } finally {
        setLoading(false)
      }
    }

    fetchRecentlyPlayed()
  }, [accessToken])

  return (
    <div>
      <h2 className="text-2xl font-bold text-white mb-4">Ostatnio słuchane</h2>
      <p className="text-spotify-lightgray text-sm mb-6">
        Ostatnie 50 odtworzonych utworów (limit Spotify API)
      </p>

      {loading && <LoadingSpinner />}
      
      {error && (
        <p className="text-red-500 text-center py-4">{error}</p>
      )}

      {!loading && !error && (
        <div className="space-y-2">
          {items.map((item, index) => (
            <RecentTrackCard key={`${item.track.id}-${index}`} item={item} />
          ))}
        </div>
      )}

      {!loading && !error && items.length === 0 && (
        <p className="text-spotify-lightgray text-center py-8">
          Brak historii słuchania
        </p>
      )}
    </div>
  )
}

interface RecentTrackCardProps {
  item: IPlayHistoryItem
}

function RecentTrackCard({ item }: RecentTrackCardProps) {
  const { track, played_at } = item
  const imageUrl = track.album.images?.[0]?.url
  const artistNames = track.artists.map((a) => a.name).join(', ')

  return (
    <a
      href={track.external_urls?.spotify || '#'}
      target="_blank"
      rel="noopener noreferrer"
      className="flex items-center gap-4 bg-gray-800/50 rounded-lg p-3 hover:bg-gray-800 transition-colors group"
    >
      <div className="relative w-12 h-12 flex-shrink-0">
        {imageUrl ? (
          <Image
            src={imageUrl}
            alt={track.album.name}
            fill
            className="object-cover rounded"
            sizes="48px"
          />
        ) : (
          <div className="w-full h-full bg-gray-700 rounded flex items-center justify-center">
            🎵
          </div>
        )}
      </div>
      
      <div className="flex-1 min-w-0">
        <h3 className="text-white font-medium truncate group-hover:text-spotify-green transition-colors">
          {track.name}
        </h3>
        <p className="text-spotify-lightgray text-sm truncate">
          {artistNames}
        </p>
      </div>
      
      <div className="text-right">
        <p className="text-spotify-lightgray text-sm">
          {formatDuration(track.duration_ms)}
        </p>
        <p className="text-spotify-gray text-xs">
          {formatRelativeTime(played_at)}
        </p>
      </div>
    </a>
  )
}
