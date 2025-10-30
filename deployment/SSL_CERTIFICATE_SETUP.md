# 🔒 SSL Certificate Setup Guide

**Version**: 1.0.0
**Purpose**: Generate and configure SSL certificates for Oracle production deployment
**Time Required**: 30-60 minutes

---

## Overview

This guide covers SSL/TLS certificate setup for Oracle production deployment. SSL certificates are **required** for production launch to ensure secure HTTPS communication.

---

## Prerequisites

- Production domain name (e.g., `oracle.example.com`)
- DNS configured and pointing to production server
- Root or sudo access on production server
- Port 80 and 443 open on firewall

---

## Option 1: Let's Encrypt (Recommended)

### Advantages
- ✅ Free
- ✅ Automatic renewal
- ✅ Trusted by all browsers
- ✅ Quick setup

### Step 1: Install Certbot

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx
```

**CentOS/RHEL**:
```bash
sudo yum install certbot python3-certbot-nginx
```

**macOS**:
```bash
brew install certbot
```

### Step 2: Stop Nginx (if running)
```bash
sudo systemctl stop nginx
# or
docker-compose down
```

### Step 3: Generate Certificate

**Standalone Mode** (if no web server running):
```bash
sudo certbot certonly --standalone \
  -d oracle.example.com \
  -d www.oracle.example.com \
  --email admin@example.com \
  --agree-tos \
  --no-eff-email
```

**Nginx Mode** (if nginx already configured):
```bash
sudo certbot --nginx \
  -d oracle.example.com \
  -d www.oracle.example.com \
  --email admin@example.com \
  --agree-tos
```

### Step 4: Copy Certificates to Deployment Directory

```bash
# Create SSL directory
sudo mkdir -p /path/to/oracle/deployment/nginx/ssl

# Copy certificates
sudo cp /etc/letsencrypt/live/oracle.example.com/fullchain.pem \
  /path/to/oracle/deployment/nginx/ssl/oracle.crt

sudo cp /etc/letsencrypt/live/oracle.example.com/privkey.pem \
  /path/to/oracle/deployment/nginx/ssl/oracle.key

