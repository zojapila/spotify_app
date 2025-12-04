import { TimeRange, TIME_RANGE_LABELS } from '@/types/spotify'

interface TimeRangeSelectorProps {
  value: TimeRange
  onChange: (range: TimeRange) => void
}

export function TimeRangeSelector({ value, onChange }: TimeRangeSelectorProps) {
  const ranges: TimeRange[] = ['short_term', 'medium_term', 'long_term']

  return (
    <div className="flex gap-2 mb-6">
      {ranges.map((range) => (
        <button
          key={range}
          onClick={() => onChange(range)}
          className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
            value === range
              ? 'bg-spotify-green text-white'
              : 'bg-gray-800 text-spotify-lightgray hover:text-white'
          }`}
        >
          {TIME_RANGE_LABELS[range]}
        </button>
      ))}
    </div>
  )
}
