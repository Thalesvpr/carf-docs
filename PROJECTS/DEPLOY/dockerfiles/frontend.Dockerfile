# CARF Frontend - Simplified Build
# Shared by REURBWEB and REURBMASTER
# Libs are installed from GitHub Packages (no more multi-stage lib builds)

# Stage 1: Build frontend
FROM node:20-alpine AS app-build
ARG PROJECT_DIR
ARG NODE_AUTH_TOKEN
WORKDIR /app

# .npmrc for GitHub Packages authentication
RUN echo "@carffundiaria:registry=https://npm.pkg.github.com" > .npmrc && \
    echo "//npm.pkg.github.com/:_authToken=${NODE_AUTH_TOKEN}" >> .npmrc

COPY ${PROJECT_DIR}/package.json ${PROJECT_DIR}/package-lock.json* ./
RUN npm install

COPY ${PROJECT_DIR}/ .
RUN rm -f .env .env.local .env.production .env.*.local .npmrc

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

# Stage 2: Serve
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
    }\n}\n' > /etc/nginx/conf.d/default.conf

EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget -qO- http://localhost:80/ || exit 1
