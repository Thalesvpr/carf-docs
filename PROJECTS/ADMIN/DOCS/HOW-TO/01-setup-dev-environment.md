# Setup Dev Environment - ADMIN

## Setup

Setup requer Node.js 18+ ou Bun 1.0+, clonar repositório `git clone https://github.com/user/carf-admin.git PROJECTS/ADMIN/SRC-CODE`, instalar deps com `bun install`, configurar `.env.local` com `VITE_API_URL=http://localhost:7001`, `VITE_KEYCLOAK_URL=http://localhost:8080`, subir dependências (GEOAPI, Keycloak, PostgreSQL) com `docker-compose up -d` na raiz do projeto CARF, e rodar dev server com `bun run dev` abrindo `http://localhost:5173` com hot reload, fazer login com usuário admin configurado no Keycloak realm, acessar dashboard em `/admin`.

## Comandos

```bash
# 1. Clonar
git clone https://github.com/user/carf-admin.git PROJECTS/ADMIN/SRC-CODE
cd PROJECTS/ADMIN/SRC-CODE

# 2. Instalar
bun install

# 3. Configurar env
echo "VITE_API_URL=http://localhost:7001" > .env.local
echo "VITE_KEYCLOAK_URL=http://localhost:8080" >> .env.local

# 4. Subir dependências
cd ../../.. && docker-compose up -d

# 5. Rodar dev
cd PROJECTS/ADMIN/SRC-CODE && bun run dev
```

