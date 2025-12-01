# 🌐 ALDO VISION + PENPOT API INTEGRATION
**Version 2.0 - Live API Integration Enabled**

---

## 🎉 NEW FEATURES

Aldo Vision now combines the best of both worlds:
1. **Local File Analysis** - Deep offline analysis with 13 personas
2. **Live API Integration** - Real-time access to Penpot designs via API

---

## 🚀 CAPABILITIES UNLOCKED

### **What You Can Now Do:**

✅ **Fetch designs directly from Penpot** (cloud or self-hosted)
✅ **Analyze live designs** without downloading files
✅ **Browse Penpot projects and files** programmatically
✅ **Search for specific designs** by name
✅ **Get real-time design data** always up-to-date
✅ **Combine with 13-persona deep analysis**
✅ **Generate professional reports** from live data
✅ **Work offline or online** - your choice!

---

## 📦 WHAT'S INCLUDED

### **New Modules:**
```
core/
└── penpot_api_connector.py   # Custom Penpot API integration (Python 3.9+)
```

### **Updated:**
```
main.py                        # Now supports --source file|api
config/
└── penpot_api.json           # API configuration
.env.example                   # API credentials template
```

---

## ⚙️ SETUP

### **Step 1: Configure Credentials**

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your credentials
PENPOT_API_URL=https://design.penpot.app
PENPOT_USERNAME=your_email@example.com
PENPOT_PASSWORD=your_password
```

### **Step 2: Test Connection**

```bash
# Test API connectivity
python3 -c "from core.penpot_api_connector import connect_to_penpot; \
            connector = connect_to_penpot(); \
            print('✅ Connected!' if connector else '❌ Failed')"
```

---

## 🎯 USAGE

### **Mode 1: Local File Analysis** (Original Mode)

```bash
# Analyze a downloaded .penpot file
python3 main.py design-file.penpot -v

# With specific personas
python3 main.py design-file.penpot -p product_designer accessibility_specialist

# Custom output directory
python3 main.py design-file.penpot -o ./my-reports
```

---

### **Mode 2: Live API Analysis** (NEW!)

```bash
# Analyze from Penpot API using File ID
python3 main.py FILE-ID-HERE --source api -v

# With API credentials from command line
python3 main.py FILE-ID --source api \
  --api-url https://design.penpot.app \
  --username your@email.com \
  --password your_password

# Using environment variables (recommended)
python3 main.py FILE-ID --source api -v

# With specific personas from API
python3 main.py FILE-ID --source api \
  -p product_designer design_systems_designer
```

---

## 🔍 FINDING FILE IDs

### **Method 1: Browse Projects** (Python)

```python
from core.penpot_api_connector import connect_to_penpot

# Connect
connector = connect_to_penpot()

# List all projects
projects = connector.list_projects()
for project in projects:
    print(f"Project: {project['name']} - ID: {project['id']}")

# List files in a project
files = connector.list_files(project_id='PROJECT-ID-HERE')
for file in files:
    print(f"File: {file['name']} - ID: {file['id']}")
```

### **Method 2: Search by Name**

```python
# Search for files
matching_files = connector.search_files('dashboard')
for file in matching_files:
    print(f"Found: {file['name']} - ID: {file['id']}")
```

### **Method 3: From Penpot URL**

```
Penpot URL format:
https://design.penpot.app/#/workspace/FILE-ID/...

Extract the FILE-ID from the URL
```

---

## 📊 WORKFLOW EXAMPLES

### **Example 1: Quick API Analysis**

```bash
# Set credentials once
export PENPOT_USERNAME="your@email.com"
export PENPOT_PASSWORD="your_password"

# Analyze multiple files quickly
python3 main.py file-id-1 --source api -v
python3 main.py file-id-2 --source api -v
python3 main.py file-id-3 --source api -v
```

### **Example 2: Hybrid Workflow**

```python
# 1. Fetch from API
from core.penpot_api_connector import connect_to_penpot

connector = connect_to_penpot()

# 2. Download file for offline analysis
connector.download_file('FILE-ID', 'downloaded-design.penpot')

