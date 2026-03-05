FROM quay.io/keycloak/keycloak:26.0
COPY themes/carf /opt/keycloak/themes/carf
COPY realm-export.json /opt/keycloak/data/import/realm.json
