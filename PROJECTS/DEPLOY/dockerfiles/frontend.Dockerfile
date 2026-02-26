# CARF Frontend - Multi-stage Build
# Shared by REURBWEB and REURBMASTER
# Build context: repo root

ARG TSCORE_DIR=PROJECTS/LIB/TS/TSCORE/SRC-CODE/carf-tscore
ARG GEOAPI_CLIENT_DIR=PROJECTS/LIB/TS/GEOAPI-CLIENT/SRC-CODE/carf-geoapi-client

# Stage 1: Build @carf/tscore
FROM node:20-alpine AS tscore-build
ARG TSCORE_DIR
WORKDIR /tscore
COPY ${TSCORE_DIR}/ .
RUN npm install --ignore-scripts && npx tsc -p tsconfig.build.json

# Stage 2: Build @carf/geoapi-client
FROM node:20-alpine AS geoapi-client-build
ARG GEOAPI_CLIENT_DIR
WORKDIR /geoapi-client
COPY ${GEOAPI_CLIENT_DIR}/ .
RUN npm install
RUN npx orval --config orval.config.ts
RUN npx tsc --skipLibCheck

# Stage 3: Build frontend
FROM node:20-alpine AS app-build
ARG PROJECT_DIR
WORKDIR /app

COPY --from=tscore-build /tscore /tscore
COPY --from=geoapi-client-build /geoapi-client /geoapi-client

COPY ${PROJECT_DIR}/package.json ./
RUN sed -i 's|file:[^"]*carf-tscore|file:/tscore|' package.json
RUN sed -i 's|file:[^"]*carf-geoapi-client|file:/geoapi-client|' package.json
RUN npm install

COPY ${PROJECT_DIR}/ .
RUN rm -f .env .env.local .env.production .env.*.local

ARG VITE_API_URL
ARG VITE_KEYCLOAK_URL
ARG VITE_KEYCLOAK_REALM=carf
ARG VITE_KEYCLOAK_CLIENT_ID
ARG VITE_GOOGLE_MAPS_KEY=
ENV VITE_API_URL=${VITE_API_URL} \
    VITE_KEYCLOAK_URL=${VITE_KEYCLOAK_URL} \
    VITE_KEYCLOAK_REALM=${VITE_KEYCLOAK_REALM} \
    VITE_KEYCLOAK_CLIENT_ID=${VITE_KEYCLOAK_CLIENT_ID} \
    VITE_GOOGLE_MAPS_KEY=${VITE_GOOGLE_MAPS_KEY}

RUN npm run build

# Stage 4: Serve
FROM nginx:alpine
COPY --from=app-build /app/dist /usr/share/nginx/html
RUN printf 'server {\n\
    listen 80;\n\
    root /usr/share/nginx/html;\n\
    index index.html;\n\
    location / {\n\
        try_files $uri $uri/ /index.html;\n\
    }\n\
    location ~* \\.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {\n\
        expires 1y;\n\
        add_header Cache-Control "public, immutable";\n\
    }\n\
}\n' > /etc/nginx/conf.d/default.conf

EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget -qO- http://localhost:80/ || exit 1
