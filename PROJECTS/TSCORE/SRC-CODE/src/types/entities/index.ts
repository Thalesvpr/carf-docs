/**
 * Entities Module
 *
 * TypeScript interfaces for domain entities.
 */

export type {
  Unit,
  UnitWithRelations,
  CreateUnitDto,
  UpdateUnitDto
} from './unit.js'

export type {
  Holder,
  HolderWithRelations,
  CreateHolderDto,
  UpdateHolderDto
} from './holder.js'

export type {
  Community,
  CommunityWithRelations,
  CreateCommunityDto,
  UpdateCommunityDto
} from './community.js'

export type {
  Tenant,
  TenantWithStats,
  CreateTenantDto,
  UpdateTenantDto
} from './tenant.js'
