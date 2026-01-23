import { Link } from 'react-router-dom'
import { Clock, Euro } from 'lucide-react'
import { Card, CardContent } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { cn, formatPrice, formatHours } from '@/lib/utils'
import type { Piece, WorkStatus, Destination } from '@/types'
import { PIECE_TYPE_LABELS, WORK_STATUS_LABELS, DESTINATION_LABELS } from '@/types'
import { PhotoThumbnail } from '@/components/gallery/PhotoThumbnail'

interface PieceCardProps {
  piece: Piece
}

function getStatusVariant(status: WorkStatus): 'default' | 'success' | 'warning' | 'info' {
  switch (status) {
    case 'finished':
    case 'ready':
      return 'success'
    case 'in_progress':
      return 'warning'
    default:
      return 'default'
  }
}

function getDestinationVariant(destination: Destination): 'default' | 'success' | 'info' | 'secondary' {
  switch (destination) {
    case 'sold':
    case 'gifted':
      return 'success'
    case 'for_sale':
    case 'for_gift':
      return 'info'
    default:
      return 'secondary'
  }
}

export function PieceCard({ piece }: PieceCardProps) {
  const firstPhoto = piece.photos[0]
  const photoPath = firstPhoto ? `pieces/${piece.id}/${firstPhoto}` : null

  return (
    <Link to={`/pieces/${piece.id}`}>
      <Card className="overflow-hidden transition-shadow hover:shadow-md">
        {/* Photo */}
        <div className="relative aspect-[4/3] bg-gray-100">
          {photoPath ? (
            <PhotoThumbnail path={photoPath} alt={piece.name} className="h-full w-full object-cover" />
          ) : (
            <div className="flex h-full items-center justify-center text-gray-400">
              No photo
            </div>
          )}
          {/* Type badge */}
          <Badge
            variant="secondary"
            className="absolute left-2 top-2 bg-white/90"
          >
            {PIECE_TYPE_LABELS[piece.type]}
          </Badge>
        </div>

        <CardContent className="p-4">
          {/* Title and ID */}
          <h3 className="font-medium text-gray-900 line-clamp-1">{piece.name}</h3>
          <p className="text-xs text-gray-400 mt-0.5">{piece.id}</p>

          {/* Status badges */}
          <div className="mt-2 flex flex-wrap gap-1">
            <Badge variant={getStatusVariant(piece.work_status)}>
              {WORK_STATUS_LABELS[piece.work_status]}
            </Badge>
            <Badge variant={getDestinationVariant(piece.destination)}>
              {DESTINATION_LABELS[piece.destination]}
            </Badge>
          </div>

          {/* Meta info */}
          <div className="mt-3 flex items-center gap-4 text-sm text-gray-500">
            {piece.work_hours && (
              <div className="flex items-center gap-1">
                <Clock className="h-4 w-4" />
                <span>{formatHours(piece.work_hours)}</span>
              </div>
            )}
            {piece.price && (
              <div className="flex items-center gap-1">
                <Euro className="h-4 w-4" />
                <span>{formatPrice(piece.price)}</span>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </Link>
  )
}
