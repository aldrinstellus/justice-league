# Aldo Vision Usage Guide

Complete guide for using the Aldo Vision agent to analyze Penpot design files.

## 🚀 Quick Start

### 1. Installation

```bash
cd aldo-agents/aldo-vision
pip install -r requirements.txt
```

### 2. Basic Usage

```bash
# Analyze a Penpot file
python main.py path/to/your/design.penpot

# Specify output directory
python main.py path/to/design.penpot --output-dir reports/my-analysis

# Generate specific output formats
python main.py design.penpot --output-formats html pdf json
```

### 3. View Results

After analysis completes, open the interactive HTML report:

```bash
# Open in browser
open output/interactive_report.html

# Or serve with local server
python -m http.server 8000 --directory output
# Then visit http://localhost:8000/interactive_report.html
```

## 📊 Analysis Features

### Multi-Persona Analysis

Aldo Vision analyzes your design from 11 different professional perspectives:

1. **🎯 Product Manager** - Business requirements, user journeys, acceptance criteria
2. **🎨 Product Designer** - UX patterns, design rationale, interaction design
3. **🤖 AI Developer** - Technical patterns, automation opportunities
4. **🔍 Core File Analyzer** - File structure, technical architecture
5. **🧩 Design Systems Designer** - Component consistency, scalability
6. **⚙️ Design Systems Engineer** - Technical implementation, APIs
7. **♿ Accessibility Specialist** - WCAG compliance, inclusive design
8. **📝 Content Strategist** - Information architecture, content design
9. **🧪 QA Engineer** - Testing strategy, quality assurance
10. **🔒 Security Analyst** - Security patterns, privacy considerations
11. **📸 Visual Reporter** - Interactive documentation, screenshots

### Output Formats

#### 1. Interactive HTML Report
- **Dashboard view** with key metrics and insights
- **Component gallery** with live examples
- **Cross-linked navigation** between personas
- **Search functionality** across all content
- **Responsive design** for mobile/desktop viewing

#### 2. Professional PDF Report
- **Executive summary** with visual highlights
- **High-resolution screenshots** with annotations
- **Print-ready formatting** with proper typography
- **Table of contents** and cross-references

#### 3. Structured Data Formats
- **Product Acceptance Criteria** (JSON) - User stories with Given/When/Then format
- **Design Acceptance Criteria** (JSON) - Visual specifications and interaction requirements
- **Developer Specifications** (JSON) - Component APIs, testing requirements
- **Claude Code Ready Format** (JSON) - AI-optimized implementation context

## 🎛 Command Line Options

### Basic Options

```bash
python main.py <input_file> [options]
```

**Required:**
- `input_file` - Path to your .penpot file

**Optional:**
- `--output-dir, -o` - Output directory (default: `output`)
- `--personas, -p` - Specific personas to analyze (default: all)
- `--output-formats, -f` - Output formats to generate
- `--config, -c` - Path to configuration file
- `--verbose, -v` - Enable verbose logging

### Examples

```bash
# Analyze specific personas only
python main.py design.penpot -p product_manager design_systems_designer

# Generate only HTML and PDF reports
python main.py design.penpot -f html pdf

# Use custom configuration
python main.py design.penpot -c my-config.json

# Verbose output for debugging
python main.py design.penpot -v
```

## ⚙️ Configuration

### Custom Configuration File

Create a JSON configuration file to customize analysis:

```json
{
  "personas": {
    "enabled": [
      "product_manager",
      "design_systems_designer",
      "accessibility_specialist"
    ],
    "weights": {
      "product_manager": 1.0,
      "design_systems_designer": 0.8,
      "accessibility_specialist": 0.9
    }
  },
  "output_formats": ["html", "pdf"],
  "visual": {
    "screenshot_quality": "high",
    "annotation_style": "professional",
    "theme": "government"
  }
}
```

### Environment Variables

Set environment variables for global configuration:

```bash
export ALDO_VISION_OUTPUT_DIR="/path/to/reports"
export ALDO_VISION_QUALITY="high"
export ALDO_VISION_THEME="professional"
```

## 📂 Understanding Output Structure

After analysis, you'll find these files in your output directory:

```
output/
├── interactive_report.html      # Main interactive report
├── comprehensive_report.pdf     # Professional PDF report
├── analysis_summary.json        # Executive summary data
├── product_acceptance.json      # User stories & acceptance criteria
├── design_acceptance.json       # Design specifications
├── developer_specs.json         # Technical implementation specs
├── claude_code_format.json      # AI-ready implementation context
├── contextual_analysis.json     # Screen context & user scenarios
└── screenshots/                 # Generated visual assets
    ├── main_application_full.png
    ├── component_button_primary.png
    ├── component_gallery.png
    └── ...
```

## 🎨 Working with Results

### Interactive HTML Report

The HTML report includes:

