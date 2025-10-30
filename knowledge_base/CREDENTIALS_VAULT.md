# 🔐 Justice League Credentials Vault

**⚠️ IMPORTANT: Keep this file secure and never commit to public repos!**

**Last Updated:** October 28, 2025
**Managed By:** Oracle 🔮

---

## 🎨 Figma API

**Access Token:**
```
figd_aPXrH3Rqpm8sdez_nHmmXKHvZ9vcK3sOcJwvhE7s
```

**Usage:**
- Used by Artemis 🏹 (Figma MCP specialist)
- Configured in `.mcp.json`
- Access Figma files and extract design data

**Configuration Location:**
```bash
/Users/admin/Documents/claudecode/Projects/aldo-vision/.mcp.json
```

---

## 🎨 Penpot API

**API URL:**
```
https://design.penpot.app
```

**Configuration:**
- Timeout: 30 seconds
- Retry attempts: 3
- SSL verification: Enabled
- Cache duration: 24 hours

**Configuration Location:**
```bash
/Users/admin/Documents/claudecode/Projects/aldo-vision/config/penpot_api.json
```

**Note:** Username/password need to be set in `.env` file (use `.env.example` as template)

---

## 🛠️ MCP Servers Configured

### 1. Figma MCP
- **Command:** `npx -y figma-mcp-server`
- **Token:** ✅ Configured
- **Hero:** Artemis 🏹

### 2. Tailwind CSS MCP
- **Command:** `npx -y tailwindcss-mcp-server`
- **Hero:** Green Arrow 🎯

### 3. Shadcn UI MCP
- **Command:** `npx -y @jpisnice/shadcn-ui-mcp-server`
- **Hero:** Zatanna ✨

---

## 📋 Quick Access Commands

### Use Figma Token
```bash
export FIGMA_ACCESS_TOKEN="figd_aPXrH3Rqpm8sdez_nHmmXKHvZ9vcK3sOcJwvhE7s"
```

### Test Figma Access
```bash
curl -H "X-FIGMA-TOKEN: figd_aPXrH3Rqpm8sdez_nHmmXKHvZ9vcK3sOcJwvhE7s" \
  "https://api.figma.com/v1/files/YOUR_FILE_KEY"
```

### Copy MCP Config
```bash
cp /Users/admin/Documents/claudecode/Projects/aldo-vision/.mcp.json /path/to/new/project/
```

---

## 🦸 Hero Access Map

| Hero | Service | Token/Config | Purpose |
|------|---------|--------------|---------|
| Artemis 🏹 | Figma | ✅ Token | Design extraction |
| Green Arrow 🎯 | Tailwind | ✅ MCP | CSS generation |
| Zatanna ✨ | Shadcn UI | ✅ MCP | Component generation |
| Oracle 🔮 | All | ✅ Access | Knowledge management |

---

## 🔄 Token Rotation

**Figma Token Created:** Unknown (check Figma account)
**Rotation Schedule:** As needed
**Last Verified:** October 28, 2025

**To Rotate Figma Token:**
1. Go to Figma → Settings → Account → Personal Access Tokens
2. Delete old token
3. Generate new token
4. Update `.mcp.json` in all projects
5. Update this file

---

## 🚀 Deploy to New Project

To use these credentials in a new project (like k12/demo):

```bash
# 1. Copy MCP configuration
cp /Users/admin/Documents/claudecode/Projects/aldo-vision/.mcp.json /Users/admin/Documents/claudecode/Projects/k12/demo/

# 2. Verify token works
cd /Users/admin/Documents/claudecode/Projects/k12/demo
cat .mcp.json | grep FIGMA_ACCESS_TOKEN

# 3. Test with Artemis
# Artemis will now have Figma access!
```

---

## 📝 Notes

- **Security:** This file contains sensitive credentials. Keep secure!
- **Backup:** Tokens stored in 1Password/secure vault (recommended)
- **Sharing:** Never commit this file to public repos
- **Access:** Only Justice League heroes and operators should access

---

**"I see everything. I know everything. I protect everything."** - Oracle 🔮
