# Justice League Heroes - Complete Reference Guide

**Last Updated**: 2025-10-30 (Auto-updated by Oracle Meta Agent)
**Version**: 1.9.3
**Total Heroes**: 18

---

## 🦸 Core Team (6 Heroes)

### 1. 🦸 Superman - Mission Coordinator

**Role**: Central mission orchestrator and team leader
**File**: `core/justice_league/superman_coordinator.py`
**Narrator**: ✅ Yes (creates and distributes to all heroes)

**Capabilities**:
- Mission planning and coordination across all heroes
- Figma file analysis and frame export coordination
- Hero deployment based on mission requirements
- Progress tracking and result aggregation
- Unified narrator system management

**Key Methods**:
- `assemble_justice_league(mission)` - Coordinate full team analysis
- `_deploy_hawkman_frame_export(mission)` - Export Figma frames as PNG
- `coordinate_design_conversion(figma_url)` - Orchestrate Figma-to-Code conversion

**When to Use**:
- Any multi-hero mission requiring coordination
- Figma file conversions
- Complex design analysis requiring multiple specialists
- Frame export operations

**Powers**:
- Team coordination and resource allocation
- Mission strategy and planning
- Hero capability matching to mission requirements
- Unified progress reporting

---

### 2. 🔮 Oracle - Meta Learning Agent

**Role**: Pattern learning, knowledge management, and continuous improvement
**File**: `core/justice_league/oracle_meta_agent.py`
**Narrator**: ✅ Yes

**Capabilities**:
- Project pattern learning and storage
- Methodology tracking and optimization
- User preference management
- Decision matrix for routing missions
- Learning session management
- Auto-updates documentation (including this file)

**Key Methods**:
- `get_project_context(file_key)` - Retrieve learned patterns for project
- `update_patterns(file_key, new_patterns)` - Store new learnings
- `start_learning_session()` - Begin structured learning
- `complete_learning_session(session)` - Finalize and store learnings
- `query_methodologies()` - Get available conversion methodologies

**When to Use**:
- Before starting any conversion (get context)
- After completing conversions (store learnings)
- When choosing between methodologies
- For preference management

**Powers**:
- Pattern recognition across projects
- Methodology effectiveness tracking
- User preference learning
- Decision automation based on historical data

**Data Storage**: `/data/oracle_project_patterns.json`

---

### 3. 🎨 Artemis - Code Generation Specialist

**Role**: Figma-to-Code conversion and component generation
**File**: `core/justice_league/artemis_codesmith.py`
**Narrator**: ✅ Yes (Friendly personality)

**Capabilities**:
- React/TypeScript component generation
- shadcn/ui component library integration
- Tailwind CSS styling
- Automatic code refinement (up to 7 iterations)
- Component testing and story generation
- Knowledge-based code generation

**Key Methods**:
- `generate_component_code_expert(figma_url, component_name, options)` - Generate code from Figma
- `refine_code(existing_code, feedback)` - Improve existing code
- `generate_test_files(component_code)` - Create test suites
- `generate_storybook_story(component_code)` - Generate Storybook stories

**When to Use**:
- Converting Figma designs to React components
- Generating shadcn/ui based components
- Creating production-ready TypeScript code
- Need iterative refinement for accuracy

**Powers**:
- Code generation with 70-85% accuracy (Figma API)
- 90-95% accuracy (Image-to-HTML method)
- Automatic refinement loops
- Oracle context integration for better results
- Knowledge base learning

**Accuracy Targets**: 99% with iterative refinement

---

### 4. 🎯 Green Arrow - Visual Validator

**Role**: Pixel-perfect WYSIWYG validation
**File**: `core/justice_league/green_arrow_visual_validator.py`
**Narrator**: ✅ Yes (Tactical personality)

**Capabilities**:
- Pixel-by-pixel visual comparison
- Screenshot-based validation
- Accuracy scoring (0-100%)
- Issue categorization (CRITICAL, HIGH, MEDIUM, LOW)
- Actionable fix recommendations
- ±2px tolerance for precision

