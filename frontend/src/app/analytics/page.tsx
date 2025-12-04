'use client';

import { useState, useEffect } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { Navigation } from '@/components/dashboard';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { getApiUrl, getApiHeaders } from '@/lib/api';
import { SettingsModal } from '@/components/ui/SettingsModal';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  LineChart, Line, PieChart, Pie, Cell, AreaChart, Area
} from 'recharts';

interface DailyListening {
  date: string;
  plays: number;
  time_ms: number;
  time_formatted: string;
}

interface HourlyDistribution {
  hour: number;
  plays: number;
  time_ms: number;
  percentage: number;
}

interface WeekdayDistribution {
  day: string;
  day_number: number;
  plays: number;
  time_ms: number;
  percentage: number;
}

interface ListeningStreak {
  current_streak: number;
  longest_streak: number;
  last_listen_date: string | null;
}

interface ListeningTrend {
  current_period_ms: number;
  previous_period_ms: number;
  change_percentage: number;
  trend: string;
}

interface ArtistDiscovery {
  artist_name: string;
  first_listen: string;
  total_plays: number;
  total_time_ms: number;
}

interface Analytics {
  daily_listening: DailyListening[];
  hourly_distribution: HourlyDistribution[];
  weekday_distribution: WeekdayDistribution[];
  streak: ListeningStreak;
  trend: ListeningTrend;
  new_artists: ArtistDiscovery[];
  new_tracks_count: number;
  most_played_hour: number;
  most_played_day: string;
  average_track_length_ms: number;
  listening_variety_score: number;
}

interface MonthlyComparison {
  month: string;
  total_plays: number;
  total_time_ms: number;
  total_time_formatted: string;
  unique_artists: number;
  unique_tracks: number;
  top_artist: string | null;
  top_track: string | null;
}

const COLORS = ['#1DB954', '#1ed760', '#169c46', '#14833b', '#127030'];

function formatTime(ms: number): string {
  const hours = Math.floor(ms / 3600000);
  const minutes = Math.floor((ms % 3600000) / 60000);
  if (hours > 0) return `${hours}h ${minutes}m`;
  return `${minutes}m`;
}

