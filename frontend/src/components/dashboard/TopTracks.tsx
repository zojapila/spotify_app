'use client'

import { useState, useEffect } from 'react'
import Image from 'next/image'
import { ISpotifyTrack, ITopTracksResponse, TimeRange } from '@/types/spotify'
import { TimeRangeSelector } from '@/components/ui/TimeRangeSelector'
import { LoadingSpinner } from '@/components/ui/LoadingSpinner'
import { formatDuration } from '@/lib/utils'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface TopTracksProps {
  accessToken: string
}

export function TopTracks({ accessToken }: TopTracksProps) {
  const [tracks, setTracks] = useState<ISpotifyTrack[]>([])
  const [timeRange, setTimeRange] = useState<TimeRange>('medium_term')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchTracks = async () => {
      setLoading(true)
      setError(null)

      try {
        const response = await fetch(
          `${API_URL}/api/spotify/top/tracks?time_range=${timeRange}&limit=20`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        )

        if (!response.ok) {
          throw new Error('Nie udało się pobrać utworów')
        }

        const data: ITopTracksResponse = await response.json()
        setTracks(data.items)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Nieznany błąd')
      } finally {
        setLoading(false)
      }
    }

    fetchTracks()
  }, [accessToken, timeRange])

  return (
    <div>
      <h2 className="text-2xl font-bold text-white mb-4">Top Utwory</h2>
      
      <TimeRangeSelector value={timeRange} onChange={setTimeRange} />

      {loading && <LoadingSpinner />}
      
      {error && (
        <p className="text-red-500 text-center py-4">{error}</p>
      )}

      {!loading && !error && (
        <div className="space-y-2">
          {tracks.map((track, index) => (
            <TrackCard key={track.id} track={track} rank={index + 1} />
          ))}
        </div>
      )}

      {!loading && !error && tracks.length === 0 && (
        <p className="text-spotify-lightgray text-center py-8">
          Brak danych o utworach dla tego okresu
        </p>
      )}
    </div>
  )
}

interface TrackCardProps {
  track: ISpotifyTrack
  rank: number
}

function TrackCard({ track, rank }: TrackCardProps) {
  const imageUrl = track.album.images?.[0]?.url
  const artistNames = track.artists.map((a) => a.name).join(', ')

  return (
    <a
      href={track.external_urls?.spotify || '#'}
      target="_blank"
      rel="noopener noreferrer"
      className="flex items-center gap-4 bg-gray-800/50 rounded-lg p-3 hover:bg-gray-800 transition-colors group"
    >
      <span className="text-spotify-lightgray font-medium w-6 text-center">
        {rank}
      </span>
      
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
      
      <div className="hidden sm:block text-spotify-lightgray text-sm">
        {track.album.name}
      </div>
      
      <div className="text-spotify-lightgray text-sm">
        {formatDuration(track.duration_ms)}
      </div>
    </a>
  )
}
