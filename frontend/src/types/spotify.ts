/**
 * Spotify API types
 */

export interface ISpotifyImage {
  url: string
  height: number | null
  width: number | null
}

export interface ISpotifyUser {
  id: string
  display_name: string | null
  email: string | null
  images: ISpotifyImage[]
  product: string | null
  followers: {
    total: number
  } | null
  external_urls: {
    spotify: string
  } | null
}

export interface ISpotifyArtist {
  id: string
  name: string
  genres: string[]
  popularity: number | null
  images: ISpotifyImage[]
  external_urls: {
    spotify: string
  } | null
  followers?: {
    total: number
  } | null
}

export interface ISpotifyArtistSimple {
  id: string
  name: string
  external_urls?: {
    spotify: string
  } | null
}

export interface ISpotifyAlbumSimple {
  id: string
  name: string
  images: ISpotifyImage[]
  release_date: string | null
  external_urls?: {
    spotify: string
  } | null
}

export interface ISpotifyTrack {
  id: string
  name: string
  duration_ms: number
  popularity: number | null
  album: ISpotifyAlbumSimple
  artists: ISpotifyArtistSimple[]
  external_urls: {
    spotify: string
  } | null
  preview_url: string | null
}

export interface ISpotifyAlbum {
  id: string
  name: string
  artists: ISpotifyArtistSimple[]
  images: ISpotifyImage[]
  release_date: string | null
  total_tracks: number | null
  track_count_in_top: number
  external_urls: {
    spotify: string
  } | null
}

export interface ITopArtistsResponse {
  items: ISpotifyArtist[]
  total: number
  limit: number
  offset: number
  time_range: string
}

export interface ITopTracksResponse {
  items: ISpotifyTrack[]
  total: number
  limit: number
  offset: number
  time_range: string
}

export interface ITopAlbumsResponse {
  items: ISpotifyAlbum[]
  total: number
  limit: number
  time_range: string
}

export interface IPlayHistoryItem {
  track: ISpotifyTrack
  played_at: string
}

export interface IRecentlyPlayedResponse {
  items: IPlayHistoryItem[]
  total: number
}

export type TimeRange = 'short_term' | 'medium_term' | 'long_term'

export const TIME_RANGE_LABELS: Record<TimeRange, string> = {
  short_term: 'Ostatni miesiąc',
  medium_term: 'Ostatnie 6 miesięcy',
  long_term: 'Wszystkie czasy',
}
