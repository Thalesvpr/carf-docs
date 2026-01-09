/**
 * ProtectedRoute Component (React)
 *
 * Route component that requires authentication and specific roles.
 *
 * @example
 * ```tsx
 * <ProtectedRoute roles={['ADMIN', 'MANAGER']}>
 *   <AdminPanel />
 * </ProtectedRoute>
 * ```
 */

import { type ReactNode } from 'react'
import { useAuth } from './useAuth.js'
import type { Role } from '../../types/enums/role.js'

interface ProtectedRouteProps {
  /** Required roles (user must have at least one) */
  roles?: Role[]

  /** Fallback component when not authorized */
  fallback?: ReactNode

  /** Child components to render when authorized */
  children: ReactNode
}

/**
 * Protected route component that checks authentication and roles
 */
export function ProtectedRoute({
  roles,
  fallback = <div>Unauthorized</div>,
  children
}: ProtectedRouteProps) {
  const { user, isLoading, login } = useAuth()

  // Show loading state
  if (isLoading) {
    return <div>Loading...</div>
  }

  // Not authenticated - redirect to login
  if (!user) {
    login()
    return <div>Redirecting to login...</div>
  }

  // Check roles if specified
  if (roles && roles.length > 0) {
    const hasRequiredRole = roles.some(role => user.roles.includes(role))
    if (!hasRequiredRole) {
      return <>{fallback}</>
    }
  }

  // Authorized - render children
  return <>{children}</>
}