# Set permissions
sudo chmod 644 /path/to/oracle/deployment/nginx/ssl/oracle.crt
sudo chmod 600 /path/to/oracle/deployment/nginx/ssl/oracle.key
sudo chown $(whoami):$(whoami) /path/to/oracle/deployment/nginx/ssl/*
```

### Step 5: Verify Certificates

```bash
# Check certificate validity
openssl x509 -in deployment/nginx/ssl/oracle.crt -text -noout | grep -E "Subject:|Issuer:|Not Before|Not After"

# Should show:
# Subject: CN=oracle.example.com
# Issuer: C=US, O=Let's Encrypt, CN=R3
# Not Before: [date]
# Not After: [date] (90 days from now)
```

### Step 6: Configure Auto-Renewal

```bash
# Test renewal (dry run)
sudo certbot renew --dry-run

# Add cron job for auto-renewal (runs twice daily)
sudo crontab -e

# Add this line:
0 0,12 * * * certbot renew --quiet --deploy-hook "cp /etc/letsencrypt/live/oracle.example.com/fullchain.pem /path/to/oracle/deployment/nginx/ssl/oracle.crt && cp /etc/letsencrypt/live/oracle.example.com/privkey.pem /path/to/oracle/deployment/nginx/ssl/oracle.key && docker-compose -f /path/to/oracle/deployment/docker-compose.yml exec nginx nginx -s reload"
```

---

## Option 2: Commercial Certificate (e.g., DigiCert, Comodo)

### Step 1: Generate Certificate Signing Request (CSR)

```bash
# Create directory
mkdir -p deployment/nginx/ssl
cd deployment/nginx/ssl

# Generate private key
openssl genrsa -out oracle.key 2048

# Generate CSR
openssl req -new -key oracle.key -out oracle.csr

# You'll be prompted for:
# Country Name (2 letter code) []:US
# State or Province Name (full name) []:California
# Locality Name (eg, city) []:San Francisco
# Organization Name (eg, company) []:Your Company
# Organizational Unit Name (eg, section) []:IT
# Common Name (eg, FQDN) []:oracle.example.com
# Email Address []:admin@example.com
```

### Step 2: Submit CSR to Certificate Authority

1. Purchase SSL certificate from CA
2. Submit the contents of `oracle.csr`
3. Complete domain validation (email, DNS, or HTTP)
4. Wait for CA to issue certificate (minutes to hours)

### Step 3: Download and Install Certificate

```bash
# Download certificate files from CA:
# - oracle.example.com.crt (your certificate)
# - intermediate.crt (intermediate certificate)
# - root.crt (root certificate - optional)

# Create full chain certificate
cat oracle.example.com.crt intermediate.crt > oracle.crt

# Move files to deployment directory
mv oracle.crt deployment/nginx/ssl/
mv oracle.key deployment/nginx/ssl/

# Set permissions
chmod 644 deployment/nginx/ssl/oracle.crt
chmod 600 deployment/nginx/ssl/oracle.key
```

### Step 4: Verify Certificate

```bash
openssl x509 -in deployment/nginx/ssl/oracle.crt -text -noout | grep -E "Subject:|Issuer:|Not Before|Not After"
```

---

## Option 3: Self-Signed Certificate (Development/Staging Only)

⚠️ **WARNING**: Self-signed certificates are NOT suitable for production. Use only for development/staging.

### Generate Self-Signed Certificate

```bash
# Create directory
mkdir -p deployment/nginx/ssl

# Generate self-signed certificate (valid for 365 days)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout deployment/nginx/ssl/oracle.key \
  -out deployment/nginx/ssl/oracle.crt \
  -subj "/C=US/ST=California/L=San Francisco/O=Dev/CN=oracle.local"

# Set permissions
chmod 644 deployment/nginx/ssl/oracle.crt
chmod 600 deployment/nginx/ssl/oracle.key
```

---

## Nginx Configuration

### Update Nginx Config (if needed)

The provided `deployment/nginx/nginx.conf` already includes SSL configuration. Verify it references your certificate files:

```nginx
server {
    listen 443 ssl http2;
    server_name oracle.example.com;

    ssl_certificate /etc/nginx/ssl/oracle.crt;
    ssl_certificate_key /etc/nginx/ssl/oracle.key;

    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # ... rest of config
}
```

### Update Docker Compose (if needed)

Verify `docker-compose.yml` mounts SSL certificates:

```yaml
nginx:
  volumes:
    - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    - ./nginx/ssl:/etc/nginx/ssl:ro  # SSL certificates
```

---

## Verification

### Step 1: Start Services

```bash
cd /path/to/oracle
docker-compose -f deployment/docker-compose.yml up -d nginx
```

### Step 2: Test SSL Locally

```bash
# Test HTTPS connection
curl -I https://oracle.example.com

# Should return:
# HTTP/2 200
# server: nginx/1.24.0
# ...

# Test SSL certificate
openssl s_client -connect oracle.example.com:443 -servername oracle.example.com < /dev/null

# Should show:
# SSL handshake has read X bytes
# Verify return code: 0 (ok)
```

### Step 3: Test from Browser

1. Open https://oracle.example.com in browser
2. Click the padlock icon
3. Verify certificate details:
   - ✅ Issued to: oracle.example.com
   - ✅ Issued by: Let's Encrypt / Your CA
   - ✅ Valid from/to dates
   - ✅ No warnings or errors

### Step 4: Test SSL Grade

```bash
# Online SSL test (after DNS is public)
# Visit: https://www.ssllabs.com/ssltest/analyze.html?d=oracle.example.com
# Target: A or A+ grade
```

---

## Security Hardening

### Recommended SSL Settings

Already configured in `deployment/nginx/nginx.conf`:

```nginx
# Use only strong protocols
ssl_protocols TLSv1.2 TLSv1.3;

# Use strong ciphers
ssl_ciphers HIGH:!aNULL:!MD5;
ssl_prefer_server_ciphers on;

# Enable HSTS (HTTP Strict Transport Security)
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

# Disable SSL session tickets (for forward secrecy)
ssl_session_tickets off;

# Enable OCSP stapling
ssl_stapling on;
ssl_stapling_verify on;
```

### Additional Security Headers

```nginx
# Prevent clickjacking
add_header X-Frame-Options "SAMEORIGIN" always;

# Prevent MIME type sniffing
add_header X-Content-Type-Options "nosniff" always;

# Enable XSS protection
add_header X-XSS-Protection "1; mode=block" always;
```

---

## Troubleshooting

### Issue 1: Certificate Not Found

**Error**: `nginx: [emerg] cannot load certificate "/etc/nginx/ssl/oracle.crt"`

**Solution**:
```bash
# Verify files exist
ls -l deployment/nginx/ssl/

# Verify Docker mount
docker-compose -f deployment/docker-compose.yml exec nginx ls -l /etc/nginx/ssl/

# If missing, copy certificates and restart
docker-compose -f deployment/docker-compose.yml restart nginx
```

---

### Issue 2: Permission Denied

**Error**: `SSL: error:0200100D:system library:fopen:Permission denied`

**Solution**:
```bash
# Fix permissions
chmod 644 deployment/nginx/ssl/oracle.crt
chmod 600 deployment/nginx/ssl/oracle.key

# Restart nginx
docker-compose -f deployment/docker-compose.yml restart nginx
```

---

### Issue 3: Certificate Expired

**Error**: `SSL certificate problem: certificate has expired`

**Solution**:
```bash
# Check expiration
openssl x509 -in deployment/nginx/ssl/oracle.crt -noout -enddate

# For Let's Encrypt - renew
sudo certbot renew --force-renewal

# Copy new certificates
sudo cp /etc/letsencrypt/live/oracle.example.com/fullchain.pem \
  deployment/nginx/ssl/oracle.crt
sudo cp /etc/letsencrypt/live/oracle.example.com/privkey.pem \
  deployment/nginx/ssl/oracle.key

# Reload nginx
docker-compose -f deployment/docker-compose.yml exec nginx nginx -s reload
```

---

### Issue 4: Wrong Certificate

**Error**: Browser shows certificate for wrong domain

**Solution**:
```bash
# Check certificate CN (Common Name)
openssl x509 -in deployment/nginx/ssl/oracle.crt -noout -subject

# Should show: subject=CN = oracle.example.com

# If wrong, regenerate certificate for correct domain
```

---

### Issue 5: Mixed Content Warnings

**Error**: Browser shows mixed content (HTTP resources on HTTPS page)

**Solution**:
```nginx
# Force all requests to HTTPS
server {
    listen 80;
    server_name oracle.example.com;
    return 301 https://$server_name$request_uri;
}
```

---

## Certificate Renewal

### Let's Encrypt (Auto-Renewal)

```bash
# Renewal happens automatically via cron
# Manual renewal:
sudo certbot renew

# Update Oracle certificates
sudo cp /etc/letsencrypt/live/oracle.example.com/fullchain.pem \
  /path/to/oracle/deployment/nginx/ssl/oracle.crt
sudo cp /etc/letsencrypt/live/oracle.example.com/privkey.pem \
  /path/to/oracle/deployment/nginx/ssl/oracle.key

# Reload nginx (zero downtime)
docker-compose -f /path/to/oracle/deployment/docker-compose.yml exec nginx nginx -s reload
```

### Commercial Certificate (Manual Renewal)

1. **30 days before expiration**: Order renewal from CA
2. Generate new CSR (or reuse existing)
3. Submit CSR to CA
4. Complete validation
5. Download new certificate
6. Replace old certificate files
7. Reload nginx

---

## Monitoring Certificate Expiration

### Add Expiration Monitoring

```bash
# Create monitoring script
cat > /usr/local/bin/check-cert-expiry.sh << 'EOF'
#!/bin/bash
CERT_FILE="/path/to/oracle/deployment/nginx/ssl/oracle.crt"
DAYS_UNTIL_EXPIRY=$(openssl x509 -in "$CERT_FILE" -noout -enddate | sed 's/notAfter=//' | xargs -I {} date -d {} +%s | xargs -I {} echo $(( ({} - $(date +%s)) / 86400 )))

if [ "$DAYS_UNTIL_EXPIRY" -lt 30 ]; then
    echo "WARNING: SSL certificate expires in $DAYS_UNTIL_EXPIRY days"
    # Send alert (email, Slack, etc.)
fi
EOF

chmod +x /usr/local/bin/check-cert-expiry.sh

# Add to cron (check daily)
echo "0 9 * * * /usr/local/bin/check-cert-expiry.sh" | crontab -
```

### Prometheus Monitoring

Already configured in `deployment/monitoring/prometheus.yml`:
```yaml
- job_name: 'ssl_exporter'
  static_configs:
    - targets: ['oracle.example.com:443']
```

---

## Checklist

### Pre-Production Checklist

- [ ] Domain name configured and DNS pointing to production server
- [ ] Port 443 open on firewall
- [ ] SSL certificate generated (Let's Encrypt recommended)
- [ ] Certificate files copied to `deployment/nginx/ssl/`
- [ ] Certificate permissions correct (644 for .crt, 600 for .key)
- [ ] Certificate verified with `openssl x509` command
- [ ] Nginx configuration updated (if needed)
- [ ] Docker Compose verified to mount SSL certificates
- [ ] HTTPS tested locally with `curl`
- [ ] HTTPS tested in browser (no warnings)
- [ ] SSL grade tested (A or A+ target)
- [ ] Auto-renewal configured (for Let's Encrypt)
- [ ] Certificate expiration monitoring enabled
- [ ] HTTP to HTTPS redirect working
- [ ] All security headers configured
- [ ] Certificate documented in production inventory

---

## Production Launch Verification

```bash
# Run this after SSL setup
echo "=== SSL Certificate Verification ==="
echo ""

# 1. Check files exist
echo "[1/7] Checking certificate files..."
if [ -f deployment/nginx/ssl/oracle.crt ] && [ -f deployment/nginx/ssl/oracle.key ]; then
    echo "✅ Certificate files found"
else
    echo "❌ Certificate files missing"
    exit 1
fi

# 2. Check permissions
echo "[2/7] Checking permissions..."
CERT_PERMS=$(stat -c %a deployment/nginx/ssl/oracle.crt)
KEY_PERMS=$(stat -c %a deployment/nginx/ssl/oracle.key)
if [ "$CERT_PERMS" = "644" ] && [ "$KEY_PERMS" = "600" ]; then
    echo "✅ Permissions correct"
else
    echo "⚠️  Permissions: oracle.crt=$CERT_PERMS (should be 644), oracle.key=$KEY_PERMS (should be 600)"
fi

# 3. Check certificate validity
echo "[3/7] Checking certificate validity..."
NOT_AFTER=$(openssl x509 -in deployment/nginx/ssl/oracle.crt -noout -enddate | cut -d= -f2)
echo "✅ Certificate valid until: $NOT_AFTER"

# 4. Check certificate subject
echo "[4/7] Checking certificate subject..."
SUBJECT=$(openssl x509 -in deployment/nginx/ssl/oracle.crt -noout -subject | sed 's/subject=//')
echo "✅ Subject: $SUBJECT"

# 5. Check days until expiry
echo "[5/7] Checking expiration..."
DAYS_LEFT=$(openssl x509 -in deployment/nginx/ssl/oracle.crt -noout -enddate | sed 's/notAfter=//' | xargs -I {} date -d {} +%s | xargs -I {} echo $(( ({} - $(date +%s)) / 86400 )))
if [ "$DAYS_LEFT" -gt 30 ]; then
    echo "✅ Certificate valid for $DAYS_LEFT more days"
else
    echo "⚠️  Certificate expires in $DAYS_LEFT days - renewal needed soon"
fi

# 6. Check nginx config
echo "[6/7] Checking Nginx configuration..."
if docker-compose -f deployment/docker-compose.yml exec -T nginx nginx -t 2>&1 | grep -q "successful"; then
    echo "✅ Nginx configuration valid"
else
    echo "❌ Nginx configuration invalid"
fi

# 7. Test HTTPS
echo "[7/7] Testing HTTPS connection..."
if curl -s -I https://localhost | grep -q "HTTP/2 200"; then
    echo "✅ HTTPS connection successful"
else
    echo "⚠️  HTTPS connection test inconclusive (may need public DNS)"
fi

echo ""
echo "=== SSL Setup Complete ==="
```

---

## Support

### Certificate Issues
- Check Nginx error logs: `docker-compose logs nginx`
- Verify certificate with: `openssl x509 -in <file> -text -noout`
- Test SSL: https://www.ssllabs.com/ssltest/

### Let's Encrypt Support
- Documentation: https://letsencrypt.org/docs/
- Community: https://community.letsencrypt.org/

---

**Oracle says**: "Secure connections protect the League. SSL is not optional." 🔒
