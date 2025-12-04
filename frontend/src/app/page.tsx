import Link from 'next/link'

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="text-center">
        <h1 className="text-5xl font-bold text-white mb-4">
          🎵 Spotify Stats
        </h1>
        <p className="text-spotify-lightgray text-xl mb-8">
          Odkryj swoje statystyki słuchania muzyki
        </p>
        <Link
          href="/login"
          className="inline-block bg-spotify-green text-white font-bold py-4 px-8 rounded-full hover:bg-green-400 transition-colors text-lg"
        >
          Rozpocznij
        </Link>
      </div>
    </main>
  )
}