**Key Methods**:
- `validate_visual_accuracy(figma_url, rendered_html)` - Compare design vs implementation
- `calculate_accuracy_score(comparison_results)` - Compute accuracy percentage
- `generate_fix_recommendations(issues)` - Create actionable fixes
- `capture_screenshots(url)` - Screenshot generation

**When to Use**:
- Validating generated code accuracy
- Before finalizing conversions
- Quality assurance for pixel-perfect requirements
- Identifying visual discrepancies

**Powers**:
- Pixel-perfect accuracy detection
- Spacing, color, typography validation
- Layout structure verification
- Visual regression detection

**Accuracy Thresholds**:
- 98-100%: ✅ EXCELLENT
- 95-97%: ✅ GOOD
- 90-94%: ⚠️ ACCEPTABLE
- <90%: ❌ NEEDS WORK

---

### 5. 🦅 Hawkman - Structural Parser & Frame Exporter

**Role**: Figma layer parsing and PNG frame export
**File**: `core/justice_league/hawkman_equipped.py`
**Narrator**: ✅ Yes

**Capabilities**:
- Layer-by-layer Figma parsing
- Structural analysis and component detection
- Batch PNG frame export (production-tested: 177 frames)
- Configurable export scale (1x-4x)
- Progress tracking with visual indicators
- Interactive folder selection

**Key Methods**:
- `parse_figma_structure(file_key, node_id)` - Parse Figma hierarchy
- `export_all_frames_as_png(file_key, output_dir, scale)` - Batch frame export
- `analyze_component_structure(node)` - Component boundary detection
- `extract_design_tokens(structure)` - Design system extraction

**When to Use**:
- Exporting all frames from Figma as PNG images
- Analyzing Figma file structure
- Creating visual reference libraries
- Preparing for Image-to-HTML conversion

**Powers**:
- Batch frame export with retry logic
- Configurable export quality (1x-4x scale)
- Progress tracking with ETA
- Interactive UX with folder prompts
- 100% success rate (production-tested)

**Production Record**: 177 frames exported in ~20 minutes

---

### 6. 👁️ Vision Analyst - Visual Measurement Specialist

**Role**: Dashboard image analysis and measurement extraction
**File**: `core/justice_league/vision_analyst.py`
**Narrator**: ✅ Yes (Observant personality)

**Capabilities**:
- Dashboard image analysis
- Layout pattern detection (header, sidebar, grid, etc.)
- Color palette extraction
- Typography system detection
- Spacing and dimension measurement
- Component identification
- Artemis brief generation

**Key Methods**:
- `analyze_dashboard_image(image_description, dimensions)` - Extract visual data
- `generate_artemis_brief(analysis)` - Create build instructions
- `detect_layout_patterns(structure)` - Identify UI patterns
- `extract_color_palette(image)` - Get color system
- `measure_spacing_system(layout)` - Calculate spacing patterns

**When to Use**:
- Converting dashboard screenshots to code
- Image-to-HTML methodology (90-95% accuracy)
- When Figma API accuracy is insufficient (<70%)
- Building fresh HTML from visual reference

**Powers**:
- Visual pattern recognition
- Precise measurement extraction
- Layout system detection
- Color and typography analysis
- Sequential thinking for complex dashboards

**Accuracy**: 90-95% for complex dashboards

---

## 🧪 Testing & QA Heroes (5 Heroes)

### 7. 🦇 Batman - Interactive Testing

**Role**: User interaction and functionality testing
**File**: `core/justice_league/batman_testing.py`
**Narrator**: ✅ Yes

**Capabilities**:
- Interactive element testing (buttons, forms, links)
- User flow validation
- Event handler verification
- State management testing
- Browser automation

**Key Methods**:
- `test_interactive_elements(component)` - Test all interactions
- `validate_user_flows(scenarios)` - Test user journeys
- `test_event_handlers(element)` - Verify click, hover, etc.
- `test_form_validation(form)` - Form testing

