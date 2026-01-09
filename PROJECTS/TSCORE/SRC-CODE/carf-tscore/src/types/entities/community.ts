/**
 * Community (Comunidade/Assentamento) Entity Type
 *
 * Community or settlement that groups housing units geographically.
 *
 * @see CENTRAL/DOMAIN-MODEL/ENTITIES/04-community.md
 */

export interface Community {
  /** Unique global identifier (UUID) */
  id: string

  /** Community name */
  name: string

  /** Community type */
  type: 'URBANA' | 'RURAL' | 'QUILOMBOLA' | 'INDIGENA' | 'RIBEIRINHA'

  /** Community code/identifier */
  code?: string | null

  /** Description */
  description?: string | null

  /** Geographic boundary - GeoJSON Polygon */
  boundary?: GeoJSON.Polygon | null

  /** Total area in square meters */
  totalArea?: number | null

  /** Estimated population */
  estimatedPopulation?: number | null

  /** REURB type (S - Social Interest, E - Specific Interest) */
  reurbType?: 'REURB-S' | 'REURB-E' | null

  /** REURB process number */
  reurbProcessNumber?: string | null

  /** Free-form observations */
  observations?: string | null

  /** Custom tenant-specific data (JSON) */
  customData?: Record<string, unknown> | null

  /** Parent tenant ID */
  tenantId: string

  /** Archived flag */
  isArchived: boolean

  /** Creation timestamp */
  createdAt: Date

  /** Last update timestamp */
  updatedAt: Date

  /** Soft delete timestamp */
  deletedAt?: Date | null

  /** Optimistic locking version */
  version: number
}

/**
 * Community with loaded relationships and statistics
 */
export interface CommunityWithRelations extends Community {
  /** Statistics */
  stats?: {
    /** Total units count */
    unitsCount: number

    /** Units by status */
    unitsByStatus: Record<string, number>

    /** Total holders count */
    holdersCount: number

    /** Total blocks count */
    blocksCount: number
  }

  /** Assigned teams */
  teams?: Array<{
    id: string
    name: string
  }>
}

/**
 * Community creation DTO
 */
export interface CreateCommunityDto {
  name: string
  type: 'URBANA' | 'RURAL' | 'QUILOMBOLA' | 'INDIGENA' | 'RIBEIRINHA'
  code?: string
  description?: string
  boundary?: GeoJSON.Polygon
  totalArea?: number
  estimatedPopulation?: number
  reurbType?: 'REURB-S' | 'REURB-E'
  reurbProcessNumber?: string
  observations?: string
  customData?: Record<string, unknown>
}

/**
 * Community update DTO
 */
export interface UpdateCommunityDto extends Partial<Omit<CreateCommunityDto, 'type'>> {
  isArchived?: boolean
}
