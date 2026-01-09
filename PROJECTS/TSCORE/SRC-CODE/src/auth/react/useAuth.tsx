/**
 * useAuth Hook (React)
 *
 * React hook for authentication state and actions.
 *
 * @example
 * ```tsx
 * function MyComponent() {
 *   const { user, login, logout, hasRole } = useAuth()
 *
 *   if (!user) {
 *     return <button onClick={login}>Login</button>
 *   }
 *
 *   return <div>Hello {user.name}</div>
 * }
 * ```
 */

import { createContext, useContext, useState, useEffect, type ReactNode } from 'react'
import type { KeycloakClient } from '../keycloak-client.js'
import type { User } from '../types.js'
import type { Role } from '../../types/enums/role.js'

interface AuthContextValue {
  /** Current authenticated user */
  user: User | null

  /** Is authentication loading */
  isLoading: boolean

  /** Is user authenticated */
  isAuthenticated: boolean

  /** Login (redirect to Keycloak) */
  login: () => void

  /** Logout */
  logout: () => Promise<void>

  /** Check if user has role */
  hasRole: (role: Role) => boolean

  /** Check if user has required permission level */
  hasPermission: (requiredRole: Role) => boolean

  /** Get access token */
  getToken: () => Promise<string>
}

const AuthContext = createContext<AuthContextValue | null>(null)

interface AuthProviderProps {
  /** Keycloak client instance */
  client: KeycloakClient

  /** Child components */
  children: ReactNode
}

/**
 * Authentication Provider Component
 *
 * Wrap your app with this provider to enable authentication.
 *
 * @example
 * ```tsx
 * const keycloakClient = new KeycloakClient({ url, realm, clientId })
 *
 * <AuthProvider client={keycloakClient}>
 *   <App />
 * </AuthProvider>
 * ```
 */
export function AuthProvider({ client, children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Initialize authentication on mount
    client.init().then(() => {
      setUser(client.getUser())
      setIsLoading(false)
    }).catch(err => {
      console.error('Auth initialization failed:', err)
      setIsLoading(false)
    })
  }, [client])

  const login = () => {
    client.login()
  }

  const logout = async () => {
    await client.logout()
  }

  const hasRole = (role: Role) => {
    return client.hasRole(role)
  }

  const hasPermission = (requiredRole: Role) => {
    return client.hasRolePermission(requiredRole)
  }

  const getToken = async () => {
    return await client.getToken()
  }

  const value: AuthContextValue = {
    user,
    isLoading,
    isAuthenticated: client.isAuthenticated(),
    login,
    logout,
    hasRole,
    hasPermission,
    getToken,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

/**
 * Use authentication context hook
 *
 * @throws Error if used outside AuthProvider
 */
export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
