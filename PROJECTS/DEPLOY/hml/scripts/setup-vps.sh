#!/bin/bash
# CARF HML — Setup inicial do VPS (Ubuntu 24.04)
# Executar como root: bash setup-vps.sh

set -euo pipefail

echo "=== CARF HML — VPS Setup ==="

echo "[1/5] Atualizando sistema..."
apt update && apt upgrade -y

echo "[2/6] Instalando Git..."
apt install -y git

echo "[3/6] Instalando Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com | sh
    systemctl enable docker
else
    echo "Docker já instalado."
fi

echo "[4/6] Criando usuário deploy..."
if ! id "deploy" &>/dev/null; then
    useradd -m -s /bin/bash -G docker deploy
    echo "Usuário 'deploy' criado. Defina a senha: passwd deploy"
else
    usermod -aG docker deploy
    echo "Usuário 'deploy' já existe."
fi

echo "[5/6] Configurando firewall..."
apt install -y ufw
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

echo "[6/6] Configurando swap (2GB)..."
if [ ! -f /swapfile ]; then
    fallocate -l 2G /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo '/swapfile none swap sw 0 0' >> /etc/fstab
    echo "Swap criado."
else
    echo "Swap já existe."
fi

echo ""
echo "========================================="
echo " CARF HML — Setup completo!"
echo "========================================="
echo ""
echo " Próximos passos:"
echo "   1. passwd deploy"
echo "   2. su - deploy"
echo "   3. bash repos.sh              # clona todos os repos"
echo "   4. cd ~/carf/PROJECTS/DEPLOY/hml"
echo "   5. cp .env.example .env && nano .env"
echo "   6. docker compose up -d --build"
echo "   7. Seguir POST-DEPLOY.md"
echo ""
echo " Para atualizar depois:"
echo "   bash ~/carf/PROJECTS/DEPLOY/hml/repos.sh pull"
echo "   cd ~/carf/PROJECTS/DEPLOY/hml"
echo "   docker compose up -d --build"
echo ""
echo " URLs HML:"
echo "   hml-app.IP.sslip.io      → REURBWEB"
echo "   hml-admin.IP.sslip.io    → REURBMASTER"
echo "   hml-api.IP.sslip.io      → GEOAPI + Swagger"
echo "   hml-auth.IP.sslip.io     → Keycloak"
echo "   hml-s3.IP.sslip.io       → MinIO Console"
echo "========================================="