**When to Use**:
- Testing interactive components
- Validating user workflows
- Ensuring proper event handling
- Quality assurance before deployment

**Powers**:
- Comprehensive interaction testing
- User journey validation
- Edge case detection
- Browser compatibility testing

---

### 8. 💚 Green Lantern - Visual Regression Testing

**Role**: Visual regression detection and baseline management
**File**: `core/justice_league/green_lantern_visual.py`
**Narrator**: ✅ Yes

**Capabilities**:
- Visual baseline storage
- Regression detection
- Screenshot comparison
- Similarity scoring
- Layout shift detection

**Key Methods**:
- `store_baseline(image_path, test_name)` - Save baseline screenshot
- `compare_with_baseline(current_image, test_name)` - Detect regressions
- `calculate_similarity(baseline, current)` - Compute similarity score
- `detect_layout_shifts(comparison)` - Find layout changes

**When to Use**:
- Preventing visual regressions
- Validating design consistency
- CI/CD pipeline integration
- Multi-version comparison

**Powers**:
- Pixel-perfect regression detection
- Baseline management
- Similarity scoring
- Layout shift detection

**Storage**: `/tmp/aldo-vision-baselines/` (configurable)

---

### 9. ⚡ Wonder Woman - Accessibility Champion

**Role**: WCAG 2.2 accessibility validation
**File**: `core/justice_league/wonder_woman_accessibility.py`
**Narrator**: ✅ Yes

**Capabilities**:
- WCAG 2.2 Level AAA compliance
- axe-core integration (57% auto-detection)
- Color contrast analysis (CIELAB Delta E)
- Keyboard navigation testing
- Screen reader compatibility
- ARIA pattern validation

**Key Methods**:
- `champion_accessibility_analysis(design_data, html)` - Complete a11y audit
- `analyze_color_contrast(colors)` - WCAG contrast validation
- `validate_aria_patterns(html)` - ARIA compliance
- `test_keyboard_navigation(page)` - Keyboard accessibility

**When to Use**:
- WCAG compliance validation
- Government/enterprise projects (accessibility required)
- Before production deployment
- Legal compliance needs

**Powers**:
- Industry-leading axe-core integration
- Advanced color science (Delta E)
- Comprehensive WCAG 2.2 coverage
- Lighthouse 13.0 integration
- Chrome DevTools Protocol (30+ tools)

**Compliance Levels**: A, AA, AAA

---

### 10. ⚡ Flash - Performance Profiling

**Role**: Performance analysis and Core Web Vitals
**File**: `core/justice_league/flash_performance.py`
**Narrator**: ✅ Yes

**Capabilities**:
- Chrome DevTools Performance API
- Core Web Vitals (LCP, FID, CLS, FCP, TTI, TBT)
- Lighthouse performance audits
- Performance regression detection
- Speed Index calculation
- Frame rate monitoring

**Key Methods**:
- `profile_performance(mcp_tools, test_name, url)` - Run performance trace
- `analyze_core_web_vitals(trace_data)` - Extract CWV metrics
- `detect_performance_regressions(current, baseline)` - Compare performance
- `generate_optimization_recommendations(results)` - Improvement suggestions

**When to Use**:
- Performance optimization
- Core Web Vitals validation
- Lighthouse audits
- Performance regression prevention

**Powers**:
- Sub-millisecond timing accuracy
- Real browser performance profiling
- Core Web Vitals measurement
- Performance bottleneck detection

**MCP Tools Required**: Chrome DevTools MCP integration

---

### 11. 🎨 Plastic Man - Responsive Design Testing

**Role**: Multi-device and responsive testing
**File**: `core/justice_league/plastic_man_responsive.py`
**Narrator**: ✅ Yes

**Capabilities**:
- 10 breakpoint testing (smartwatch to 4K)
- Device-specific testing (iPhone, Android, iPad)
- Touch target validation (WCAG AAA: 44x44px)
- Orientation testing (portrait/landscape)
- Viewport meta tag verification
- Responsive image optimization

