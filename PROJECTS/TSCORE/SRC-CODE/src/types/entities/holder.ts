/**
 * Holder (Titular) Entity Type
 *
 * Individual person (holder/occupant) linked to housing units.
 *
 * @see CENTRAL/DOMAIN-MODEL/ENTITIES/03-holder.md
 */

export interface Holder {
  /** Unique global identifier (UUID) */
  id: string

  /** Full name */
  name: string

  /** CPF (Brazilian tax ID) - normalized 11 digits */
  cpf?: string | null

  /** RG (identity document) */
  rg?: string | null

  /** RG issuing agency */
  rgIssuer?: string | null

  /** Birth date */
  birthDate?: Date | null

  /** Gender (M/F/OTHER) */
  gender?: 'M' | 'F' | 'OTHER' | null

  /** Marital status */
  maritalStatus?: 'SINGLE' | 'MARRIED' | 'DIVORCED' | 'WIDOWED' | 'STABLE_UNION' | null

  /** Occupation/profession */
  occupation?: string | null

  /** Email */
  email?: string | null

  /** Phone number - normalized */
  phone?: string | null

  /** Secondary phone */
  phoneSecondary?: string | null

  /** Photo URL */
  photoUrl?: string | null

  /** Free-form observations */
  observations?: string | null

  /** Custom tenant-specific data (JSON) */
  customData?: Record<string, unknown> | null

  /** Parent tenant ID */
  tenantId: string

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
 * Holder with loaded relationships
 */
export interface HolderWithRelations extends Holder {
  /** Units linked to this holder */
  units?: Array<{
    id: string
    code: string
    status: string
    relationshipType: string
    ownershipPercentage: number
  }>

  /** Documents count */
  documentsCount?: number
}

/**
 * Holder creation DTO
 */
export interface CreateHolderDto {
  name: string
  cpf?: string
  rg?: string
  rgIssuer?: string
  birthDate?: Date | string
  gender?: 'M' | 'F' | 'OTHER'
  maritalStatus?: 'SINGLE' | 'MARRIED' | 'DIVORCED' | 'WIDOWED' | 'STABLE_UNION'
  occupation?: string
  email?: string
  phone?: string
  phoneSecondary?: string
  photoUrl?: string
  observations?: string
  customData?: Record<string, unknown>
}

/**
 * Holder update DTO
 */
export interface UpdateHolderDto extends Partial<CreateHolderDto> {}