# 3. Analyze locally with full depth
# python3 main.py downloaded-design.penpot -v
```

### **Example 3: Automated Monitoring**

```python
# Monitor and analyze new designs automatically
import schedule
import time

def analyze_latest_designs():
    connector = connect_to_penpot()
    projects = connector.list_projects()

    for project in projects:
        files = connector.list_files(project['id'])
        for file in files:
            # Analyze via API
            print(f"Analyzing {file['name']}...")
            # Run Aldo Vision analysis

schedule.every().day.at("09:00").do(analyze_latest_designs)

while True:
    schedule.run_pending()
    time.sleep(60)
```

---

## 🔧 API CONNECTOR FEATURES

### **Available Methods:**

```python
from core.penpot_api_connector import PenpotAPIConnector

connector = PenpotAPIConnector(
    api_url='https://design.penpot.app',
    username='your@email.com',
    password='your_password'
)

# Authentication
connector.authenticate()

# Browse
projects = connector.list_projects()
files = connector.list_files(project_id)

# Retrieve
file_data = connector.get_file_data(file_id)
metadata = connector.get_file_metadata(file_id)

# Search
results = connector.search_files('dashboard')

# Download
connector.download_file(file_id, 'output.penpot')

# Convert for Aldo Vision
aldo_data = connector.export_to_aldo_format(file_data)
```

---

## 📈 COMPARISON

| Feature | File Mode | API Mode |
|---------|-----------|----------|
| **Internet Required** | ❌ | ✅ |
| **Speed** | Fast (local) | Network dependent |
| **Always Current** | ❌ (snapshot) | ✅ (live data) |
| **Privacy** | ✅ (offline) | ⚠️ (API credentials) |
| **Batch Processing** | ✅ | ✅ |
| **Team Collaboration** | ❌ | ✅ |
| **13 Persona Analysis** | ✅ | ✅ |
| **Professional Reports** | ✅ | ✅ |
| **Works with Self-Hosted** | ✅ | ✅ |

---

## 🔐 SECURITY BEST PRACTICES

### **Environment Variables (Recommended):**

```bash
# Store credentials securely in .env
# Add .env to .gitignore
echo ".env" >> .gitignore

# Never commit credentials to git
git add .env.example  # ✅ Safe
# git add .env       # ❌ NEVER DO THIS
```

### **Alternative: Config File:**

```json
// config/penpot_credentials.json (add to .gitignore)
{
  "api_url": "https://design.penpot.app",
  "username": "your@email.com",
  "password": "your_password"
}
```

### **Self-Hosted Penpot:**

```bash
# For self-hosted instances
export PENPOT_API_URL="https://penpot.your-company.com"
export PENPOT_USERNAME="your_username"
export PENPOT_PASSWORD="your_password"

python3 main.py FILE-ID --source api
```

---

## 🎨 OUTPUT FORMATS

Both modes generate the same professional outputs:

### **Generated Files:**

```
output/
├── interactive_report.html        # Interactive HTML dashboard
├── comprehensive_report.pdf       # Professional PDF report
├── product_acceptance.json        # User stories (Given/When/Then)
├── design_acceptance.json         # Visual specifications
├── developer_specs.json           # Component APIs
├── claude_code_format.json        # AI-optimized guide
├── contextual_analysis.json       # Design rationale
└── analysis_summary.json          # Executive summary
```

---

## 🐛 TROUBLESHOOTING

### **Connection Failed:**

```bash
# Check API URL
echo $PENPOT_API_URL

# Test connectivity
curl -v https://design.penpot.app/api

# Verify credentials
python3 -c "from core.penpot_api_connector import connect_to_penpot; \
            connector = connect_to_penpot(); \
            print('Success' if connector.token else 'Failed')"
```

### **File Not Found:**

```bash
# List available files
python3 -c "from core.penpot_api_connector import connect_to_penpot; \
            c = connect_to_penpot(); \
            projects = c.list_projects(); \
            [print(f'Project: {p[\"name\"]}') for p in projects]"
