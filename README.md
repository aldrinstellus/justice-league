# Aldo Vision Agent

**Comprehensive Penpot Design File Analysis Agent**

Aldo Vision is an advanced multi-persona analysis agent that provides deep insights into Penpot design files from 11 different professional perspectives, generating comprehensive visual reports with interactive HTML and PDF outputs.

## 🎯 Agent Overview

This agent analyzes design files through the lens of:

1. **Product Manager** - Business requirements & user journeys
2. **Product Designer** - UX patterns & design rationale
3. **AI Developer** - Technical patterns & automation opportunities
4. **Core File Analyzer** - Technical architecture & file structure
5. **Design Systems Designer** - Component consistency & scalability
6. **Design Systems Engineer** - Technical implementation & architecture
7. **Accessibility Specialist** - WCAG compliance & inclusive design
8. **Content Strategist** - Information architecture & content design
9. **QA/Test Engineer** - Testing strategy & quality assurance
10. **Security Analyst** - Privacy & security considerations
11. **Visual Report Generator** - Interactive documentation & visual communication

## 🚀 Key Features

### Multi-Perspective Analysis
- **Business Intelligence**: Strategic reasoning and user needs analysis
- **Design Rationale**: Aesthetic choices and UX patterns explanation
- **Technical Insights**: Implementation patterns and architecture analysis
- **Future-Proofing**: AI/Web3/multimodal interface preparation

### Output Formats
- **Product Acceptance Criteria**: User stories with Given/When/Then format
- **Design Acceptance Criteria**: Visual specifications and interaction requirements
- **Developer Specifications**: Component APIs, testing requirements, technical specs
- **Claude Code Ready**: AI-optimized project context for pixel-perfect implementation
- **Contextual Analysis**: Screen purpose, user mental models, design rationale

### Visual Reporting
- **Interactive HTML Reports**: Clickable dashboards, component galleries, deep-linked navigation
- **Professional PDF Reports**: High-resolution screenshots with annotations
- **Component Screenshots**: Isolated component visuals with specifications
- **Cross-Tool Integration**: Direct links to Penpot, Figma, Storybook, GitHub

## 📁 Project Structure

```
aldo-vision/
├── README.md                 # This file
├── package.json             # Dependencies and scripts
├── main.py                  # Main agent orchestrator
├── config/
│   ├── personas.json        # Persona configurations
│   ├── output_formats.json  # Report template settings
│   └── visual_config.json   # Screenshot and annotation settings
├── core/
│   ├── penpot_extractor.py  # Penpot file extraction and parsing
│   ├── analysis_engine.py   # Core analysis orchestration
│   └── component_detector.py # UI component identification
├── personas/
│   ├── product_manager.py
│   ├── product_designer.py
│   ├── ai_developer.py
│   ├── file_analyzer.py
│   ├── design_systems_designer.py
│   ├── design_systems_engineer.py
│   ├── accessibility_specialist.py
│   ├── content_strategist.py
│   ├── qa_engineer.py
│   ├── security_analyst.py
│   └── visual_reporter.py
├── output_generators/
│   ├── product_acceptance.py    # Product acceptance criteria generator
│   ├── design_acceptance.py     # Design acceptance criteria generator
│   ├── developer_specs.py       # Developer specification generator
│   ├── claude_code_format.py    # Claude Code consumable format
│   └── contextual_analysis.py   # Screen context analysis
├── visual_system/
│   ├── screenshot_engine.py     # Component and screen capture
│   ├── html_generator.py        # Interactive HTML report generation
│   ├── pdf_generator.py         # Professional PDF report generation
│   ├── annotation_system.py     # Visual markup and annotations
│   └── linking_system.py        # Cross-reference and deep linking
├── templates/
│   ├── html/                    # HTML report templates
│   ├── pdf/                     # PDF report templates
│   └── components/              # Reusable template components
├── assets/
│   ├── personas/                # Persona avatars and icons
│   ├── templates/               # Report styling assets
│   └── examples/                # Example outputs
└── tests/
    ├── test_extraction.py       # Penpot extraction tests
    ├── test_personas.py         # Persona analysis tests
    ├── test_visual_system.py    # Visual reporting tests
    └── fixtures/                # Test data and fixtures
```

## 🛠 Installation & Setup

```bash
cd aldo-agents/aldo-vision
pip install -r requirements.txt
```

## 📖 Usage

### Basic Analysis
```python
from main import AldoVisionAgent

agent = AldoVisionAgent()
results = agent.analyze_penpot_file("path/to/design.penpot")
```

### Generate Reports
```python
# Generate all output formats
reports = agent.generate_comprehensive_reports(results)

# Access specific outputs
html_report = reports['interactive_html']
pdf_report = reports['professional_pdf']
acceptance_criteria = reports['product_acceptance_criteria']
```

### Custom Analysis
```python
# Run specific persona analysis
pm_analysis = agent.run_persona_analysis('product_manager', results)
design_analysis = agent.run_persona_analysis('design_systems_designer', results)
```

## 🔧 Configuration

Configure persona weights, output preferences, and visual settings in the `config/` directory.

## 📊 Example Outputs

See `assets/examples/` for sample reports generated from various design files.

## 🤝 Contributing

This agent is part of the Aldo Agents ecosystem. See the main aldo-agents README for contribution guidelines.

## 📄 License

Part of the Aldo Agents project - see main project license.