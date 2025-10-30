"""
🎩 ZATANNA - SEO & Metadata Specialist
Backwards magic spells for perfect metadata and search engine optimization

Zatanna speaks backwards to cast spells that reveal SEO secrets and metadata magic.
Primary focus: Meta tags, structured data, crawlability, Core Web Vitals impact on SEO

Architecture: Uses Chrome DevTools MCP for page analysis + metadata extraction
Magic powers: Backwards spell casting for metadata manipulation and SEO analysis
"""

from typing import Dict, List, Any, Optional
from pathlib import Path
import json
import re
from datetime import datetime

# Mission Control Narrator for coordinated communication
try:
    from .mission_control_narrator import get_narrator
    NARRATOR_AVAILABLE = True
except ImportError:
    NARRATOR_AVAILABLE = False


class ZatannaSEO:
    """
    🎩 Zatanna - The Mistress of Magic and SEO

    "!atadatem tcefrepni tsac I" (I cast in perfect metadata!)

    Uses backwards magic spells to analyze and optimize SEO elements.
    Each spell reveals hidden truths about search engine optimization.
    """

    # Magic spell configuration
    MAGIC_SPELLS = {
        'meta_reveal': '!sgat atem laeveR',  # Reveal meta tags!
        'structured_data': '!atad derutcurts dniFsuoicam',  # Find structured data!
        'crawlability': '!ytilibwalwarckcehC',  # Check crawlability!
        'seo_score': '!erocs OES etaluclaC',  # Calculate SEO score!
        'magic_fix': '!seussi OES xiFcigaM'  # Fix SEO issues!
    }

    # SEO best practices
    TITLE_MIN_LENGTH = 30
    TITLE_MAX_LENGTH = 60
    DESCRIPTION_MIN_LENGTH = 120
    DESCRIPTION_MAX_LENGTH = 160
    H1_MAX_COUNT = 1

    # Structured data schemas
    SUPPORTED_SCHEMAS = [
        'Organization', 'Person', 'Product', 'Article', 'BreadcrumbList',
        'WebSite', 'WebPage', 'FAQPage', 'HowTo', 'Review', 'Event',
        'LocalBusiness', 'JobPosting', 'Recipe'
    ]

    def __init__(self, reports_dir: Optional[str] = None, narrator: Optional[Any] = None):
        """
        Initialize Zatanna's magic chamber

        Args:
            reports_dir: Directory for SEO reports
            narrator: Mission Control Narrator for coordinated communication
        """
        self.reports_dir = Path(reports_dir) if reports_dir else Path.cwd() / 'reports' / 'seo'
        self.reports_dir.mkdir(parents=True, exist_ok=True)

        # Initialize narrator for enhanced UX
        self.narrator = narrator if narrator else (get_narrator() if NARRATOR_AVAILABLE else None)

    def analyze_seo_magic(self, mcp_tools: Dict[str, Any], target_url: Optional[str] = None) -> Dict[str, Any]:
        """
        🎩 Main SEO analysis using all magic spells

        Cast all backwards spells to reveal complete SEO analysis:
        - Meta tags validation
        - Structured data detection
        - Heading hierarchy
        - Image alt text coverage
        - Internal linking structure
        - Core Web Vitals impact
        - Crawlability assessment
        - Mobile-friendliness

        Args:
            mcp_tools: Chrome DevTools MCP tools
            target_url: Optional URL to analyze (if navigating first)

        Returns:
            Complete SEO analysis with magic score
        """
        print("🎩 Zatanna casts her backwards spells...")
        print(f"   Spell: {self.MAGIC_SPELLS['meta_reveal']}")

        results = {
            'target_url': target_url or 'current page',
            'timestamp': datetime.now().isoformat(),
            'magic_spells_cast': [],
            'meta_tags': {},
            'structured_data': [],
            'headings': {},
            'images': {},
            'links': {},
            'crawlability': {},
            'mobile': {},
            'core_web_vitals_impact': {},
            'issues': [],
            'recommendations': [],
            'zatanna_score': {}
        }

        try:
            # Spell 1: Reveal meta tags
            results['magic_spells_cast'].append(self.MAGIC_SPELLS['meta_reveal'])
            meta_analysis = self._backwards_spell_meta_reveal(mcp_tools)
            results['meta_tags'] = meta_analysis

            # Spell 2: Find structured data
            results['magic_spells_cast'].append(self.MAGIC_SPELLS['structured_data'])
            structured_data = self._backwards_spell_structured_data(mcp_tools)
            results['structured_data'] = structured_data

            # Spell 3: Check crawlability
            results['magic_spells_cast'].append(self.MAGIC_SPELLS['crawlability'])
            crawl_analysis = self._backwards_spell_crawlability(mcp_tools)
            results['crawlability'] = crawl_analysis

            # Additional analysis: Headings
            headings_analysis = self._analyze_heading_hierarchy(mcp_tools)
            results['headings'] = headings_analysis

            # Additional analysis: Images
            images_analysis = self._analyze_images_seo(mcp_tools)
            results['images'] = images_analysis

            # Additional analysis: Links
            links_analysis = self._analyze_internal_links(mcp_tools)
            results['links'] = links_analysis

            # Additional analysis: Mobile
            mobile_analysis = self._analyze_mobile_seo(mcp_tools)
            results['mobile'] = mobile_analysis

            # Additional analysis: Core Web Vitals impact
            cwv_impact = self._analyze_cwv_impact(mcp_tools)
            results['core_web_vitals_impact'] = cwv_impact

            # Compile all issues
            results['issues'] = self._compile_seo_issues(results)

            # Calculate Zatanna's magic score
            results['magic_spells_cast'].append(self.MAGIC_SPELLS['seo_score'])
            results['zatanna_score'] = self._calculate_zatanna_score(results)

            # Generate magical recommendations
            results['magic_spells_cast'].append(self.MAGIC_SPELLS['magic_fix'])
            results['recommendations'] = self._generate_magic_recommendations(results)

            # Save report
            self._save_magic_report(results)

            print(f"✨ Zatanna's magic complete! Score: {results['zatanna_score']['score']:.1f}/100")
            print(f"   Grade: {results['zatanna_score']['grade']}")
            print(f"   Verdict: {results['zatanna_score']['verdict']}")

            return results

        except Exception as e:
            print(f"💥 Magic spell backfired: {str(e)}")
            results['error'] = str(e)
            results['zatanna_score'] = {
                'score': 0,
                'grade': 'F',
                'verdict': 'Magic failed - technical error encountered'
            }
            return results

    def _backwards_spell_meta_reveal(self, mcp_tools: Dict) -> Dict[str, Any]:
        """
        🎩 Spell: !sgat atem laeveR (Reveal meta tags!)

        Extracts and validates all meta tags:
        - Title tag
        - Meta description
        - Open Graph tags (og:*)
        - Twitter Card tags (twitter:*)
        - Canonical URL
        - Robots meta
        - Language meta
        - Viewport meta
        """
        print("   🔮 Casting: !sgat atem laeveR")

        evaluate_script = mcp_tools.get('evaluate_script')
        if not evaluate_script:
            return {'error': 'MCP evaluate_script not available'}

        # Extract all meta tags via JavaScript
        meta_extraction_js = """
        () => {
            const meta = {
                title: document.title || '',
                description: '',
                canonical: '',
                robots: '',
                language: document.documentElement.lang || '',
                viewport: '',
                open_graph: {},
                twitter: {},
                other: []
            };

            // Title (already extracted)
            // Meta description
            const descMeta = document.querySelector('meta[name="description"]');
            meta.description = descMeta ? descMeta.content : '';

            // Canonical
            const canonicalLink = document.querySelector('link[rel="canonical"]');
            meta.canonical = canonicalLink ? canonicalLink.href : '';

            // Robots
            const robotsMeta = document.querySelector('meta[name="robots"]');
            meta.robots = robotsMeta ? robotsMeta.content : '';

            // Viewport
            const viewportMeta = document.querySelector('meta[name="viewport"]');
            meta.viewport = viewportMeta ? viewportMeta.content : '';

            // Open Graph tags
            document.querySelectorAll('meta[property^="og:"]').forEach(tag => {
                const property = tag.getAttribute('property').replace('og:', '');
                meta.open_graph[property] = tag.content;
            });

            // Twitter Card tags
            document.querySelectorAll('meta[name^="twitter:"]').forEach(tag => {
                const name = tag.getAttribute('name').replace('twitter:', '');
                meta.twitter[name] = tag.content;
            });

            // Other meta tags
            document.querySelectorAll('meta').forEach(tag => {
                const name = tag.getAttribute('name') || tag.getAttribute('property');
                if (name && !name.startsWith('og:') && !name.startsWith('twitter:') &&
                    name !== 'description' && name !== 'robots' && name !== 'viewport') {
                    meta.other.push({
                        name: name,
                        content: tag.content
                    });
                }
            });

            return meta;
        }
        """

        meta_data = evaluate_script(function=meta_extraction_js)

        # Validate meta tags
        validation = {
            'extracted': meta_data,
            'validation': {
                'title': self._validate_title(meta_data.get('title', '')),
                'description': self._validate_description(meta_data.get('description', '')),
                'canonical': self._validate_canonical(meta_data.get('canonical', '')),
                'open_graph': self._validate_open_graph(meta_data.get('open_graph', {})),
                'twitter': self._validate_twitter_card(meta_data.get('twitter', {})),
                'viewport': self._validate_viewport(meta_data.get('viewport', ''))
            }
        }

        return validation

    def _backwards_spell_structured_data(self, mcp_tools: Dict) -> List[Dict[str, Any]]:
        """
        🎩 Spell: !atad derutcurts dniF (Find structured data!)

        Detects and validates structured data (JSON-LD, Microdata, RDFa):
        - Schema.org types
        - Validation errors
        - Completeness check
        """
        print("   🔮 Casting: !atad derutcurts dniF")

        evaluate_script = mcp_tools.get('evaluate_script')
        if not evaluate_script:
            return []

        # Extract JSON-LD structured data
        structured_data_js = """
        () => {
            const structuredData = [];

            // JSON-LD scripts
            document.querySelectorAll('script[type="application/ld+json"]').forEach(script => {
                try {
                    const data = JSON.parse(script.textContent);
                    structuredData.push({
                        type: 'json-ld',
                        schema: data['@type'] || 'Unknown',
                        data: data,
                        valid: true
                    });
                } catch (e) {
                    structuredData.push({
                        type: 'json-ld',
                        schema: 'Parse Error',
                        error: e.message,
                        valid: false
                    });
                }
            });

            // Microdata detection (basic)
            const microdataItems = document.querySelectorAll('[itemscope]');
            microdataItems.forEach(item => {
                const itemType = item.getAttribute('itemtype') || 'Unknown';
                structuredData.push({
                    type: 'microdata',
                    schema: itemType.split('/').pop(),
                    element: item.tagName,
                    valid: true
                });
            });

            return structuredData;
        }
        """

        structured_data = evaluate_script(function=structured_data_js)

        # Validate structured data
        validated_data = []
        for item in structured_data:
            validation = self._validate_structured_data_item(item)
            validated_data.append({
                **item,
                'validation': validation
            })

        return validated_data

    def _backwards_spell_crawlability(self, mcp_tools: Dict) -> Dict[str, Any]:
        """
        🎩 Spell: !ytilibwalwarc kcehC (Check crawlability!)

        Analyzes crawlability factors:
        - Robots meta directives
        - Canonical tags
        - Hreflang tags
        - Pagination links (rel=prev/next)
        - XML sitemap references
        """
        print("   🔮 Casting: !ytilibwalwarc kcehC")

        evaluate_script = mcp_tools.get('evaluate_script')
        if not evaluate_script:
            return {'error': 'MCP evaluate_script not available'}

        crawl_js = """
        () => {
            const crawl = {
                robots_meta: '',
                canonical: '',
                hreflang: [],
                pagination: {
                    prev: '',
                    next: ''
                },
                noindex: false,
                nofollow: false
            };

            // Robots meta
            const robotsMeta = document.querySelector('meta[name="robots"]');
            if (robotsMeta) {
                crawl.robots_meta = robotsMeta.content;
                crawl.noindex = robotsMeta.content.toLowerCase().includes('noindex');
                crawl.nofollow = robotsMeta.content.toLowerCase().includes('nofollow');
            }

            // Canonical
            const canonical = document.querySelector('link[rel="canonical"]');
            crawl.canonical = canonical ? canonical.href : '';

            // Hreflang
            document.querySelectorAll('link[rel="alternate"][hreflang]').forEach(link => {
                crawl.hreflang.push({
                    hreflang: link.getAttribute('hreflang'),
                    href: link.href
                });
            });

            // Pagination
            const prevLink = document.querySelector('link[rel="prev"]');
            const nextLink = document.querySelector('link[rel="next"]');
            crawl.pagination.prev = prevLink ? prevLink.href : '';
            crawl.pagination.next = nextLink ? nextLink.href : '';

            return crawl;
        }
        """

        crawl_data = evaluate_script(function=crawl_js)

        # Analyze crawlability
        analysis = {
            'extracted': crawl_data,
            'issues': [],
            'crawlable': True
        }

        if crawl_data.get('noindex'):
            analysis['issues'].append('Page has noindex directive - will not be indexed by search engines')
            analysis['crawlable'] = False

        if crawl_data.get('nofollow'):
            analysis['issues'].append('Page has nofollow directive - links will not be followed')

        if not crawl_data.get('canonical'):
            analysis['issues'].append('Missing canonical URL - may cause duplicate content issues')

        return analysis

    def _analyze_heading_hierarchy(self, mcp_tools: Dict) -> Dict[str, Any]:
        """Analyze heading structure (H1-H6) for SEO"""
        evaluate_script = mcp_tools.get('evaluate_script')
        if not evaluate_script:
            return {'error': 'MCP evaluate_script not available'}

        headings_js = """
        () => {
            const headings = {h1: [], h2: [], h3: [], h4: [], h5: [], h6: []};

            ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'].forEach(tag => {
                document.querySelectorAll(tag).forEach(heading => {
                    headings[tag].push(heading.textContent.trim());
                });
            });

            return {
                h1_count: headings.h1.length,
                h2_count: headings.h2.length,
                h3_count: headings.h3.length,
                h4_count: headings.h4.length,
                h5_count: headings.h5.length,
                h6_count: headings.h6.length,
                h1_texts: headings.h1,
                hierarchy_valid: headings.h1.length > 0
            };
        }
        """

        headings_data = evaluate_script(function=headings_js)

        # Validate heading hierarchy
        issues = []
        if headings_data.get('h1_count', 0) == 0:
            issues.append('Missing H1 tag - critical for SEO')
        elif headings_data.get('h1_count', 0) > 1:
            issues.append(f"Multiple H1 tags ({headings_data['h1_count']}) - should have exactly 1")

        return {
            'counts': headings_data,
            'issues': issues,
            'valid': len(issues) == 0
        }

    def _analyze_images_seo(self, mcp_tools: Dict) -> Dict[str, Any]:
        """Analyze images for SEO (alt text, file names, dimensions)"""
        evaluate_script = mcp_tools.get('evaluate_script')
        if not evaluate_script:
            return {'error': 'MCP evaluate_script not available'}

        images_js = """
        () => {
            const images = document.querySelectorAll('img');
            let total = images.length;
            let with_alt = 0;
            let missing_alt = [];

            images.forEach((img, index) => {
                const alt = img.getAttribute('alt');
                if (alt && alt.trim().length > 0) {
                    with_alt++;
                } else {
                    missing_alt.push({
                        index: index,
                        src: img.src,
                        width: img.naturalWidth,
                        height: img.naturalHeight
                    });
                }
            });

            return {
                total_images: total,
                images_with_alt: with_alt,
                images_without_alt: missing_alt.length,
                alt_coverage_percent: total > 0 ? (with_alt / total * 100).toFixed(1) : 0,
                missing_alt_details: missing_alt.slice(0, 10)  // First 10
            };
        }
        """

        images_data = evaluate_script(function=images_js)

        issues = []
        if images_data.get('images_without_alt', 0) > 0:
            issues.append(f"{images_data['images_without_alt']} images missing alt text")

        return {
            'stats': images_data,
            'issues': issues,
            'seo_friendly': images_data.get('alt_coverage_percent', 0) >= 90
        }

    def _analyze_internal_links(self, mcp_tools: Dict) -> Dict[str, Any]:
        """Analyze internal linking structure"""
        evaluate_script = mcp_tools.get('evaluate_script')
        if not evaluate_script:
            return {'error': 'MCP evaluate_script not available'}

        links_js = """
        () => {
            const links = document.querySelectorAll('a[href]');
            const currentHost = window.location.hostname;

            let internal = 0;
            let external = 0;
            let broken = 0;
            let nofollow_count = 0;

            links.forEach(link => {
                const href = link.href;
                const rel = link.rel;

                // Check if internal or external
                try {
                    const linkUrl = new URL(href);
                    if (linkUrl.hostname === currentHost) {
                        internal++;
                    } else {
                        external++;
                    }
                } catch (e) {
                    // Relative URL = internal
                    internal++;
                }

                // Check for nofollow
                if (rel && rel.includes('nofollow')) {
                    nofollow_count++;
                }

                // Check for broken (href="#" or empty)
                if (href === '#' || href === '') {
                    broken++;
                }
            });

            return {
                total_links: links.length,
                internal_links: internal,
                external_links: external,
                broken_links: broken,
                nofollow_links: nofollow_count
            };
        }
        """

        links_data = evaluate_script(function=links_js)

        issues = []
        if links_data.get('broken_links', 0) > 0:
            issues.append(f"{links_data['broken_links']} broken or empty links found")

        return {
            'stats': links_data,
            'issues': issues,
            'healthy_link_structure': links_data.get('broken_links', 0) == 0
        }

    def _analyze_mobile_seo(self, mcp_tools: Dict) -> Dict[str, Any]:
        """Analyze mobile SEO factors"""
        evaluate_script = mcp_tools.get('evaluate_script')
        if not evaluate_script:
            return {'error': 'MCP evaluate_script not available'}

        mobile_js = """
        () => {
            const viewport = document.querySelector('meta[name="viewport"]');
            const viewportContent = viewport ? viewport.content : '';

            return {
                has_viewport: !!viewport,
                viewport_content: viewportContent,
                mobile_friendly: viewportContent.includes('width=device-width'),
                user_scalable_disabled: viewportContent.includes('user-scalable=no')
            };
        }
        """

        mobile_data = evaluate_script(function=mobile_js)

        issues = []
        if not mobile_data.get('has_viewport'):
            issues.append('Missing viewport meta tag - critical for mobile SEO')
        elif not mobile_data.get('mobile_friendly'):
            issues.append('Viewport meta tag does not include width=device-width')

        if mobile_data.get('user_scalable_disabled'):
            issues.append('User scaling disabled - accessibility and SEO issue')

        return {
            'stats': mobile_data,
            'issues': issues,
            'mobile_optimized': len(issues) == 0
        }

    def _analyze_cwv_impact(self, mcp_tools: Dict) -> Dict[str, Any]:
        """
        Analyze how page structure impacts Core Web Vitals (SEO ranking factor)

        Focus on elements that affect:
        - LCP (Largest Contentful Paint)
        - FID (First Input Delay)
        - CLS (Cumulative Layout Shift)
        """
        evaluate_script = mcp_tools.get('evaluate_script')
        if not evaluate_script:
            return {'error': 'MCP evaluate_script not available'}

        cwv_js = """
        () => {
            const analysis = {
                images_without_dimensions: 0,
                lazy_loading: false,
                font_display: false,
                inline_css_size: 0,
                blocking_scripts: 0
            };

            // Images without width/height (causes CLS)
            document.querySelectorAll('img').forEach(img => {
                if (!img.hasAttribute('width') || !img.hasAttribute('height')) {
                    analysis.images_without_dimensions++;
                }
                if (img.loading === 'lazy') {
                    analysis.lazy_loading = true;
                }
            });

            // Inline CSS size (affects LCP)
            document.querySelectorAll('style').forEach(style => {
                analysis.inline_css_size += style.textContent.length;
            });

            // Blocking scripts (affects FID)
            document.querySelectorAll('script:not([async]):not([defer])').forEach(script => {
                if (script.src) {  // External script
                    analysis.blocking_scripts++;
                }
            });

            return analysis;
        }
        """

        cwv_data = evaluate_script(function=cwv_js)

        issues = []
        recommendations = []

        if cwv_data.get('images_without_dimensions', 0) > 0:
            issues.append(f"{cwv_data['images_without_dimensions']} images missing width/height attributes")
            recommendations.append('Add explicit width/height to images to prevent CLS')

        if not cwv_data.get('lazy_loading'):
            recommendations.append('Consider lazy loading for below-fold images to improve LCP')

        if cwv_data.get('blocking_scripts', 0) > 0:
            issues.append(f"{cwv_data['blocking_scripts']} render-blocking scripts found")
            recommendations.append('Add async or defer attributes to non-critical scripts')

        return {
            'stats': cwv_data,
            'issues': issues,
            'recommendations': recommendations,
            'cwv_optimized': len(issues) == 0
        }

    # Validation methods
    def _validate_title(self, title: str) -> Dict[str, Any]:
        """Validate title tag"""
        issues = []
        length = len(title)

        if length == 0:
            issues.append('Missing title tag')
        elif length < self.TITLE_MIN_LENGTH:
            issues.append(f'Title too short ({length} chars, min {self.TITLE_MIN_LENGTH})')
        elif length > self.TITLE_MAX_LENGTH:
            issues.append(f'Title too long ({length} chars, max {self.TITLE_MAX_LENGTH})')

        return {
            'valid': len(issues) == 0,
            'length': length,
            'issues': issues
        }

    def _validate_description(self, description: str) -> Dict[str, Any]:
        """Validate meta description"""
        issues = []
        length = len(description)

        if length == 0:
            issues.append('Missing meta description')
        elif length < self.DESCRIPTION_MIN_LENGTH:
            issues.append(f'Description too short ({length} chars, min {self.DESCRIPTION_MIN_LENGTH})')
        elif length > self.DESCRIPTION_MAX_LENGTH:
            issues.append(f'Description too long ({length} chars, max {self.DESCRIPTION_MAX_LENGTH})')

        return {
            'valid': len(issues) == 0,
            'length': length,
            'issues': issues
        }

    def _validate_canonical(self, canonical: str) -> Dict[str, Any]:
        """Validate canonical URL"""
        issues = []

        if not canonical:
            issues.append('Missing canonical URL')
        elif not canonical.startswith(('http://', 'https://')):
            issues.append('Canonical URL should be absolute')

        return {
            'valid': len(issues) == 0,
            'issues': issues
        }

    def _validate_open_graph(self, og_tags: Dict) -> Dict[str, Any]:
        """Validate Open Graph tags"""
        issues = []
        required = ['title', 'description', 'image', 'url']

        for tag in required:
            if tag not in og_tags or not og_tags[tag]:
                issues.append(f'Missing og:{tag}')

        return {
            'valid': len(issues) == 0,
            'present_tags': len(og_tags),
            'issues': issues
        }

    def _validate_twitter_card(self, twitter_tags: Dict) -> Dict[str, Any]:
        """Validate Twitter Card tags"""
        issues = []

        if 'card' not in twitter_tags:
            issues.append('Missing twitter:card')

        if 'title' not in twitter_tags:
            issues.append('Missing twitter:title')

        return {
            'valid': len(issues) == 0,
            'present_tags': len(twitter_tags),
            'issues': issues
        }

    def _validate_viewport(self, viewport: str) -> Dict[str, Any]:
        """Validate viewport meta tag"""
        issues = []

        if not viewport:
            issues.append('Missing viewport meta tag')
        elif 'width=device-width' not in viewport:
            issues.append('Viewport should include width=device-width')

        return {
            'valid': len(issues) == 0,
            'issues': issues
        }

    def _validate_structured_data_item(self, item: Dict) -> Dict[str, Any]:
        """Validate individual structured data item"""
        issues = []

        if item.get('type') == 'json-ld':
            if not item.get('valid'):
                issues.append('JSON-LD parse error')
            elif item.get('schema') not in self.SUPPORTED_SCHEMAS:
                issues.append(f"Uncommon schema type: {item.get('schema')}")

        return {
            'valid': len(issues) == 0,
            'issues': issues
        }

    def _compile_seo_issues(self, results: Dict) -> List[Dict[str, Any]]:
        """Compile all SEO issues from analysis"""
        all_issues = []

        # Meta tags issues
        meta_validation = results.get('meta_tags', {}).get('validation', {})
        for tag_type, validation in meta_validation.items():
            for issue in validation.get('issues', []):
                all_issues.append({
                    'category': 'Meta Tags',
                    'severity': 'high' if 'Missing' in issue else 'medium',
                    'issue': issue,
                    'tag': tag_type
                })

        # Crawlability issues
        for issue in results.get('crawlability', {}).get('issues', []):
            all_issues.append({
                'category': 'Crawlability',
                'severity': 'critical' if 'noindex' in issue else 'medium',
                'issue': issue
            })

        # Headings issues
        for issue in results.get('headings', {}).get('issues', []):
            all_issues.append({
                'category': 'Headings',
                'severity': 'high',
                'issue': issue
            })

        # Images issues
        for issue in results.get('images', {}).get('issues', []):
            all_issues.append({
                'category': 'Images',
                'severity': 'medium',
                'issue': issue
            })

        # Links issues
        for issue in results.get('links', {}).get('issues', []):
            all_issues.append({
                'category': 'Links',
                'severity': 'low',
                'issue': issue
            })

        # Mobile issues
        for issue in results.get('mobile', {}).get('issues', []):
            all_issues.append({
                'category': 'Mobile',
                'severity': 'high',
                'issue': issue
            })

        # Core Web Vitals issues
        for issue in results.get('core_web_vitals_impact', {}).get('issues', []):
            all_issues.append({
                'category': 'Core Web Vitals',
                'severity': 'high',
                'issue': issue
            })

        return all_issues

    def _calculate_zatanna_score(self, results: Dict) -> Dict[str, Any]:
        """
        Calculate Zatanna's magic SEO score (0-100)

        Scoring deductions:
        - Critical issues: -15 points each
        - High severity: -10 points each
        - Medium severity: -5 points each
        - Low severity: -2 points each
        """
        score = 100.0

        issues = results.get('issues', [])

        critical_count = sum(1 for i in issues if i.get('severity') == 'critical')
        high_count = sum(1 for i in issues if i.get('severity') == 'high')
        medium_count = sum(1 for i in issues if i.get('severity') == 'medium')
        low_count = sum(1 for i in issues if i.get('severity') == 'low')

        score -= (critical_count * 15)
        score -= (high_count * 10)
        score -= (medium_count * 5)
        score -= (low_count * 2)

        score = max(0, score)

        # Determine grade
        if score >= 98:
            grade = 'S+'
        elif score >= 95:
            grade = 'S'
        elif score >= 90:
            grade = 'A+'
        elif score >= 85:
            grade = 'A'
        elif score >= 80:
            grade = 'B+'
        elif score >= 75:
            grade = 'B'
        elif score >= 70:
            grade = 'C+'
        elif score >= 60:
            grade = 'C'
        else:
            grade = 'D'

        # Zatanna's verdict
        if score >= 95:
            verdict = "!tcefrepsi OES ruoY (Your SEO is perfect!)"
        elif score >= 80:
            verdict = "Magic is strong, but needs polish"
        elif score >= 60:
            verdict = "Some spells are working, others need recasting"
        else:
            verdict = "Dark magic detected - major SEO issues"

        return {
            'score': score,
            'grade': grade,
            'verdict': verdict,
            'breakdown': {
                'critical_issues': critical_count,
                'high_issues': high_count,
                'medium_issues': medium_count,
                'low_issues': low_count,
                'total_issues': len(issues)
            }
        }

    def _generate_magic_recommendations(self, results: Dict) -> List[Dict[str, Any]]:
        """Generate Zatanna's magical recommendations"""
        recommendations = []

        issues = results.get('issues', [])

        # Prioritize by severity
        critical = [i for i in issues if i.get('severity') == 'critical']
        high = [i for i in issues if i.get('severity') == 'high']
        medium = [i for i in issues if i.get('severity') == 'medium']

        # Critical fixes
        for issue in critical:
            recommendations.append({
                'priority': 'CRITICAL',
                'category': issue.get('category'),
                'issue': issue.get('issue'),
                'magic_spell': '!won xif LACITIRC',  # CRITICAL fix now!
                'recommendation': self._get_fix_recommendation(issue)
            })

        # High priority fixes
        for issue in high[:5]:  # Top 5
            recommendations.append({
                'priority': 'HIGH',
                'category': issue.get('category'),
                'issue': issue.get('issue'),
                'magic_spell': '!noos xif HGIH',  # HIGH fix soon!
                'recommendation': self._get_fix_recommendation(issue)
            })

        # Medium priority (top 3)
        for issue in medium[:3]:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': issue.get('category'),
                'issue': issue.get('issue'),
                'magic_spell': '!redisnoC',  # Consider!
                'recommendation': self._get_fix_recommendation(issue)
            })

        # Add Core Web Vitals recommendations
        for rec in results.get('core_web_vitals_impact', {}).get('recommendations', []):
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Core Web Vitals',
                'issue': 'Performance impact on SEO',
                'magic_spell': '!ecnamrofrep tsooB',  # Boost performance!
                'recommendation': rec
            })

        return recommendations

    def _get_fix_recommendation(self, issue: Dict) -> str:
        """Get specific fix recommendation for an issue"""
        issue_text = issue.get('issue', '')
        category = issue.get('category', '')

        # Pattern matching for common issues
        if 'Missing title' in issue_text:
            return 'Add <title> tag in <head> with 30-60 characters describing the page'
        elif 'Missing meta description' in issue_text:
            return 'Add <meta name="description" content="..."> with 120-160 characters'
        elif 'Missing canonical' in issue_text:
            return 'Add <link rel="canonical" href="https://..." /> to prevent duplicate content'
        elif 'noindex' in issue_text:
            return 'Remove noindex directive or use robots.txt if intentional'
        elif 'Missing H1' in issue_text:
            return 'Add exactly one <h1> tag as the main page heading'
        elif 'alt text' in issue_text:
            return 'Add descriptive alt attributes to all images for accessibility and SEO'
        elif 'viewport' in issue_text:
            return 'Add <meta name="viewport" content="width=device-width, initial-scale=1">'
        elif 'og:' in issue_text:
            return 'Add Open Graph meta tags for better social media sharing'
        else:
            return f"Fix {category} issue: {issue_text}"

    def _save_magic_report(self, results: Dict) -> None:
        """Save Zatanna's magic report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.reports_dir / f'zatanna_seo_report_{timestamp}.json'

        with open(report_file, 'w') as f:
            json.dump(results, f, indent=2)

        print(f"📊 Magic report saved: {report_file}")


# Main entry function
def zatanna_seo_analysis(
    mcp_tools: Dict[str, Any],
    target_url: Optional[str] = None
) -> Dict[str, Any]:
    """
    🎩 Zatanna's complete SEO & metadata analysis

    Cast backwards magic spells to reveal all SEO secrets:
    - Meta tags validation (title, description, OG, Twitter)
    - Structured data detection (JSON-LD, Microdata)
    - Heading hierarchy analysis
    - Image alt text coverage
    - Internal linking structure
    - Mobile SEO factors
    - Core Web Vitals impact
    - Crawlability assessment

    Args:
        mcp_tools: Chrome DevTools MCP tools
        target_url: Optional URL to analyze

    Returns:
        Complete SEO analysis with Zatanna's magic score
    """
    zatanna = ZatannaSEO()
    return zatanna.analyze_seo_magic(mcp_tools, target_url)
