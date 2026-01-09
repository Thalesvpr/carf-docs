/**
 * Keycloak Client
 *
 * OAuth2/OIDC client for Keycloak authentication.
 *
 * @see CENTRAL/INTEGRATION/KEYCLOAK/README.md
 * @see CENTRAL/REQUIREMENTS/FUNCTIONAL-REQUIREMENTS/RF-001-integracao-com-keycloak.md
 */

import type { KeycloakConfig, User, AuthTokens } from './types.js'
import type { Role } from '../types/enums/role.js'
import { hasRolePermission } from '../types/enums/role.js'

/**
 * Keycloak OAuth2 client
 *
 * Note: This is a basic implementation. Full OAuth2 flow implementation
 * should include PKCE, token refresh, logout, etc.
 */
export class KeycloakClient {
  private config: KeycloakConfig
  private tokens: AuthTokens | null = null
  private user: User | null = null

  constructor(config: KeycloakConfig) {
    this.config = config
  }

  /**
   * Initialize authentication (check for existing session)
   */
  async init(): Promise<void> {
    // Load tokens from storage (localStorage/sessionStorage)
    const storedTokens = this.loadTokensFromStorage()
    if (storedTokens) {
      this.tokens = storedTokens
      await this.loadUser()
    }
  }

  /**
   * Start login flow (redirect to Keycloak)
   */
  login(redirectUri?: string): void {
    const url = this.buildAuthorizationUrl(redirectUri)
    window.location.href = url
  }

  /**
   * Handle OAuth2 callback (parse authorization code)
   * @param code - Authorization code from callback
   * @param state - State parameter for CSRF protection
   */
  async handleCallback(code: string, state: string): Promise<void> {
    // Exchange code for tokens
    const tokens = await this.exchangeCodeForTokens(code)
    this.tokens = tokens
    this.saveTokensToStorage(tokens)
    await this.loadUser()
  }

  /**
   * Logout (clear session and redirect to Keycloak logout)
   */
  async logout(redirectUri?: string): Promise<void> {
    const url = this.buildLogoutUrl(redirectUri)
    this.clearTokensFromStorage()
    this.tokens = null
    this.user = null
    window.location.href = url
  }

  /**
   * Get current access token (refresh if expired)
   */
  async getToken(): Promise<string> {
    if (!this.tokens) {
      throw new Error('Not authenticated')
    }

    // Check if token is expired
    const now = Date.now() / 1000
    if (this.tokens.expiresAt < now + 60) { // Refresh 60s before expiry
      await this.refreshTokens()
    }

    return this.tokens.accessToken
  }

  /**
   * Get current user
   */
  getUser(): User | null {
    return this.user
  }

  /**
   * Check if user has a specific role
   */
  hasRole(role: Role): boolean {
    if (!this.user) return false
    return this.user.roles.includes(role)
  }

  /**
   * Check if user has at least the required role level
   */
  hasRolePermission(requiredRole: Role): boolean {
    if (!this.user) return false
    return this.user.roles.some(userRole => hasRolePermission(userRole, requiredRole))
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return this.tokens !== null && this.user !== null
  }

  // Private helper methods

  private buildAuthorizationUrl(redirectUri?: string): string {
    const { url, realm, clientId } = this.config
    const redirect = redirectUri || window.location.origin + '/auth/callback'
    const state = this.generateState()
    const nonce = this.generateNonce()

    // Store state for CSRF validation
    sessionStorage.setItem('oauth_state', state)
    sessionStorage.setItem('oauth_nonce', nonce)

    const params = new URLSearchParams({
      client_id: clientId,
      redirect_uri: redirect,
      response_type: 'code',
      scope: 'openid profile email',
      state,
      nonce,
      // PKCE parameters would go here
    })

    return `${url}/realms/${realm}/protocol/openid-connect/auth?${params}`
  }

  private buildLogoutUrl(redirectUri?: string): string {
    const { url, realm } = this.config
    const redirect = redirectUri || window.location.origin

    const params = new URLSearchParams({
      post_logout_redirect_uri: redirect,
    })

    return `${url}/realms/${realm}/protocol/openid-connect/logout?${params}`
  }

  private async exchangeCodeForTokens(code: string): Promise<AuthTokens> {
    // TODO: Implement token exchange with Keycloak
    // This is a placeholder - real implementation would make HTTP request
    throw new Error('Not implemented: exchangeCodeForTokens')
  }

  private async refreshTokens(): Promise<void> {
    if (!this.tokens?.refreshToken) {
      throw new Error('No refresh token available')
    }

    // TODO: Implement token refresh with Keycloak
    // This is a placeholder - real implementation would make HTTP request
    throw new Error('Not implemented: refreshTokens')
  }

  private async loadUser(): Promise<void> {
    if (!this.tokens) return

    // Decode JWT and extract user info
    const userInfo = this.decodeJWT(this.tokens.accessToken)
    this.user = {
      id: userInfo.sub,
      username: userInfo.preferred_username,
      email: userInfo.email,
      name: userInfo.name,
      roles: userInfo.realm_access?.roles || [],
      tenantId: userInfo.tenant_id,
      customClaims: userInfo,
    }
  }

  private decodeJWT(token: string): any {
    const parts = token.split('.')
    if (parts.length !== 3) {
      throw new Error('Invalid JWT')
    }

    const payload = parts[1]
    const decoded = atob(payload.replace(/-/g, '+').replace(/_/g, '/'))
    return JSON.parse(decoded)
  }

  private generateState(): string {
    return Math.random().toString(36).substring(2, 15)
  }

  private generateNonce(): string {
    return Math.random().toString(36).substring(2, 15)
  }

  private saveTokensToStorage(tokens: AuthTokens): void {
    localStorage.setItem('auth_tokens', JSON.stringify(tokens))
  }

  private loadTokensFromStorage(): AuthTokens | null {
    const stored = localStorage.getItem('auth_tokens')
    return stored ? JSON.parse(stored) : null
  }

  private clearTokensFromStorage(): void {
    localStorage.removeItem('auth_tokens')
    sessionStorage.removeItem('oauth_state')
    sessionStorage.removeItem('oauth_nonce')
  }
}
