# Supabase Project Setup Best Practices

**Created**: December 2025
**Author**: Oracle (Justice League)
**Last Updated**: 2025-12-05

## Overview

This guide covers best practices for setting up and migrating Supabase projects, including database configuration, authentication providers, and connection string management with Prisma.

---

## Table of Contents

1. [Project Creation](#1-project-creation)
2. [Region Selection](#2-region-selection)
3. [Connection Strings](#3-connection-strings)
4. [Prisma Integration](#4-prisma-integration)
5. [Authentication Providers](#5-authentication-providers)
6. [Database Migration](#6-database-migration)
7. [Environment Variables](#7-environment-variables)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. Project Creation

### Dashboard URL
```
https://supabase.com/dashboard/projects
```

### Checklist Before Creating
- [ ] Choose organization (PRO plan recommended for production)
- [ ] Select appropriate region (see Region Selection below)
- [ ] Prepare database password (strong, 20+ characters)
- [ ] Have Google OAuth credentials ready (if using Google auth)

### Project Reference
After creation, note your project reference ID (e.g., `svxvmuorexnzigrskftr`). This appears in:
- Dashboard URL: `supabase.com/dashboard/project/{PROJECT_REF}`
- API URLs: `{PROJECT_REF}.supabase.co`
- Connection strings: `postgres.{PROJECT_REF}`

---

## 2. Region Selection

### Available Regions (as of 2025)
| Region | Code | Location | Use Case |
|--------|------|----------|----------|
| `ap-south-1` | Mumbai | India/Middle East | **Best for UAE/Dubai users** |
| `ap-southeast-1` | Singapore | Southeast Asia | Asia-Pacific general |
| `us-east-1` | N. Virginia | USA East | North America East |
| `us-west-1` | N. California | USA West | North America West |
| `eu-west-1` | Ireland | Europe | EU compliance |
| `eu-central-1` | Frankfurt | Europe | EU compliance |

### Latency Considerations
| User Location | Recommended Region | Expected Latency |
|---------------|-------------------|------------------|
| Dubai/UAE | `ap-south-1` (Mumbai) | ~30-50ms |
| Dubai/UAE | `ap-southeast-1` (Singapore) | ~80-120ms |
| India | `ap-south-1` (Mumbai) | ~10-30ms |
| USA | `us-east-1` or `us-west-1` | ~20-50ms |
| Europe | `eu-west-1` or `eu-central-1` | ~20-50ms |

### Migration Between Regions
Supabase does NOT support direct region migration. You must:
1. Create new project in target region
2. Export/import data (pg_dump/pg_restore or Prisma)
3. Update connection strings
4. Re-configure authentication
5. Delete old project (optional)

---

## 3. Connection Strings

### Two Connection Types

#### 1. Pooled Connection (Transaction Mode) - Port 6543
```
DATABASE_URL="postgresql://postgres.{PROJECT_REF}:{PASSWORD}@aws-1-{REGION}.pooler.supabase.com:6543/postgres?pgbouncer=true&sslmode=require&connection_limit=1"
```

**Use for:**
- Application runtime queries
- Prisma Client queries
- Connection-limited environments (serverless)

#### 2. Direct Connection - Port 5432
```
DIRECT_URL="postgresql://postgres.{PROJECT_REF}:{PASSWORD}@aws-1-{REGION}.pooler.supabase.com:5432/postgres?sslmode=require&connection_limit=1"
```

**Use for:**
- Prisma migrations (`npx prisma migrate`)
- Prisma schema push (`npx prisma db push`)
- Direct database operations

### Connection String Template
```bash
# Mumbai (ap-south-1) Example
DATABASE_URL="postgresql://postgres.{PROJECT_REF}:{PASSWORD}@aws-1-ap-south-1.pooler.supabase.com:6543/postgres?pgbouncer=true&sslmode=require&connection_limit=1"
DIRECT_URL="postgresql://postgres.{PROJECT_REF}:{PASSWORD}@aws-1-ap-south-1.pooler.supabase.com:5432/postgres?sslmode=require&connection_limit=1"

# Singapore (ap-southeast-1) Example
DATABASE_URL="postgresql://postgres.{PROJECT_REF}:{PASSWORD}@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres?pgbouncer=true&sslmode=require&connection_limit=1"
DIRECT_URL="postgresql://postgres.{PROJECT_REF}:{PASSWORD}@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres?sslmode=require&connection_limit=1"
```

### Important Parameters
| Parameter | Value | Purpose |
|-----------|-------|---------|
| `pgbouncer=true` | Required for port 6543 | Disables prepared statements for pooler compatibility |
| `sslmode=require` | Always use | Encrypts connection |
| `connection_limit=1` | Recommended | Prevents connection exhaustion |

---

## 4. Prisma Integration

### schema.prisma Configuration
```prisma
datasource db {
  provider  = "postgresql"
  url       = env("DATABASE_URL")
  directUrl = env("DIRECT_URL")
}
```

### prisma.config.ts (Prisma 6+)
```typescript
import path from "node:path";
import type { PrismaConfig } from "prisma";
import "dotenv/config";

export default {
  earlyAccess: true,
  schema: path.join("prisma", "schema.prisma"),
} satisfies PrismaConfig;
```

### Required .env Setup
```bash
# .env file
DATABASE_URL="postgresql://postgres.{PROJECT_REF}:{PASSWORD}@aws-1-{REGION}.pooler.supabase.com:6543/postgres?pgbouncer=true&sslmode=require&connection_limit=1"
DIRECT_URL="postgresql://postgres.{PROJECT_REF}:{PASSWORD}@aws-1-{REGION}.pooler.supabase.com:5432/postgres?sslmode=require&connection_limit=1"
```

### Prisma Commands
```bash
# Push schema to database (uses DIRECT_URL)
npx prisma db push

# Generate Prisma Client
npx prisma generate

# Run migrations (uses DIRECT_URL)
npx prisma migrate deploy

# Open Prisma Studio
npx prisma studio

# Seed database
npx prisma db seed
# OR
npm run db:seed
```

---

## 5. Authentication Providers

### Enabling Google OAuth

#### Step 1: Get Callback URL
Navigate to: `Authentication > Sign In / Providers > Google`

Callback URL format:
```
https://{PROJECT_REF}.supabase.co/auth/v1/callback
```

#### Step 2: Configure Google Cloud Console
1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create/select OAuth 2.0 Client ID
3. Add authorized redirect URI (the callback URL above)
4. Note Client ID and Client Secret

#### Step 3: Enable in Supabase
1. Navigate to: `Authentication > Sign In / Providers`
2. Click on "Google"
3. Toggle "Enable Sign in with Google"
4. Enter Client ID (comma-separated if multiple)
5. Enter Client Secret
6. Click "Save"

### Common OAuth Error
```json
{"code":400,"error_code":"validation_failed","msg":"Unsupported provider: provider is not enabled"}
```

**Solution**: Enable the provider in Supabase dashboard before using it.

### Environment Variables for Auth
```bash
# .env
NEXT_PUBLIC_SUPABASE_URL="https://{PROJECT_REF}.supabase.co"
NEXT_PUBLIC_SUPABASE_ANON_KEY="{ANON_KEY}"

# For NextAuth.js integration
AUTH_GOOGLE_ID="{GOOGLE_CLIENT_ID}"
AUTH_GOOGLE_SECRET="{GOOGLE_CLIENT_SECRET}"
```

---

## 6. Database Migration

### Full Migration Checklist

When migrating to a new Supabase project:

```bash
# 1. Create new project in Supabase dashboard

# 2. Get credentials from dashboard:
#    - Project Settings > Database > Connection string
#    - Project Settings > API > anon key

# 3. Update .env with new credentials
DATABASE_URL="postgresql://postgres.{NEW_PROJECT_REF}:..."
DIRECT_URL="postgresql://postgres.{NEW_PROJECT_REF}:..."
NEXT_PUBLIC_SUPABASE_URL="https://{NEW_PROJECT_REF}.supabase.co"
NEXT_PUBLIC_SUPABASE_ANON_KEY="{NEW_ANON_KEY}"

# 4. Push schema to new database
npx prisma db push

# 5. Run seed script (if applicable)
npm run db:seed

# 6. Enable authentication providers in dashboard
#    - Google OAuth
#    - Email (usually enabled by default)

# 7. Test the application
npm run dev
```

### Data Export/Import (if needed)
```bash
# Export from old database
pg_dump -h {OLD_HOST} -U postgres -d postgres > backup.sql

# Import to new database
psql -h {NEW_HOST} -U postgres -d postgres < backup.sql
```

---

## 7. Environment Variables

### Complete .env Template
```bash
# ===========================================
# DATABASE (Supabase PostgreSQL)
# ===========================================

# Pooled connection for runtime queries (port 6543)
DATABASE_URL="postgresql://postgres.{PROJECT_REF}:{PASSWORD}@aws-1-{REGION}.pooler.supabase.com:6543/postgres?pgbouncer=true&sslmode=require&connection_limit=1"

# Direct connection for migrations (port 5432)
DIRECT_URL="postgresql://postgres.{PROJECT_REF}:{PASSWORD}@aws-1-{REGION}.pooler.supabase.com:5432/postgres?sslmode=require&connection_limit=1"

# ===========================================
# SUPABASE API
# ===========================================

NEXT_PUBLIC_SUPABASE_URL="https://{PROJECT_REF}.supabase.co"
NEXT_PUBLIC_SUPABASE_ANON_KEY="{ANON_KEY}"

# ===========================================
# AUTHENTICATION
# ===========================================

AUTH_SECRET="{RANDOM_SECRET}"

# Google OAuth
AUTH_GOOGLE_ID="{GOOGLE_CLIENT_ID}"
AUTH_GOOGLE_SECRET="{GOOGLE_CLIENT_SECRET}"
```

### Security Notes
- **NEVER commit .env files to git**
- Use `.env.example` as a template (without real values)
- Rotate passwords if accidentally exposed
- Use strong passwords (20+ characters, mixed case, numbers, symbols)

---

## 8. Troubleshooting

### Common Issues

#### "Provider is not enabled" Error
```json
{"code":400,"error_code":"validation_failed","msg":"Unsupported provider: provider is not enabled"}
```
**Solution**: Enable the OAuth provider in Supabase dashboard under Authentication > Sign In / Providers

#### Connection Refused
```
Error: connect ECONNREFUSED
```
**Solutions**:
- Check region in connection string matches your project
- Verify password is correct
- Ensure SSL is enabled (`sslmode=require`)

#### Prepared Statement Errors
```
Error: prepared statement "s0" already exists
```
**Solution**: Ensure `pgbouncer=true` is in your DATABASE_URL (port 6543)

#### Migration Fails
```
Error: P1001: Can't reach database server
```
**Solutions**:
- Use DIRECT_URL (port 5432) for migrations
- Check network connectivity
- Verify database password

#### Prisma Client Not Generated
```
Error: @prisma/client did not initialize
```
**Solution**: Run `npx prisma generate` after schema changes

#### Google OAuth "redirect_uri_mismatch" Error
```
Error 400: redirect_uri_mismatch
```
**Causes & Solutions**:
1. **Callback URL not added**: Add `https://{PROJECT_REF}.supabase.co/auth/v1/callback` to Google Cloud Console → OAuth 2.0 Client → Authorized redirect URIs
2. **Wrong Supabase project**: Verify PROJECT_REF in callback URL matches your current Supabase project
3. **Region migration**: When migrating regions, the new project has a different PROJECT_REF - update callback URL in Google Cloud Console

#### Google OAuth Client ID Mismatch (CRITICAL)
**Symptom**: Login fails silently or shows "Error 400: invalid_client"

**Root Cause**: Multiple Google Cloud OAuth clients exist, and wrong Client ID is in `.env` or Supabase dashboard.

**Diagnosis Steps**:
```bash
# 1. Check current .env Client ID
grep AUTH_GOOGLE_ID .env

# 2. Compare with Google Cloud Console
# Go to: https://console.cloud.google.com/apis/credentials
# Find the OAuth 2.0 Client you want to use
# Verify Client ID matches
```

**The Fix** (All THREE must match):
1. **Google Cloud Console** → OAuth 2.0 Client → Client ID & Client Secret
2. **Your `.env` file** → `AUTH_GOOGLE_ID` and `AUTH_GOOGLE_SECRET`
3. **Supabase Dashboard** → Authentication → Sign In / Providers → Google → Client ID & Client Secret

**Common Scenario**: Multiple Google Cloud projects exist (e.g., `ATC-DS`, `MyApp-Dev`, `MyApp-Prod`). Each has different Client IDs. Ensure you're using credentials from the SAME Google Cloud project.

**If Client Secret is masked/lost**:
1. Go to Google Cloud Console → APIs & Services → Credentials
2. Click on your OAuth 2.0 Client ID
3. Click "ADD SECRET" under Client secrets
4. Copy the new secret
5. Update both `.env` AND Supabase dashboard with new secret

**Complete Sync Procedure**:
```bash
# After getting credentials from Google Cloud Console:

# 1. Update .env file
AUTH_GOOGLE_ID=your-client-id.apps.googleusercontent.com
AUTH_GOOGLE_SECRET=GOCSPX-your-client-secret

# 2. Update Supabase Dashboard
# Navigate to: Authentication > Sign In / Providers > Google
# Enter SAME Client ID and Client Secret
# Click "Save"

# 3. Restart dev server
npm run dev
```

**Verification Checklist**:
- [ ] Google Cloud Console callback URL matches new Supabase project
- [ ] `.env` AUTH_GOOGLE_ID matches Google Cloud Console
- [ ] `.env` AUTH_GOOGLE_SECRET matches Google Cloud Console
- [ ] Supabase Dashboard Google Client ID matches `.env`
- [ ] Supabase Dashboard Google Client Secret matches `.env`
- [ ] Dev server restarted after `.env` changes

---

## Quick Reference

### URLs
| Resource | URL Pattern |
|----------|-------------|
| Dashboard | `https://supabase.com/dashboard/project/{PROJECT_REF}` |
| API | `https://{PROJECT_REF}.supabase.co` |
| Auth Callback | `https://{PROJECT_REF}.supabase.co/auth/v1/callback` |
| Pooler (Transaction) | `aws-1-{REGION}.pooler.supabase.com:6543` |
| Pooler (Direct) | `aws-1-{REGION}.pooler.supabase.com:5432` |

### Dashboard Navigation
| Setting | Location |
|---------|----------|
| Connection strings | Project Settings > Database |
| API keys | Project Settings > API |
| Auth providers | Authentication > Sign In / Providers |
| Database password | Project Settings > Database > Reset database password |
| Project region | Cannot be changed after creation |

---

## Cost Analysis

**Estimated time to complete migration**: 15-30 minutes
**Estimated token cost**: ~$0.50-$1.00 (Oracle coordination)

This guide was created during the ATCK migration from Singapore to Mumbai region (December 2025).

---

**Last Updated**: 2025-12-05
