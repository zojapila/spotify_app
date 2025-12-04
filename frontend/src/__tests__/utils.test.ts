import { formatDuration, formatDurationLong, formatRelativeTime } from '@/lib/utils'

describe('formatDuration', () => {
  it('formats milliseconds to MM:SS', () => {
    expect(formatDuration(180000)).toBe('3:00')
    expect(formatDuration(215000)).toBe('3:35')
    expect(formatDuration(60000)).toBe('1:00')
    expect(formatDuration(45000)).toBe('0:45')
  })

  it('pads seconds with zero', () => {
    expect(formatDuration(65000)).toBe('1:05')
    expect(formatDuration(3000)).toBe('0:03')
  })
})

describe('formatDurationLong', () => {
  it('formats minutes only', () => {
    expect(formatDurationLong(1800000)).toBe('30m')
    expect(formatDurationLong(300000)).toBe('5m')
  })

  it('formats hours and minutes', () => {
    expect(formatDurationLong(5400000)).toBe('1h 30m')
    expect(formatDurationLong(9000000)).toBe('2h 30m')
  })
})

describe('formatRelativeTime', () => {
  it('returns "Przed chwilą" for less than a minute', () => {
    const now = new Date().toISOString()
    expect(formatRelativeTime(now)).toBe('Przed chwilą')
  })

  it('returns minutes for less than an hour', () => {
    const thirtyMinutesAgo = new Date(Date.now() - 30 * 60 * 1000).toISOString()
    expect(formatRelativeTime(thirtyMinutesAgo)).toBe('30 min temu')
  })

  it('returns hours for less than a day', () => {
    const twoHoursAgo = new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString()
    expect(formatRelativeTime(twoHoursAgo)).toBe('2 godziny temu')
  })

  it('returns days for less than a week', () => {
    const threeDaysAgo = new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString()
    expect(formatRelativeTime(threeDaysAgo)).toBe('3 dni temu')
  })
})
