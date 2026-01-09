/**
 * Tenant (Cliente Multi-tenant) Entity Type
 *
 * Multi-tenant client with RLS isolation.
 *
 * @see CENTRAL/DOMAIN-MODEL/ENTITIES/07-tenant.md
 */

export interface Tenant {
  /** Unique global identifier (UUID) */
  id: string

  /** Tenant name (e.g., "Prefeitura de São Paulo") */
  name: string

  /** Slug for URL (e.g., "prefeitura-sp") */
  slug: string

  /** CNPJ (Brazilian company tax ID) - normalized 14 digits */
  cnpj?: string | null

  /** Email */
  email?: string | null

  /** Phone */
  phone?: string | null

  /** Logo URL */
  logoUrl?: string | null

  /** Primary color (hex) */
  primaryColor?: string | null

  /** Secondary color (hex) */
  secondaryColor?: string | null

  /** Timezone (e.g., "America/Sao_Paulo") */
  timezone: string

  /** Locale (e.g., "pt-BR") */
  locale: string

  /** Custom settings (JSON) */
  settings?: Record<string, unknown> | null

  /** Active flag */
  isActive: boolean

  /** Trial expiration date */
  trialExpiresAt?: Date | null

  /** Subscription type */
  subscriptionType?: 'FREE' | 'BASIC' | 'PRO' | 'ENTERPRISE' | null

  /** Subscription expires at */
  subscriptionExpiresAt?: Date | null

  /** Storage limit in bytes */
  storageLimitBytes?: number | null

  /** Current storage used in bytes */
  storageUsedBytes: number

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
 * Tenant with statistics
 */
export interface TenantWithStats extends Tenant {
  /** Statistics */
  stats?: {
    /** Total users count */
    usersCount: number

    /** Total communities count */
    communitiesCount: number

    /** Total units count */
    unitsCount: number

    /** Total holders count */
    holdersCount: number

    /** Storage usage percentage */
    storageUsagePercentage: number
  }
}

/**
 * Tenant creation DTO
 */
export interface CreateTenantDto {
  name: string
  slug: string
  cnpj?: string
  email?: string
  phone?: string
  logoUrl?: string
  primaryColor?: string
  secondaryColor?: string
  timezone?: string
  locale?: string
  settings?: Record<string, unknown>
  subscriptionType?: 'FREE' | 'BASIC' | 'PRO' | 'ENTERPRISE'
  storageLimitBytes?: number
}

/**
 * Tenant update DTO
 */
export interface UpdateTenantDto extends Partial<Omit<CreateTenantDto, 'slug'>> {
  isActive?: boolean
}