export default function AnalyticsPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [monthly, setMonthly] = useState<MonthlyComparison[]>([]);
  const [loading, setLoading] = useState(true);
  const [days, setDays] = useState(30);
  const [showSettings, setShowSettings] = useState(false);

  useEffect(() => {
    const token = searchParams.get('access_token') || localStorage.getItem('spotify_access_token');
    if (!token) {
      router.push('/login');
      return;
    }
    setAccessToken(token);
    if (searchParams.get('access_token')) {
      localStorage.setItem('spotify_access_token', token);
    }
  }, [searchParams, router]);

  useEffect(() => {
    if (!accessToken) return;
    fetchAnalytics();
  }, [accessToken, days]);

  const fetchAnalytics = async () => {
    if (!accessToken) return;
    setLoading(true);
    
    try {
      const [analyticsRes, monthlyRes] = await Promise.all([
        fetch(`${getApiUrl()}/api/tracking/analytics?days=${days}`, {
          headers: getApiHeaders(accessToken),
        }),
        fetch(`${getApiUrl()}/api/tracking/monthly?months=6`, {
          headers: getApiHeaders(accessToken),
        }),
      ]);

      if (analyticsRes.ok) {
        setAnalytics(await analyticsRes.json());
      }
      if (monthlyRes.ok) {
        setMonthly(await monthlyRes.json());
      }
    } catch (error) {
      console.error('Error fetching analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (!accessToken || loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-900 to-black flex items-center justify-center">
        <LoadingSpinner />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-900 to-black text-white">
      <SettingsModal isOpen={showSettings} onClose={() => setShowSettings(false)} />
      <Navigation accessToken={accessToken} />
      
      <main className="container mx-auto px-4 py-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">📊 Analityka słuchania</h1>
          
          <div className="flex items-center gap-4">
            <select
              value={days}
              onChange={(e) => setDays(Number(e.target.value))}
              className="bg-gray-800 text-white px-4 py-2 rounded-lg border border-gray-700"
            >
              <option value={7}>Ostatnie 7 dni</option>
              <option value={30}>Ostatnie 30 dni</option>
              <option value={90}>Ostatnie 90 dni</option>
              <option value={0}>Wszystkie dane</option>
            </select>
            <button
              onClick={() => setShowSettings(true)}
              className="text-gray-400 hover:text-white transition-colors"
              title="Ustawienia"
            >
              ⚙️
            </button>
          </div>
        </div>

        {!analytics || analytics.daily_listening.length === 0 ? (
          <div className="text-center py-20">
            <p className="text-xl text-gray-400 mb-4">📭 Brak danych do analizy</p>
            <p className="text-gray-500">
              Zacznij słuchać muzyki na Spotify, a dane pojawią się tutaj automatycznie!
            </p>
          </div>
        ) : (
          <>
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
              <StatCard
                icon="🔥"
                label="Obecna passa"
                value={`${analytics.streak.current_streak} dni`}
                sublabel={`Rekord: ${analytics.streak.longest_streak} dni`}
              />
              <StatCard
                icon={analytics.trend.trend === 'up' ? '📈' : analytics.trend.trend === 'down' ? '📉' : '➡️'}
                label="Trend"
                value={`${analytics.trend.change_percentage > 0 ? '+' : ''}${analytics.trend.change_percentage}%`}
                sublabel={`vs poprzedni okres`}
              />
              <StatCard
                icon="🎵"
                label="Nowe utwory"
                value={analytics.new_tracks_count.toString()}
                sublabel={`w tym okresie`}
              />
              <StatCard
                icon="🎨"
                label="Różnorodność"
                value={`${analytics.listening_variety_score}%`}
                sublabel="wynik różnorodności"
              />
            </div>

            {/* Daily Listening Chart */}
            <div className="bg-gray-800/50 rounded-xl p-6 mb-8">
              <h2 className="text-xl font-semibold mb-4">📅 Dzienne słuchanie</h2>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={analytics.daily_listening}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis 
                    dataKey="date" 
                    stroke="#9CA3AF"
                    tickFormatter={(value) => new Date(value).toLocaleDateString('pl-PL', { day: 'numeric', month: 'short' })}
                  />
                  <YAxis stroke="#9CA3AF" />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1F2937', border: 'none', borderRadius: '8px' }}
                    labelFormatter={(value) => new Date(value).toLocaleDateString('pl-PL', { weekday: 'long', day: 'numeric', month: 'long' })}
                    formatter={(value: number, name: string) => [
                      name === 'plays' ? `${value} utworów` : formatTime(value),
                      name === 'plays' ? 'Odtworzenia' : 'Czas'
                    ]}
                  />
                  <Area type="monotone" dataKey="time_ms" stroke="#1DB954" fill="#1DB954" fillOpacity={0.3} name="time" />
                </AreaChart>
              </ResponsiveContainer>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
              {/* Hourly Distribution */}
              <div className="bg-gray-800/50 rounded-xl p-6">
                <h2 className="text-xl font-semibold mb-4">🕐 Godziny słuchania</h2>
                <p className="text-gray-400 text-sm mb-4">
                  Najczęściej słuchasz o <span className="text-green-400 font-semibold">{analytics.most_played_hour}:00</span>
                </p>
                <ResponsiveContainer width="100%" height={250}>
                  <BarChart data={analytics.hourly_distribution}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis dataKey="hour" stroke="#9CA3AF" tickFormatter={(h) => `${h}:00`} />
                    <YAxis stroke="#9CA3AF" />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#1F2937', border: 'none', borderRadius: '8px' }}
                      formatter={(value: number) => [`${value} utworów`, 'Odtworzenia']}
                      labelFormatter={(h) => `${h}:00 - ${h}:59`}
                    />
                    <Bar dataKey="plays" fill="#1DB954" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {/* Weekday Distribution */}
              <div className="bg-gray-800/50 rounded-xl p-6">
                <h2 className="text-xl font-semibold mb-4">📆 Dni tygodnia</h2>
                <p className="text-gray-400 text-sm mb-4">
                  Najbardziej aktywny dzień: <span className="text-green-400 font-semibold">{analytics.most_played_day}</span>
                </p>
                <ResponsiveContainer width="100%" height={250}>
                  <BarChart data={analytics.weekday_distribution} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis type="number" stroke="#9CA3AF" />
                    <YAxis dataKey="day" type="category" stroke="#9CA3AF" width={100} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#1F2937', border: 'none', borderRadius: '8px' }}
                      formatter={(value: number, name: string, props: any) => [
                        `${value} utworów (${props.payload.percentage}%)`,
                        'Odtworzenia'
                      ]}
                    />
                    <Bar dataKey="plays" fill="#1DB954" radius={[0, 4, 4, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Monthly Comparison */}
            {monthly.length > 0 && (
              <div className="bg-gray-800/50 rounded-xl p-6 mb-8">
                <h2 className="text-xl font-semibold mb-4">📊 Porównanie miesięczne</h2>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={[...monthly].reverse()}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis 
                      dataKey="month" 
                      stroke="#9CA3AF"
                      tickFormatter={(m) => {
                        const [year, month] = m.split('-');
                        const date = new Date(parseInt(year), parseInt(month) - 1);
                        return date.toLocaleDateString('pl-PL', { month: 'short' });
                      }}
                    />
                    <YAxis stroke="#9CA3AF" />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#1F2937', border: 'none', borderRadius: '8px' }}
                      formatter={(value: number, name: string) => [
                        name === 'total_plays' ? `${value} utworów` : formatTime(value),
                        name === 'total_plays' ? 'Odtworzenia' : 'Czas słuchania'
                      ]}
                      labelFormatter={(m) => {
                        const [year, month] = m.split('-');
                        const date = new Date(parseInt(year), parseInt(month) - 1);
                        return date.toLocaleDateString('pl-PL', { month: 'long', year: 'numeric' });
                      }}
                    />
                    <Bar dataKey="total_plays" fill="#1DB954" radius={[4, 4, 0, 0]} name="total_plays" />
                  </BarChart>
                </ResponsiveContainer>
                
                {/* Monthly Details Table */}
                <div className="mt-6 overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead>
                      <tr className="text-gray-400 border-b border-gray-700">
                        <th className="text-left py-2">Miesiąc</th>
                        <th className="text-right py-2">Czas</th>
                        <th className="text-right py-2">Utwory</th>
                        <th className="text-right py-2">Artyści</th>
                        <th className="text-left py-2 pl-4">Top artysta</th>
                      </tr>
                    </thead>
                    <tbody>
                      {[...monthly].reverse().map((m) => (
                        <tr key={m.month} className="border-b border-gray-700/50 hover:bg-gray-700/30">
                          <td className="py-2">{m.month}</td>
                          <td className="text-right">{m.total_time_formatted}</td>
                          <td className="text-right">{m.unique_tracks}</td>
                          <td className="text-right">{m.unique_artists}</td>
                          <td className="pl-4 text-green-400">{m.top_artist || '-'}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* New Artists Discovered */}
            {analytics.new_artists.length > 0 && (
              <div className="bg-gray-800/50 rounded-xl p-6">
                <h2 className="text-xl font-semibold mb-4">🆕 Odkryci artyści</h2>
                <p className="text-gray-400 text-sm mb-4">
                  Nowi artyści których zaczęłaś słuchać w tym okresie
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {analytics.new_artists.map((artist, i) => (
                    <div key={artist.artist_name} className="bg-gray-700/50 rounded-lg p-4">
                      <div className="flex items-center gap-3">
                        <span className="text-2xl">{i === 0 ? '🥇' : i === 1 ? '🥈' : i === 2 ? '🥉' : '🎤'}</span>
                        <div>
                          <p className="font-semibold">{artist.artist_name}</p>
                          <p className="text-sm text-gray-400">
                            {artist.total_plays} utworów • {formatTime(artist.total_time_ms)}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </main>
    </div>
  );
}

function StatCard({ icon, label, value, sublabel }: { icon: string; label: string; value: string; sublabel: string }) {
  return (
    <div className="bg-gray-800/50 rounded-xl p-6">
      <div className="flex items-center gap-3 mb-2">
        <span className="text-2xl">{icon}</span>
        <span className="text-gray-400">{label}</span>
      </div>
      <p className="text-3xl font-bold text-green-400">{value}</p>
      <p className="text-sm text-gray-500">{sublabel}</p>
    </div>
  );
}
