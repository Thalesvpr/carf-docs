/**
 * Unit (Unidade Habitacional) Entity Type
 *
 * Housing unit in urban land regularization process.
 *
 * @see CENTRAL/DOMAIN-MODEL/ENTITIES/02-unit.md
 */

import type { UnitStatus } from '../enums/unit-status.js'

export interface Unit {
  /** Unique global identifier (UUID) */
  id: string

  /** Human-readable code unique within community (e.g., "U-001") */
  code: string

  /** Unit status in workflow */
  status: UnitStatus

  /** Address - Street name */
  street: string

  /** Address - Number */
  number?: string | null

  /** Address - Complement */
  complement?: string | null

  /** Address - Neighborhood */
  neighborhood?: string | null

  /** Address - City */
  city: string

  /** Address - State (2-letter code) */
  state: string

  /** Address - ZIP code (CEP) */
  zipCode?: string | null

  /** Geometry - GeoJSON Polygon defining property boundary */
  geometry?: GeoJSON.Polygon | null

  /** Calculated area in square meters */
  area?: number | null

  /** Type of occupation (residential, commercial, mixed, institutional) */
  occupationType?: 'RESIDENTIAL' | 'COMMERCIAL' | 'MIXED' | 'INSTITUTIONAL' | null

  /** Number of residents */
  residents?: number | null

  /** Current land situation description */
  landSituation?: string | null

  /** Free-form observations */
  observations?: string | null

  /** Custom tenant-specific data (JSON) */
  customData?: Record<string, unknown> | null

  /** Parent community ID */
  communityId: string

  /** Optional block ID (quadra urbana) */
  blockId?: string | null

  /** Optional plot ID (lote) */
  plotId?: string | null

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
 * Unit with loaded relationships
 */
export interface UnitWithRelations extends Unit {
  /** Community data */
  community?: {
    id: string
    name: string
    type: string
  }

  /** Holders (titulares) */
  holders?: Array<{
    id: string
    name: string
    cpf?: string
    relationshipType: string
    ownershipPercentage: number
  }>

  /** Documents count */
  documentsCount?: number

  /** Photos count */
  photosCount?: number
}

/**
 * Unit creation DTO
 */
export interface CreateUnitDto {
  code: string
  street: string
  number?: string
  complement?: string
  neighborhood?: string
  city: string
  state: string
  zipCode?: string
  geometry?: GeoJSON.Polygon
  area?: number
  occupationType?: 'RESIDENTIAL' | 'COMMERCIAL' | 'MIXED' | 'INSTITUTIONAL'
  residents?: number
  landSituation?: string
  observations?: string
  customData?: Record<string, unknown>
  communityId: string
  blockId?: string
  plotId?: string
}

/**
 * Unit update DTO
 */
export interface UpdateUnitDto extends Partial<Omit<CreateUnitDto, 'code' | 'communityId'>> {
  status?: UnitStatus
}
