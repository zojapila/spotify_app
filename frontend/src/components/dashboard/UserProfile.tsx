import Image from 'next/image'
import { ISpotifyUser } from '@/types/spotify'

interface UserProfileProps {
  user: ISpotifyUser
}

export function UserProfile({ user }: UserProfileProps) {
  const imageUrl = user.images?.[0]?.url

  return (
    <div className="flex items-center gap-3">
      {imageUrl ? (
        <Image
          src={imageUrl}
          alt={user.display_name || 'User'}
          width={40}
          height={40}
          className="rounded-full"
        />
      ) : (
        <div className="w-10 h-10 rounded-full bg-spotify-gray flex items-center justify-center">
          <span className="text-white text-sm">
            {user.display_name?.charAt(0) || '?'}
          </span>
        </div>
      )}
      <div className="hidden sm:block">
        <p className="text-white font-medium text-sm">
          {user.display_name || 'Użytkownik'}
        </p>
        {user.product && (
          <p className="text-spotify-lightgray text-xs capitalize">
            {user.product}
          </p>
        )}
      </div>
    </div>
  )
}