**Key Methods**:
- `test_all_breakpoints(mcp_tools, scenarios)` - Test all device sizes
- `validate_touch_targets(snapshot)` - Ensure tappable elements
- `test_orientation_changes(page)` - Portrait/landscape testing
- `analyze_responsive_patterns(breakpoints)` - Responsive strategy analysis

**When to Use**:
- Mobile-first development validation
- Cross-device compatibility testing
- Touch interface validation
- Responsive design QA

**Powers**:
- 10 standard breakpoints pre-configured
- Touch target size validation
- Device emulation
- Responsive pattern detection

**Breakpoints**: Smartwatch (272px) to 4K (3840px)

---

## 🔧 Integration & Security Heroes (3 Heroes)

### 12. 🌊 Aquaman - Network Analysis

**Role**: Network traffic and resource loading specialist
**File**: `core/justice_league/aquaman_network.py`
**Narrator**: ✅ Yes

**Capabilities**:
- Network request monitoring (all HTTP/HTTPS)
- Resource waterfall analysis
- Critical path detection
- Blocking resource identification
- Request/response timing
- Cache efficiency analysis
- CDN performance validation

**Key Methods**:
- `analyze_network_traffic(mcp_tools, resource_types)` - Monitor all requests
- `identify_blocking_resources(requests)` - Find render-blocking assets
- `analyze_waterfall_timing(requests)` - Timing breakdown
- `generate_optimization_plan(analysis)` - Network improvements

**When to Use**:
- Network performance optimization
- Resource loading analysis
- Third-party script auditing
- CDN effectiveness validation

**Powers**:
- Complete network visibility
- Waterfall analysis
- Critical path identification
- Cache strategy validation

**MCP Tools Required**: Chrome DevTools network monitoring

---

### 13. 🤖 Cyborg - Integration Master

**Role**: External API and system integrations
**File**: `core/justice_league/cyborg_integrations.py`
**Narrator**: ✅ Yes

**Capabilities**:
- Figma API integration (OAuth, file extraction)
- Penpot API integration (open-source design)
- GitHub API integration (repository operations)
- Jira/Linear integration (issue tracking)
- Slack/Discord notifications
- Webhook management
- Generic REST API client

**Key Methods**:
- `connect_all_systems(credentials)` - Initialize all integrations
- `sync_figma_components(file_key)` - Sync Figma data
- `create_github_issue(repo, issue_data)` - GitHub operations
- `send_notification(platform, message)` - Cross-platform notifications

**When to Use**:
- Connecting to external design tools
- Issue tracker integration
- Notification systems
- Data synchronization

**Powers**:
- Multi-platform integration
- OAuth authentication
- Webhook management
- Data synchronization

**Supported Platforms**: Figma, Penpot, GitHub, Jira, Linear, Slack, Discord

---

### 14. 🧠 Martian Manhunter - Security Guardian

**Role**: Security vulnerability scanning and testing
**File**: `core/justice_league/martian_manhunter_security.py`
**Narrator**: ✅ Yes

**Capabilities**:
- OWASP Top 10 vulnerability scanning
- Authentication/authorization testing
- Session management validation
- SSL/TLS certificate checking
- Security header verification
- Dependency vulnerability scanning
- Secrets detection
- Penetration testing simulation

**Key Methods**:
- `scan_all_vulnerabilities(target_data)` - Comprehensive security scan
- `test_authentication(auth_data)` - Auth vulnerability testing
- `scan_dependencies(package_json)` - Dependency audit
- `detect_secrets(code_paths)` - Secret scanning

**When to Use**:
- Pre-deployment security audits
- Vulnerability assessments
- Compliance validation
- Penetration testing

**Powers**:
- OWASP Top 10 coverage
- Dependency vulnerability detection
- Secret scanning
- Security header validation

**Telepathic Powers**: Detects vulnerabilities before attackers

---

## 🎯 Specialty Heroes (4 Heroes)

### 15. 🔬 The Atom - Component Analysis

