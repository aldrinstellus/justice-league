# Global API Keys Protocol

**CRITICAL REQUIREMENT**: All Justice League heroes MUST use the global API folder for credentials.

## Global API Folder Location

```
/Users/admin/Documents/claudecode/api/
├── .env                 # Runtime environment variables (ALWAYS CHECK FIRST)
├── README.md            # Full documentation with usage examples
├── figma-tokens.json    # Structured Figma tokens (6 team tokens)
└── gamma-token.json     # Structured Gamma token + project tracking
```

## Current API Keys

| Service | Environment Variable | File | Status |
|---------|---------------------|------|--------|
| Gamma.app | `GAMMA_API_KEY` | `.env`, `gamma-token.json` | Active |
| Figma | `FIGMA_ACCESS_TOKEN` | `figma-tokens.json` | Active (6 tokens) |
| Penpot | `PENPOT_USERNAME/PASSWORD` | `.env` | When needed |

## Heroes Using API Keys

| Hero | API Service | Purpose |
|------|-------------|---------|
| Quicksilver | Figma | Parallel frame exports (PNG/PDF) |
| Hawkman | Figma | Structural parsing & hierarchy |
| Artemis | Figma | Design-to-code conversion |
| Hephaestus | Figma | Code-to-design reverse engineering |
| Cyborg | Figma, Multiple | Multi-platform integrations |
| Oracle | Gamma.app | Presentation generation |
| Zatanna | Gamma.app | Content transformation |

## Standard Usage Pattern (ALL SCRIPTS)

### Python Scripts - Always check global folder first:

```python
from dotenv import load_dotenv
import os

# ALWAYS load global API folder FIRST, then project-specific
load_dotenv("/Users/admin/Documents/claudecode/api/.env")
load_dotenv()  # Project .env as fallback

# Get API key
api_key = os.getenv("GAMMA_API_KEY")  # or FIGMA_ACCESS_TOKEN
```

### Bash/Shell - Export from global folder:

```bash
# Source global API keys
source /Users/admin/Documents/claudecode/api/.env

# Or export individually
export GAMMA_API_KEY=$(grep GAMMA_API_KEY /Users/admin/Documents/claudecode/api/.env | cut -d'=' -f2)
```

## Standing Instructions for Heroes

1. **ALWAYS check global folder first**: `/Users/admin/Documents/claudecode/api/.env`
2. **Never hardcode API keys** in scripts - use environment variables
3. **Update global folder** when adding new API services
4. **Document in README.md** when adding new keys
5. **Create JSON file** for structured token storage (like `figma-tokens.json`)
6. **Never commit .env files** to git repositories
7. **Never ask user for API keys** that are already in global folder

## Quick Reference Commands

```bash
# View all API keys
cat /Users/admin/Documents/claudecode/api/.env

# View Figma tokens (structured)
cat /Users/admin/Documents/claudecode/api/figma-tokens.json

# View Gamma token (structured)
cat /Users/admin/Documents/claudecode/api/gamma-token.json

# View full API documentation
cat /Users/admin/Documents/claudecode/api/README.md
```

## Adding New API Keys

When adding a new API service:

1. Add to `.env`:
   ```
   NEW_SERVICE_API_KEY=your-key-here
   ```

2. Create structured JSON file (optional but recommended):
   ```json
   {
     "service_name": {
       "description": "Service description",
       "tokens": {
         "main": {
           "owner": "Aldrin",
           "token": "your-key-here",
           "status": "active"
         }
       },
       "usage": {
         "environment_variable": "NEW_SERVICE_API_KEY",
         "api_base": "https://api.service.com/v1"
       }
     }
   }
   ```

3. Update README.md with:
   - Service name and purpose
   - Usage examples
   - Heroes that use the service

---

**Last Updated**: December 1, 2025
**Maintained By**: Oracle (Justice League)
