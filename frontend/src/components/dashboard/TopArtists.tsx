'use client'

import { useState, useEffect } from 'react'
import Image from 'next/image'
import { ISpotifyArtist, ITopArtistsResponse, TimeRange } from '@/types/spotify'
import { TimeRangeSelector } from '@/components/ui/TimeRangeSelector'
import { LoadingSpinner } from '@/components/ui/LoadingSpinner'
import { getApiUrl } from '@/lib/api'

interface TopArtistsProps {
  accessToken: string
}

export function TopArtists({ accessToken }: TopArtistsProps) {
  const [artists, setArtists] = useState<ISpotifyArtist[]>([])
  const [timeRange, setTimeRange] = useState<TimeRange>('medium_term')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchArtists = async () => {
      setLoading(true)
      setError(null)

      try {
        const response = await fetch(
          `${getApiUrl()}/api/spotify/top/artists?time_range=${timeRange}&limit=20`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        )

        if (!response.ok) {
          throw new Error('Nie udało się pobrać artystów')
        }

        const data: ITopArtistsResponse = await response.json()
        setArtists(data.items)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Nieznany błąd')
      } finally {
        setLoading(false)
      }
    }

    fetchArtists()
  }, [accessToken, timeRange])

  return (
    <div>
      <h2 className="text-2xl font-bold text-white mb-4">Top Artyści</h2>
      
      <TimeRangeSelector value={timeRange} onChange={setTimeRange} />

      {loading && <LoadingSpinner />}
      
      {error && (
        <p className="text-red-500 text-center py-4">{error}</p>
      )}

      {!loading && !error && (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          {artists.map((artist, index) => (
            <ArtistCard key={artist.id} artist={artist} rank={index + 1} />
          ))}
        </div>
      )}

      {!loading && !error && artists.length === 0 && (
        <p className="text-spotify-lightgray text-center py-8">
          Brak danych o artystach dla tego okresu
        </p>
      )}
    </div>
  )
}

interface ArtistCardProps {
  artist: ISpotifyArtist
  rank: number
}

function ArtistCard({ artist, rank }: ArtistCardProps) {
  const imageUrl = artist.images?.[0]?.url

  return (
    <a
      href={artist.external_urls?.spotify || '#'}
      target="_blank"
      rel="noopener noreferrer"
      className="group bg-gray-800/50 rounded-lg p-4 hover:bg-gray-800 transition-colors"
    >
      <div className="relative mb-4">
        <div className="aspect-square relative rounded-full overflow-hidden bg-gray-700">
          {imageUrl ? (
            <Image
              src={imageUrl}
              alt={artist.name}
              fill
              className="object-cover"
              sizes="(max-width: 640px) 50vw, (max-width: 768px) 33vw, 20vw"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-4xl">
              🎤
            </div>
          )}
        </div>
        <span className="absolute -top-2 -left-2 bg-spotify-green text-white text-sm font-bold w-8 h-8 rounded-full flex items-center justify-center">
          {rank}
        </span>
      </div>
      
      <h3 className="text-white font-medium truncate group-hover:text-spotify-green transition-colors">
        {artist.name}
      </h3>
      
      {artist.genres.length > 0 && (
        <p className="text-spotify-lightgray text-sm truncate">
          {artist.genres.slice(0, 2).join(', ')}
        </p>
      )}
    </a>
  )
}