**Role**: Component library and design system validation
**File**: `core/justice_league/atom_component_analysis.py`
**Narrator**: ✅ Yes

**Capabilities**:
- Component variant enumeration
- Design token consistency validation
- Component accessibility testing
- Bulk component testing
- Design system compliance
- Pattern library analysis
- Naming convention validation

**Key Methods**:
- `analyze_component_library(components, design_tokens)` - Full library audit
- `enumerate_variants(components)` - List all component variations
- `validate_design_tokens(components, tokens)` - Token consistency
- `validate_naming_conventions(components)` - Naming standards

**When to Use**:
- Design system audits
- Component library validation
- Design token consistency checks
- Pattern library analysis

**Powers**:
- Molecular-level component analysis
- Variant enumeration
- Design token validation
- Consistency checking

**Analysis Focus**: Buttons, inputs, typography, colors, spacing

---

### 16. 🎩 Zatanna - SEO Specialist

**Role**: SEO optimization and metadata validation
**File**: `core/justice_league/zatanna_seo.py`
**Narrator**: ✅ Yes

**Capabilities**:
- Meta tag validation (title, description, OG tags)
- Structured data detection (Schema.org)
- Heading hierarchy validation
- Image alt text coverage
- Internal linking structure
- Core Web Vitals impact on SEO
- Crawlability assessment
- Mobile-friendliness

**Key Methods**:
- `analyze_seo_magic(mcp_tools, url)` - Complete SEO analysis
- `validate_meta_tags(snapshot)` - Meta tag audit
- `detect_structured_data(html)` - Schema.org validation
- `analyze_heading_hierarchy(html)` - H1-H6 structure

**When to Use**:
- SEO optimization
- Pre-launch SEO audits
- Metadata validation
- Search engine compliance

**Powers**:
- Backwards magic spell casting
- Complete SEO analysis
- Structured data detection
- Meta tag optimization

**Magic Spells**: "!sgat atem laeveR" (Reveal meta tags!)

**SEO Best Practices**:
- Title: 30-60 characters
- Description: 120-160 characters
- Max 1 H1 per page
- Structured data (13 schemas supported)

---

### 17. 🪔 Litty - Ethics & Empathy Validator

**Role**: Ethical design and user empathy validation
**File**: `core/justice_league/litty_ethics.py`
**Narrator**: ✅ Yes

**Capabilities**:
- Dark pattern detection (15 types)
- User empathy validation
- Inclusive design advocacy
- User story generation
- Ethical UX validation
- Elderly/disabled user perspective
- Guilt-tripping for developer awareness

**Key Methods**:
- `validate_ethical_design(design_data)` - Dark pattern detection
- `generate_user_stories(personas)` - Real impact narratives
- `analyze_inclusivity(design)` - Inclusive design audit
- `guilt_trip_developer(issues)` - Empathy inducement

**When to Use**:
- Ethical design validation
- Dark pattern prevention
- Accessibility from empathy perspective
- User impact assessment

**Powers**:
- Dark pattern detection (15 types)
- User persona empathy generation
- Ethical validation
- Malayali guilt-tripping phrases

**Personas**: Ammachi (grandma), visually impaired, elderly, rural user, dyslexic

**Catchphrase**: "Eda mone! Do you know how your ammachi would struggle with this?"

**Dark Patterns Detected**: Forced continuity, confirmshaming, hidden costs, roach motel, etc.

---

### 18. 🔨 Hephaestus - Component Builder

**Role**: Physical component construction and assembly
**File**: `core/justice_league/hephaestus_builder.py`
**Narrator**: ❌ No (static builder)

**Capabilities**:
- Component file generation
- Directory structure creation
- Template scaffolding
- File system operations
- Build tooling integration

**Key Methods**:
- `build_component(template, output_path)` - Create component files
- `scaffold_project(structure)` - Generate project structure
- `generate_from_template(template_data)` - Template rendering

**When to Use**:
- Creating new component files
- Project scaffolding
- File generation from templates
- Build automation

