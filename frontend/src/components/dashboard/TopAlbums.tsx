'use client'

import { useState, useEffect } from 'react'
import Image from 'next/image'
import { ISpotifyAlbum, ITopAlbumsResponse, TimeRange } from '@/types/spotify'
import { TimeRangeSelector } from '@/components/ui/TimeRangeSelector'
import { LoadingSpinner } from '@/components/ui/LoadingSpinner'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface TopAlbumsProps {
  accessToken: string
}

export function TopAlbums({ accessToken }: TopAlbumsProps) {
  const [albums, setAlbums] = useState<ISpotifyAlbum[]>([])
  const [timeRange, setTimeRange] = useState<TimeRange>('medium_term')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchAlbums = async () => {
      setLoading(true)
      setError(null)

      try {
        const response = await fetch(
          `${API_URL}/api/spotify/top/albums?time_range=${timeRange}&limit=20`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          }
        )

        if (!response.ok) {
          throw new Error('Nie udało się pobrać albumów')
        }

        const data: ITopAlbumsResponse = await response.json()
        setAlbums(data.items)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Nieznany błąd')
      } finally {
        setLoading(false)
      }
    }

    fetchAlbums()
  }, [accessToken, timeRange])

  return (
    <div>
      <h2 className="text-2xl font-bold text-white mb-4">Top Albumy</h2>
      <p className="text-spotify-lightgray text-sm mb-4">
        Na podstawie Twoich najczęściej słuchanych utworów
      </p>
      
      <TimeRangeSelector value={timeRange} onChange={setTimeRange} />

      {loading && <LoadingSpinner />}
      
      {error && (
        <p className="text-red-500 text-center py-4">{error}</p>
      )}

      {!loading && !error && (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
          {albums.map((album, index) => (
            <AlbumCard key={album.id} album={album} rank={index + 1} />
          ))}
        </div>
      )}

      {!loading && !error && albums.length === 0 && (
        <p className="text-spotify-lightgray text-center py-8">
          Brak danych o albumach dla tego okresu
        </p>
      )}
    </div>
  )
}

interface AlbumCardProps {
  album: ISpotifyAlbum
  rank: number
}

function AlbumCard({ album, rank }: AlbumCardProps) {
  const imageUrl = album.images?.[0]?.url
  const artistNames = album.artists.map((a) => a.name).join(', ')

  return (
    <a
      href={album.external_urls?.spotify || '#'}
      target="_blank"
      rel="noopener noreferrer"
      className="group bg-gray-800/50 rounded-lg p-4 hover:bg-gray-800 transition-colors"
    >
      <div className="relative mb-4">
        <div className="aspect-square relative rounded overflow-hidden bg-gray-700 shadow-lg">
          {imageUrl ? (
            <Image
              src={imageUrl}
              alt={album.name}
              fill
              className="object-cover"
              sizes="(max-width: 640px) 50vw, (max-width: 768px) 33vw, 20vw"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-4xl">
              💿
            </div>
          )}
        </div>
        <span className="absolute -top-2 -left-2 bg-spotify-green text-white text-sm font-bold w-8 h-8 rounded-full flex items-center justify-center">
          {rank}
        </span>
      </div>
      
      <h3 className="text-white font-medium truncate group-hover:text-spotify-green transition-colors">
        {album.name}
      </h3>
      
      <p className="text-spotify-lightgray text-sm truncate">
        {artistNames}
      </p>
      
      {album.track_count_in_top > 0 && (
        <p className="text-spotify-green text-xs mt-1">
          {album.track_count_in_top} {album.track_count_in_top === 1 ? 'utwór' : 'utworów'} w top
        </p>
      )}
    </a>
  )
}
