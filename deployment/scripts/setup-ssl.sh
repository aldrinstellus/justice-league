#!/bin/bash
################################################################################
# Oracle SSL Certificate Setup Script
# Automates Let's Encrypt certificate generation and installation
################################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SSL_DIR="$PROJECT_ROOT/deployment/nginx/ssl"
DOMAIN="${ORACLE_DOMAIN:-oracle.example.com}"
EMAIL="${ORACLE_EMAIL:-admin@example.com}"
STAGING="${ORACLE_STAGING:-false}"

echo "================================================================================"
echo "Oracle SSL Certificate Setup"
echo "================================================================================"
echo ""

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --domain)
            DOMAIN="$2"
            shift 2
            ;;
        --email)
            EMAIL="$2"
            shift 2
            ;;
        --staging)
            STAGING=true
            shift
            ;;
        --help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --domain DOMAIN    Domain name (default: oracle.example.com)"
            echo "  --email EMAIL      Email for Let's Encrypt (default: admin@example.com)"
            echo "  --staging          Use Let's Encrypt staging (for testing)"
            echo "  --help             Show this help message"
            echo ""
            echo "Environment variables:"
            echo "  ORACLE_DOMAIN      Domain name"
            echo "  ORACLE_EMAIL       Email address"
            echo "  ORACLE_STAGING     Use staging (true/false)"
            echo ""
            echo "Examples:"
            echo "  $0 --domain oracle.mycompany.com --email ssl@mycompany.com"
            echo "  $0 --staging  # Test with Let's Encrypt staging"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

echo "Configuration:"
echo "  Domain: $DOMAIN"
echo "  Email: $EMAIL"
echo "  Staging: $STAGING"
echo ""

# Check if running as root
if [[ $EUID -ne 0 ]] && [[ "$STAGING" == "false" ]]; then
    echo -e "${YELLOW}Warning: This script typically needs root access for Let's Encrypt.${NC}"
    echo -e "${YELLOW}Run with sudo if you encounter permission errors.${NC}"
    echo ""
fi

# Step 1: Check prerequisites
echo "[1/7] Checking prerequisites..."

# Check certbot
if ! command -v certbot &> /dev/null; then
    echo -e "${RED}✗ certbot not found${NC}"
    echo ""
    echo "Install certbot:"
    echo "  Ubuntu/Debian: sudo apt install certbot"
    echo "  CentOS/RHEL: sudo yum install certbot"
    echo "  macOS: brew install certbot"
    exit 1
fi
echo -e "${GREEN}✓ certbot found${NC}"

# Check openssl
if ! command -v openssl &> /dev/null; then
    echo -e "${RED}✗ openssl not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ openssl found${NC}"

# Check domain resolution
echo "Checking domain DNS resolution..."
if host "$DOMAIN" &> /dev/null; then
    echo -e "${GREEN}✓ Domain $DOMAIN resolves${NC}"
else
    echo -e "${YELLOW}⚠ Domain $DOMAIN does not resolve${NC}"
    echo -e "${YELLOW}  Certificate generation will likely fail.${NC}"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""

# Step 2: Create SSL directory
echo "[2/7] Creating SSL directory..."
mkdir -p "$SSL_DIR"
chmod 755 "$SSL_DIR"
echo -e "${GREEN}✓ SSL directory created: $SSL_DIR${NC}"
echo ""

# Step 3: Stop services that might block port 80/443
echo "[3/7] Checking for services on ports 80/443..."

if lsof -Pi :80 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠ Service running on port 80${NC}"
    echo "Certbot needs port 80. Stop nginx/apache first:"
    echo "  docker-compose down"
    echo "  OR: sudo systemctl stop nginx"
    read -p "Attempt to stop Docker services? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose -f "$PROJECT_ROOT/deployment/docker-compose.yml" down || true
        echo -e "${GREEN}✓ Docker services stopped${NC}"
    fi
else
    echo -e "${GREEN}✓ Port 80 available${NC}"
fi

if lsof -Pi :443 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠ Service running on port 443${NC}"
else
    echo -e "${GREEN}✓ Port 443 available${NC}"
fi

echo ""

# Step 4: Generate certificate
echo "[4/7] Generating Let's Encrypt certificate..."

CERTBOT_ARGS="certonly --standalone -d $DOMAIN --email $EMAIL --agree-tos --non-interactive"

if [[ "$STAGING" == "true" ]]; then
    CERTBOT_ARGS="$CERTBOT_ARGS --staging"
    echo -e "${YELLOW}Using Let's Encrypt STAGING environment (for testing)${NC}"
fi

echo "Running: certbot $CERTBOT_ARGS"
echo ""

if certbot $CERTBOT_ARGS; then
    echo -e "${GREEN}✓ Certificate generated successfully${NC}"
else
    echo -e "${RED}✗ Certificate generation failed${NC}"
    echo ""
    echo "Common issues:"
    echo "1. Domain not pointing to this server"
    echo "2. Port 80/443 blocked by firewall"
    echo "3. Another service using port 80/443"
    echo "4. DNS propagation not complete"
    echo ""
    echo "Try staging first: $0 --domain $DOMAIN --email $EMAIL --staging"
    exit 1
fi

echo ""