**Powers**:
- Component file creation
- Template rendering
- Directory scaffolding
- Build integration

---

## 📊 Hero Selection Matrix

### By Use Case

**Figma-to-Code Conversion**:
1. 🔮 Oracle - Get project context
2. 🎨 Artemis - Generate code
3. 🎯 Green Arrow - Validate accuracy
4. 🔮 Oracle - Store learnings

**Image-to-HTML Conversion**:
1. 🔮 Oracle - Sequential thinking framework
2. 👁️ Vision Analyst - Extract measurements
3. 🎨 Artemis - Build from measurements
4. 🎯 Green Arrow - Validate accuracy
5. 🔮 Oracle - Store methodology

**Frame Export**:
1. 🦸 Superman - Coordinate export mission
2. 🦅 Hawkman - Export all frames as PNG
3. 🔮 Oracle - Track metadata (optional)

**Quality Assurance**:
- 🦇 Batman - Interactive testing
- 💚 Green Lantern - Visual regression
- ⚡ Wonder Woman - Accessibility
- ⚡ Flash - Performance
- 🎨 Plastic Man - Responsive
- 🔬 The Atom - Component validation

**Security & Integration**:
- 🌊 Aquaman - Network analysis
- 🤖 Cyborg - API integrations
- 🧠 Martian Manhunter - Security scanning

**Optimization**:
- 🎩 Zatanna - SEO optimization
- 🪔 Litty - Ethical design
- ⚡ Flash - Performance tuning

---

## 🔄 Auto-Update Protocol

**This file is automatically updated by Oracle Meta Agent when:**
- New heroes are added to the Justice League
- Hero capabilities are enhanced
- New methodologies are implemented
- Best practices are updated
- Integration patterns change

**Update Trigger**: Oracle's `update_hero_documentation()` method
**Frequency**: After significant system changes
**Validation**: Auto-verified against actual hero implementations

**Last Auto-Update**: 2025-10-30 (Initial creation)
**Next Scheduled Update**: On next hero addition or capability enhancement

---

## 📚 Quick Reference

### Hero Capabilities Summary

| Hero | Primary Role | Narrator | MCP Required | Best For |
|------|-------------|----------|--------------|----------|
| Superman | Coordination | ✅ | No | Mission orchestration |
| Oracle | Learning | ✅ | No | Pattern management |
| Artemis | Code Gen | ✅ | No | Figma-to-Code |
| Green Arrow | Validation | ✅ | No | Visual accuracy |
| Hawkman | Parsing | ✅ | No | Frame export |
| Vision Analyst | Analysis | ✅ | No | Image-to-HTML |
| Batman | Testing | ✅ | Yes | Interaction testing |
| Green Lantern | Regression | ✅ | No | Visual consistency |
| Wonder Woman | A11y | ✅ | Yes | Accessibility |
| Flash | Performance | ✅ | Yes | Speed optimization |
| Plastic Man | Responsive | ✅ | Yes | Multi-device |
| Aquaman | Network | ✅ | Yes | Network analysis |
| Cyborg | Integration | ✅ | No | API connections |
| Martian Manhunter | Security | ✅ | No | Vulnerability scan |
| The Atom | Components | ✅ | No | Design systems |
| Zatanna | SEO | ✅ | Yes | Search optimization |
| Litty | Ethics | ✅ | No | Ethical design |
| Hephaestus | Builder | ❌ | No | File generation |

### Narrator Integration Status
- **Total Heroes**: 18
- **With Narrator**: 16 (88.9%)
- **Unified Instance**: Yes (all share Superman's narrator)
- **Coordinator**: Superman creates and distributes

### MCP Integration Requirements
- **Heroes Requiring MCP**: 6 (Batman, Wonder Woman, Flash, Plastic Man, Aquaman, Zatanna)
- **MCP Type**: Chrome DevTools MCP
- **Purpose**: Browser automation and performance profiling

---

**End of Justice League Heroes Reference**
**Auto-managed by**: 🔮 Oracle Meta Agent
**Version**: 1.9.3
