# ADMIN + Keycloak (React + Admin API)

## Install
```bash
npm install keycloak-js @keycloak/keycloak-admin-client
```

## Config
```typescript
// src/config/keycloak.ts
import Keycloak from 'keycloak-js';

export const keycloak = new Keycloak({
  url: 'http://localhost:8080',
  realm: 'carf',
  clientId: 'admin',
});
```

## Admin Client
```typescript
// src/lib/keycloakAdmin.ts
import KeycloakAdminClient from '@keycloak/keycloak-admin-client';

const adminClient = new KeycloakAdminClient({
  baseUrl: 'http://localhost:8080',
  realmName: 'carf',
});

// Authenticate with user token
export const initAdminClient = async (token: string) => {
  adminClient.setAccessToken(token);
};

export default adminClient;
```

## Create User
```typescript
// src/services/userService.ts
import adminClient from '../lib/keycloakAdmin';

export const createUser = async (userData: {
  username: string;
  email: string;
  firstName: string;
  lastName: string;
  tenantId: string;
}) => {
  const user = await adminClient.users.create({
    enabled: true,
    username: userData.username,
    email: userData.email,
    firstName: userData.firstName,
    lastName: userData.lastName,
    attributes: {
      tenants: [userData.tenantId],
      current_tenant: [userData.tenantId]
    }
  });

  return user;
};
```

## Assign Role
```typescript
export const assignRole = async (userId: string, roleName: string) => {
  const role = await adminClient.roles.findOneByName({ name: roleName });

  if (role) {
    await adminClient.users.addRealmRoleMappings({
      id: userId,
      roles: [{ id: role.id!, name: role.name! }]
    });
  }
};
```

## List Users by Tenant
```typescript
export const getUsersByTenant = async (tenantId: string) => {
  const users = await adminClient.users.find({
    max: 100,
    q: `tenants:${tenantId}`
  });

  return users;
};
```

## Update User Tenant
```typescript
export const switchUserTenant = async (userId: string, newTenantId: string) => {
  const user = await adminClient.users.findOne({ id: userId });

  await adminClient.users.update(
    { id: userId },
    {
      ...user,
      attributes: {
        ...user.attributes,
        current_tenant: [newTenantId]
      }
    }
  );
};
```

## Reset Password
```typescript
export const resetPassword = async (userId: string, newPassword: string) => {
  await adminClient.users.resetPassword({
    id: userId,
    credential: {
      temporary: false,
      type: 'password',
      value: newPassword
    }
  });
};
```

## Usage in Component
```typescript
// src/pages/Users.tsx
import { useEffect, useState } from 'react';
import { createUser, assignRole } from '../services/userService';
import { useAuth } from '../providers/AuthProvider';

export const UsersPage = () => {
  const { token } = useAuth();
  const [users, setUsers] = useState([]);

  useEffect(() => {
    initAdminClient(token);
    loadUsers();
  }, [token]);

  const handleCreateUser = async (data) => {
    const user = await createUser(data);
    await assignRole(user.id, 'analyst');
    loadUsers();
  };

  return <div>...</div>;
};
```

Done. ✅
