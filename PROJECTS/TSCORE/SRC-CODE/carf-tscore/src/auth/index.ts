/**
 * Auth Module
 *
 * Authentication module with Keycloak OAuth2/OIDC support.
 *
 * Exports client and types. Framework-specific hooks/composables
 * are available via subpath imports:
 * - import { useAuth } from '@carf/tscore/auth/react'
 * - import { useAuth } from '@carf/tscore/auth/vue'
 */

export { KeycloakClient } from './keycloak-client.js'
export type {
  KeycloakConfig,
  User,
  AuthTokens,
  AuthState
} from './types.js'