**Executive Dashboard**
- Key metrics and statistics
- Design quality score
- Business impact summary
- Next steps recommendations

**Component Gallery**
- Interactive component showcase
- Usage statistics and specifications
- Variant documentation
- Consistency scores

**Persona Analysis Sections**
- Detailed findings from each perspective
- Visual evidence and screenshots
- Prioritized recommendations
- Action items and success metrics

### Product Acceptance Criteria

The generated acceptance criteria include:

```json
{
  "user_stories": [
    {
      "id": "US-001",
      "title": "Grant Application Submission",
      "user_story": "As a grant applicant, I want to submit my application online...",
      "acceptance_criteria": [
        {
          "id": "US-001-AC-01",
          "given": "I am on the application form page",
          "when": "I fill out all required fields",
          "then": "I can successfully submit my application"
        }
      ],
      "definition_of_done": [...],
      "business_rules": [...],
      "priority": "High"
    }
  ]
}
```

### Claude Code Ready Format

Perfect for AI-assisted development:

```json
{
  "project_context": {
    "name": "Wisconsin DNR Grant Management System",
    "type": "Government Web Application",
    "primary_users": ["Grant Applicants", "DNR Staff"]
  },
  "implementation_prompts": {
    "component_generation": "Create a React component for grant application form with validation...",
    "api_integration": "Implement API integration for form submission..."
  }
}
```

## 🔧 Advanced Usage

### Programmatic Usage

```python
from main import AldoVisionAgent

# Initialize agent
agent = AldoVisionAgent()

# Run analysis
results = agent.analyze_penpot_file("design.penpot")

# Generate specific reports
html_report = agent.html_generator.generate_report(results, visual_assets)
pdf_report = agent.pdf_generator.generate_report(results, visual_assets)

# Access specific persona analysis
pm_analysis = results['persona_analyses']['product_manager']
design_analysis = results['persona_analyses']['design_systems_designer']
```

### Custom Persona Analysis

```python
# Run single persona analysis
pm_results = agent.run_persona_analysis('product_manager', results)

# Add custom analysis
custom_insights = {
    'business_priority': 'high',
    'implementation_complexity': 'medium',
    'user_impact': 'high'
}
results['custom_analysis'] = custom_insights
```

### Batch Processing

```python
import os
from pathlib import Path

# Analyze multiple files
penpot_files = Path('designs').glob('*.penpot')
for file_path in penpot_files:
    print(f"Analyzing {file_path.name}...")
    results = agent.analyze_penpot_file(str(file_path))

    # Generate reports in separate directories
    output_dir = f"reports/{file_path.stem}"
    reports = agent.generate_comprehensive_reports(results, output_dir)
    print(f"Reports saved to {output_dir}")
```

## 🚨 Troubleshooting

### Common Issues

**1. "File not found" error**
```bash
# Ensure file path is correct and file exists
ls -la path/to/your/file.penpot

# Use absolute path if needed
python main.py "/full/path/to/design.penpot"
```

**2. "Permission denied" error**
```bash
# Check file permissions
chmod 644 design.penpot

# Check output directory permissions
chmod 755 output/
```

**3. "Module not found" error**
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

**4. Memory issues with large files**
```bash
# Use lower quality settings for large files
python main.py design.penpot --config low-memory-config.json
```

**5. Screenshot generation fails**
```bash
# Install system dependencies (macOS)
brew install cairo pango gdk-pixbuf libffi

# Install system dependencies (Ubuntu)
sudo apt-get install libcairo2-dev libpango1.0-dev libgdk-pixbuf2.0-dev libffi-dev
```

### Performance Optimization

**For Large Files (>50MB):**
```json
{
  "visual": {
    "screenshot_quality": "medium",
    "generate_component_isolation": false,
    "annotation_density": "low"
  },
  "analysis": {
    "deep_analysis": false,
    "concurrent_processing": true
  }
}
```

**For Faster Analysis:**
```bash
# Analyze only critical personas
python main.py design.penpot -p product_manager design_systems_designer

# Skip visual generation
python main.py design.penpot --no-screenshots

# Generate only essential formats
python main.py design.penpot -f json
```

## 📞 Support

### Debug Mode

```bash
# Enable detailed logging
python main.py design.penpot --verbose

# Check log file
tail -f aldo-vision.log
```

### Getting Help

1. **Check the logs** in `aldo-vision.log`
2. **Review configuration** in `config/` directory
3. **Verify file format** - ensure it's a valid .penpot file
4. **Test with sample files** in `assets/examples/`

### Performance Monitoring

```python
import time
start_time = time.time()

# Run analysis
results = agent.analyze_penpot_file("design.penpot")

end_time = time.time()
print(f"Analysis completed in {end_time - start_time:.2f} seconds")
```

This comprehensive usage guide should help you get the most out of the Aldo Vision agent for your design analysis needs.