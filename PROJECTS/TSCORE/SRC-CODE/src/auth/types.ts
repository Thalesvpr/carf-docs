/**
 * Authentication Types
 *
 * Types for Keycloak OAuth2/OIDC authentication.
 */

import type { Role } from '../types/enums/role.js'

/**
 * Keycloak configuration
 */
export interface KeycloakConfig {
  /** Keycloak server URL (e.g., "https://keycloak.example.com") */
  url: string

  /** Realm name (e.g., "carf") */
  realm: string

  /** Client ID (e.g., "geoapi-web") */
  clientId: string

  /** Optional client secret (for confidential clients) */
  clientSecret?: string
}

/**
 * Authenticated user information
 */
export interface User {
  /** User ID (subject from JWT) */
  id: string

  /** Username */
  username: string

  /** Email */
  email?: string

  /** Full name */
  name?: string

  /** User roles */
  roles: Role[]

  /** Tenant ID (from custom claims) */
  tenantId: string

  /** Additional custom claims */
  customClaims?: Record<string, unknown>
}

/**
 * Authentication tokens
 */
export interface AuthTokens {
  /** Access token (JWT) */
  accessToken: string

  /** Refresh token */
  refreshToken: string

  /** ID token (OIDC) */
  idToken?: string

  /** Token expiration time (Unix timestamp) */
  expiresAt: number
}

/**
 * Authentication state
 */
export interface AuthState {
  /** Is user authenticated */
  isAuthenticated: boolean

  /** Is authentication loading */
  isLoading: boolean

  /** Current user */
  user: User | null

  /** Authentication error */
  error: Error | null
}