```

### **Permission Denied:**

- Check user has access to the file/project
- Verify team membership in Penpot
- Confirm API credentials are correct

---

## 📚 FULL COMMAND REFERENCE

### **Common Flags:**

```bash
# Source selection
--source file          # Local file analysis (default)
--source api           # Penpot API analysis

# API Authentication
--api-url URL          # Penpot API endpoint
--username USER        # Penpot username
--password PASS        # Penpot password

# Output options
-o DIR                 # Output directory
-f html pdf json       # Output formats
-v                     # Verbose logging

# Analysis options
-p persona1 persona2   # Specific personas
-c config.json         # Custom config file
```

### **Complete Examples:**

```bash
# Example 1: Local file with all defaults
python3 main.py design.penpot

# Example 2: API with env credentials
python3 main.py abc123 --source api -v

# Example 3: API with inline credentials
python3 main.py abc123 --source api \
  --api-url https://design.penpot.app \
  --username user@example.com \
  --password secret123

# Example 4: Specific personas, PDF only
python3 main.py abc123 --source api \
  -p accessibility_specialist qa_engineer \
  -f pdf -v

# Example 5: Custom output directory
python3 main.py abc123 --source api \
  -o ./client-reports/2024-10 -v
```

---

## 🌟 ADVANCED FEATURES

### **Batch Analysis from API:**

```python
from core.penpot_api_connector import connect_to_penpot
from main import AldoVisionAgent
from main import AnalysisConfig

connector = connect_to_penpot()
agent = AldoVisionAgent()

# Get all files from a project
files = connector.list_files(project_id='PROJECT-ID')

# Analyze each file
for file in files:
    config = AnalysisConfig(
        input_file=file['id'],
        source_type='api',
        output_dir=f"output/{file['name']}"
    )

    results = agent.analyze_from_api(file['id'], config)
    agent.generate_comprehensive_reports(results, config.output_dir)
    print(f"✅ Analyzed: {file['name']}")
```

### **Scheduled Analysis:**

```bash
# Create a cron job for daily analysis
# crontab -e
0 9 * * * cd /path/to/aldo-vision && python3 main.py FILE-ID --source api -o ./daily-reports/$(date +\%Y-\%m-\%d)
```

---

## 🦸 COMBINED SUPERPOWERS

### **Aldo Vision (Local) + Penpot API:**

✅ 13 Expert Personas
✅ Live Penpot Integration
✅ Offline & Online Modes
✅ Professional HTML/PDF Reports
✅ Accessibility Compliance (WCAG)
✅ Design System Analysis
✅ Component Detection
✅ Code Generation Specs
✅ Security Analysis
✅ Real-time Updates
✅ Team Collaboration
✅ Self-Hosted Support

---

## 📖 DOCUMENTATION

- **Main README**: `README.md`
- **Usage Guide**: `USAGE.md`
- **Library List**: `SUPERMAN_VISION_LIBRARIES.md`
- **Tool Inventory**: `COMPLETE_TOOLKIT_INVENTORY.md`
- **Design Tools MCP**: `DESIGN_TOOLS_MCP_ANALYSIS.md`
- **This Guide**: `PENPOT_API_INTEGRATION.md`

---

## 🎯 CONCLUSION

**Aldo Vision v2.0 is now the most powerful Penpot design analysis tool available:**

- ✅ Works with local files AND live API
- ✅ 13-persona deep analysis
- ✅ Professional automated reports
- ✅ Cloud AND self-hosted Penpot
- ✅ Python 3.9+ compatible (no upgrade needed)
- ✅ Secure credential management
- ✅ Batch processing support
- ✅ Real-time design monitoring

**You now have Superman-level vision for Penpot designs - both offline and online!** 🦸🌐

---

## 🚀 QUICK START

```bash
# 1. Setup credentials
cp .env.example .env
# Edit .env with your Penpot credentials

# 2. Test connection
python3 -c "from core.penpot_api_connector import connect_to_penpot; print('✅ Connected!' if connect_to_penpot() else '❌ Failed')"

# 3. Analyze from API
python3 main.py YOUR-FILE-ID --source api -v

# Done! 🎉
```