# Step 5: Copy certificates to deployment directory
echo "[5/7] Copying certificates to deployment directory..."

CERT_PATH="/etc/letsencrypt/live/$DOMAIN"

if [[ ! -d "$CERT_PATH" ]]; then
    echo -e "${RED}✗ Certificate directory not found: $CERT_PATH${NC}"
    exit 1
fi

# Copy certificate
cp "$CERT_PATH/fullchain.pem" "$SSL_DIR/oracle.crt"
echo -e "${GREEN}✓ Certificate copied: $SSL_DIR/oracle.crt${NC}"

# Copy private key
cp "$CERT_PATH/privkey.pem" "$SSL_DIR/oracle.key"
echo -e "${GREEN}✓ Private key copied: $SSL_DIR/oracle.key${NC}"

echo ""

# Step 6: Set permissions
echo "[6/7] Setting permissions..."

chmod 644 "$SSL_DIR/oracle.crt"
echo -e "${GREEN}✓ Certificate permissions: 644${NC}"

chmod 600 "$SSL_DIR/oracle.key"
echo -e "${GREEN}✓ Private key permissions: 600${NC}"

# Change ownership to current user (if not root)
if [[ $EUID -ne 0 ]]; then
    sudo chown "$(whoami):$(whoami)" "$SSL_DIR/oracle.crt" "$SSL_DIR/oracle.key" 2>/dev/null || true
fi

echo ""

# Step 7: Verify certificates
echo "[7/7] Verifying certificates..."

# Check certificate validity
EXPIRY=$(openssl x509 -in "$SSL_DIR/oracle.crt" -noout -enddate | cut -d= -f2)
echo -e "${GREEN}✓ Certificate valid until: $EXPIRY${NC}"

# Check certificate subject
SUBJECT=$(openssl x509 -in "$SSL_DIR/oracle.crt" -noout -subject | sed 's/subject=//')
echo -e "${GREEN}✓ Certificate subject: $SUBJECT${NC}"

# Check days until expiry
DAYS_LEFT=$(openssl x509 -in "$SSL_DIR/oracle.crt" -noout -enddate | sed 's/notAfter=//' | xargs -I {} date -d {} +%s | xargs -I {} echo $(( ({} - $(date +%s)) / 86400 )))
if [[ $DAYS_LEFT -gt 60 ]]; then
    echo -e "${GREEN}✓ Certificate valid for $DAYS_LEFT more days${NC}"
else
    echo -e "${YELLOW}⚠ Certificate expires in $DAYS_LEFT days - renewal needed soon${NC}"
fi

# Check certificate chain
echo -n "Checking certificate chain... "
if openssl verify -CAfile <(openssl x509 -in "$SSL_DIR/oracle.crt") "$SSL_DIR/oracle.crt" &> /dev/null; then
    echo -e "${GREEN}✓ Valid${NC}"
else
    echo -e "${YELLOW}⚠ Could not verify (normal for self-signed)${NC}"
fi

echo ""
echo "================================================================================"
echo "SSL Certificate Setup Complete!"
echo "================================================================================"
echo ""
echo "Certificate files:"
echo "  Certificate: $SSL_DIR/oracle.crt"
echo "  Private Key: $SSL_DIR/oracle.key"
echo ""
echo "Next steps:"
echo "1. Verify nginx configuration includes these certificates"
echo "2. Start Oracle services: docker-compose up -d"
echo "3. Test HTTPS: curl -I https://$DOMAIN"
echo "4. Setup auto-renewal (see below)"
echo ""
echo "Auto-Renewal Setup:"
echo "================================================================================"
echo "Let's Encrypt certificates expire every 90 days."
echo "Setup automatic renewal with cron:"
echo ""
echo "sudo crontab -e"
echo ""
echo "Add this line to renew twice daily:"
echo "0 0,12 * * * certbot renew --quiet --deploy-hook '$PROJECT_ROOT/deployment/scripts/reload-ssl.sh'"
echo ""
echo "Or test renewal now:"
echo "sudo certbot renew --dry-run"
echo ""

# Create reload script
RELOAD_SCRIPT="$SCRIPT_DIR/reload-ssl.sh"
cat > "$RELOAD_SCRIPT" << 'EOF'
#!/bin/bash
# Reload SSL certificates after Let's Encrypt renewal

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SSL_DIR="$PROJECT_ROOT/deployment/nginx/ssl"
DOMAIN="${RENEWED_DOMAINS:-oracle.example.com}"

echo "Reloading SSL certificates for $DOMAIN..."

# Copy renewed certificates
cp "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" "$SSL_DIR/oracle.crt"
cp "/etc/letsencrypt/live/$DOMAIN/privkey.pem" "$SSL_DIR/oracle.key"

# Set permissions
chmod 644 "$SSL_DIR/oracle.crt"
chmod 600 "$SSL_DIR/oracle.key"

# Reload nginx
docker-compose -f "$PROJECT_ROOT/deployment/docker-compose.yml" exec nginx nginx -s reload

echo "SSL certificates reloaded successfully"
EOF

chmod +x "$RELOAD_SCRIPT"
echo "Created reload script: $RELOAD_SCRIPT"
echo ""

echo "================================================================================"
echo "Oracle says: \"SSL certificates installed. Communications secured.\" 🔒"
echo "================================================================================"
