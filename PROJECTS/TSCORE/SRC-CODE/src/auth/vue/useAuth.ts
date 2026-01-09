/**
 * useAuth Composable (Vue 3)
 *
 * Vue 3 composable for authentication state and actions.
 *
 * @example
 * ```vue
 * <script setup>
 * import { useAuth } from '@carf/tscore/auth/vue'
 *
 * const { user, login, logout, hasRole } = useAuth()
 * </script>
 *
 * <template>
 *   <button v-if="!user" @click="login">Login</button>
 *   <div v-else>Hello {{ user.name }}</div>
 * </template>
 * ```
 */

import { ref, computed, type Ref } from 'vue'
import type { KeycloakClient } from '../keycloak-client.js'
import type { User } from '../types.js'
import type { Role } from '../../types/enums/role.js'

let globalClient: KeycloakClient | null = null
const globalUser = ref<User | null>(null)
const globalIsLoading = ref(true)

/**
 * Initialize authentication globally (call once in main.ts)
 */
export async function initAuth(client: KeycloakClient): Promise<void> {
  globalClient = client
  await client.init()
  globalUser.value = client.getUser()
  globalIsLoading.value = false
}

/**
 * Use authentication composable
 *
 * @throws Error if initAuth not called
 */
export function useAuth() {
  if (!globalClient) {
    throw new Error('Auth not initialized. Call initAuth(client) first.')
  }

  const user = globalUser as Ref<User | null>
  const isLoading = globalIsLoading
  const isAuthenticated = computed(() => globalClient!.isAuthenticated())

  const login = () => {
    globalClient!.login()
  }

  const logout = async () => {
    await globalClient!.logout()
  }

  const hasRole = (role: Role) => {
    return globalClient!.hasRole(role)
  }

  const hasPermission = (requiredRole: Role) => {
    return globalClient!.hasRolePermission(requiredRole)
  }

  const getToken = async () => {
    return await globalClient!.getToken()
  }

  return {
    user,
    isLoading,
    isAuthenticated,
    login,
    logout,
    hasRole,
    hasPermission,
    getToken,
  }
}
