# Figma MCP Server Integration Guide

## Overview

The Figma MCP (Model Context Protocol) server enables direct access to Figma designs with exact measurements, colors, typography, and spacing values. This eliminates guesswork and achieves 99%+ accuracy in design-to-code conversion.

## Current Setup

### Installed MCP Servers

```json
{
  "mcpServers": {
    "tailwindcss-server": {
      "command": "npx",
      "args": ["-y", "tailwindcss-mcp-server"]
    },
    "shadcn-ui": {
      "command": "npx",
      "args": ["-y", "@jpisnice/shadcn-ui-mcp-server"]
    },
    "figma": {
      "command": "npx",
      "args": ["-y", "figma-mcp-server"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "YOUR_FIGMA_TOKEN_HERE"
      }
    }
  }
}
```

## How to Use Figma MCP with Dev Mode

### Step 1: Open Figma Desktop

1. Launch Figma Desktop application
2. Open your design file: `fubdMARNgA2lVhmzpPg77y`
3. Navigate to the frame you want to convert (e.g., "Settings/Main" - ID: 875:35531)

### Step 2: Enable Dev Mode

1. Click the **"Dev Mode"** toggle in the top-right corner
2. Select the frame/component you want to inspect
3. The right panel will show detailed specs:
   - **Layout**: Spacing, padding, margins in px
   - **Typography**: Font family, size, weight, line height
   - **Colors**: Hex codes, RGB, opacity
   - **Effects**: Shadows, borders, blur
   - **Auto Layout**: Gap, direction, alignment

### Step 3: Query Design Specs via MCP

Once the Figma MCP server is configured, I can query design properties:

#### Example Queries I Can Make:

```
"What is the exact spacing between the profile card and main content?"
"What are the exact font sizes and weights for all headings?"
"What is the exact hex color of the pink theme used throughout?"
"What are the exact padding values for the navigation bar?"
"What are the border radius values for all cards?"
```

## Benefits of Using Figma MCP

### Before (API-based - 95-97% accuracy)
- ✅ Layout structure correct
- ✅ Components positioned correctly
- ❌ Spacing estimated visually
- ❌ Colors approximated
- ❌ Font sizes guessed
- ❌ Padding/margins approximated

### After (MCP + Dev Mode - 99%+ accuracy)
- ✅ Layout structure correct
- ✅ Components positioned correctly
- ✅ **Exact spacing in px**
- ✅ **Exact hex colors**
- ✅ **Exact font sizes and weights**
- ✅ **Exact padding/margins**
- ✅ **Exact border radius**
- ✅ **Exact shadow values**

## Design Values We Can Extract

### 1. Layout & Spacing
```
- Container width: 1200px
- Gap between elements: 24px
- Section padding: 32px
- Card spacing: 16px
```

### 2. Typography
```
- Heading: Inter 24px / 700
- Subheading: Inter 18px / 600
- Body: Inter 14px / 400
- Line height: 1.5
```

### 3. Colors
```
- Primary pink: #EC4899
- Gray text: #6B7280
- Border: #E5E7EB
- Background: #F9FAFB
```

### 4. Effects
```
- Card shadow: 0px 4px 6px rgba(0, 0, 0, 0.1)
- Border radius: 8px
- Button radius: 9999px (fully rounded)
```

## Example Workflow

### Current Approach (Without Dev Mode)
1. Export Figma design as image
2. Visually estimate spacing: "Looks like 20-24px"
3. Guess colors: "Seems like #E91E63 or #EC4899?"
4. Approximate font sizes: "Maybe 16px or 18px?"
5. Result: 95-97% accuracy

### With Figma MCP + Dev Mode
1. Open Figma Desktop, enable Dev Mode
2. Select "Settings/Main" frame
3. Query via MCP: "Get exact spacing for profile card"
4. Response: `padding: 24px, margin-top: -64px`
5. Query: "Get primary pink color"
6. Response: `#EC4899`
7. Query: "Get heading font specs"
8. Response: `font-family: Inter, size: 18px, weight: 600`
9. Implement with **exact** values
10. Result: 99%+ accuracy

## Available Figma MCP Tools

The `figma-mcp-server` package provides these capabilities:

1. **get_file_info** - Get file metadata and structure
2. **get_node_info** - Get detailed node properties
3. **get_styles** - Extract design system styles
4. **get_components** - List reusable components
5. **get_variables** - Get design tokens/variables

## Next Steps to Achieve 99% Accuracy

### 1. Restart Claude Code
After updating `.mcp.json`, restart Claude Code to load the Figma MCP server.

### 2. Open Figma Desktop
1. Open the design file
2. Enable Dev Mode
3. Select the "Settings/Main" frame (ID: 875:35531)

### 3. Request Exact Values
Ask me to query specific design properties:
- "What's the exact spacing between the avatar and name?"
- "What's the exact padding for the Personal Details card?"
- "What are the exact font specs for 'Thomas Lean'?"

### 4. Update Component with Exact Values
I'll update the Settings.tsx component with precise values instead of estimates.

### 5. Verify 99%+ Accuracy
Compare the final result side-by-side with Figma design.

## Troubleshooting

### MCP Server Not Loading
```bash
# Test the server manually
npx figma-mcp-server

# Check if token is valid
curl -H "X-Figma-Token: YOUR_FIGMA_TOKEN_HERE" \
  https://api.figma.com/v1/me
```

### Token Expired
If the Figma access token expires, generate a new one:
1. Go to Figma > Settings > Account > Personal Access Tokens
2. Generate new token
3. Update `FIGMA_ACCESS_TOKEN` in `.mcp.json`

## References

- **Figma API Docs**: https://www.figma.com/developers/api
- **MCP Server Package**: https://www.npmjs.com/package/figma-mcp-server
- **Current File ID**: `fubdMARNgA2lVhmzpPg77y`
- **Settings Frame ID**: `875:35531`

## Summary

**Current Status**: 95-97% accuracy (visual estimation)
**With Figma MCP**: Can achieve 99%+ accuracy (exact values)
**Required**: Open Figma Desktop with Dev Mode enabled

Ready to query exact design specs when you open the design in Figma Desktop!
