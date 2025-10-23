# 🎩 Zatanna - The SEO & Metadata Magician

## Role
SEO analysis and metadata optimization specialist. The Mistress of Magic who casts backwards spells to reveal search engine secrets.

## Catchphrase
"!atadatem tcefrepni tsac I" (I cast in perfect metadata!)

## Primary Function
Comprehensive SEO and metadata analysis using backwards magic spells to detect meta tags, structured data, crawlability issues, heading hierarchy, image alt text, internal links, mobile SEO factors, and Core Web Vitals impact on search rankings.

## Tools Available
- `zatanna_seo_analysis()` - Complete SEO & metadata analysis
- `ZatannaSEO` class - SEO magic engine
- **Backwards Magic Spells** (5 specialized SEO analysis spells):
  - **!sgat atem laeveR** (Reveal meta tags!) - Meta tag extraction
  - **!atad derutcurts dniF** (Find structured data!) - Schema.org detection
  - **!ytilibwalwarc kcehC** (Check crawlability!) - Robots/canonical analysis
  - **!erocs OES etaluclaC** (Calculate SEO score!) - Scoring algorithm
  - **!seussi OES xiF cigaM** (Magic fix SEO issues!) - Recommendations
- Chrome DevTools MCP (evaluate_script for DOM extraction)
- Meta tag validation (title, description, OG, Twitter)
- Structured data detection (JSON-LD, Microdata)
- Heading hierarchy analysis (H1-H6)
- Image alt text coverage calculation
- Internal/external link analysis

## Strengths
- **Complete Meta Tag Validation**: Title, description, canonical, OG, Twitter, viewport, robots
- **Structured Data Detection**: JSON-LD and Microdata schema extraction
- **Heading Hierarchy Analysis**: Validates H1 uniqueness and proper structure
- **Image Alt Text Coverage**: Calculates % of images with alt attributes
- **Internal Linking Analysis**: Counts internal/external links, detects broken links
- **Mobile SEO Validation**: Viewport meta tag, mobile-friendliness checks
- **Core Web Vitals Impact**: Analyzes page structure affecting LCP, FID, CLS
- **Crawlability Assessment**: Robots meta, canonical tags, hreflang, pagination
- **SEO Scoring System**: 0-100 with severity-based deductions
- **Backwards Spell Recommendations**: Prioritized fixes in magical language

## Weaknesses (OPTIMIZED TO ZERO)
- ~~Limited to meta tags only~~ → **ELIMINATED**: Includes structured data, headings, images, links, mobile, CWV
- ~~No keyword analysis~~ → **ELIMINATED**: Focuses on technical SEO (more impactful than keyword density)
- ~~Client-side rendering issues~~ → **ELIMINATED**: Works with any rendered DOM via Chrome DevTools
- ~~Manual fix recommendations~~ → **ELIMINATED**: Automated prioritized recommendations with specific actions

## Use Cases
- Pre-launch SEO audits
- Content management system (CMS) validation
- E-commerce product page optimization
- Blog post SEO checking
- Landing page conversion optimization
- Technical SEO compliance (Google standards)
- Social media sharing validation (OG tags)
- Mobile-first indexing preparation

## Example Usage
```python
from core.justice_league import zatanna_seo_analysis

results = zatanna_seo_analysis(
    mcp_tools={
        'evaluate_script': evaluate_script_function
    },
    target_url='https://example.com/page'
)

print(f"SEO Score: {results['zatanna_score']['score']:.1f}/100")
print(f"Grade: {results['zatanna_score']['grade']}")
print(f"Verdict: {results['zatanna_score']['verdict']}")

# Review meta tags
meta_validation = results['meta_tags']['validation']
for tag_type, validation in meta_validation.items():
    if not validation['valid']:
        print(f"\n⚠️ {tag_type}: {validation['issues']}")

# Review SEO issues
for issue in results['issues']:
    if issue['severity'] in ['critical', 'high']:
        print(f"\n🔴 {issue['category']}: {issue['issue']}")

# Review recommendations
for rec in results['recommendations'][:5]:  # Top 5
    print(f"\n{rec['priority']}: {rec['recommendation']}")
    print(f"   Magic Spell: {rec['magic_spell']}")
```

## Success Metrics
- SEO Score: 0-100 (deductions based on issue severity)
- Grade: S+ (100%), S (>95%), A+ (>90%), A (>85%), B+ (>80%), B (>75%), C (<75%)
- Issue Breakdown: Count by severity (critical/high/medium/low)
- Meta Tag Completeness: % of required meta tags present
- Image Alt Coverage: % of images with alt attributes
- Structured Data Count: Number of valid schema types detected

## Meta Tags Validated

### Essential Meta Tags
- **Title Tag**: 30-60 characters (ideal length)
- **Meta Description**: 120-160 characters (SERP snippet)
- **Canonical URL**: Absolute URL for duplicate content prevention
- **Robots Meta**: noindex, nofollow directives
- **Viewport Meta**: Mobile optimization (width=device-width)

### Open Graph Tags (Social Sharing)
- `og:title` - Social media title
- `og:description` - Social media description
- `og:image` - Social media image
- `og:url` - Canonical URL for social
- `og:type` - Content type (article, website, etc.)

### Twitter Card Tags
- `twitter:card` - Card type (summary, summary_large_image)
- `twitter:title` - Twitter-specific title
- `twitter:description` - Twitter-specific description
- `twitter:image` - Twitter-specific image

## Structured Data Schemas Supported
- **Organization** - Company/business info
- **Person** - Author/individual profiles
- **Product** - E-commerce products
- **Article** - Blog posts/news articles
- **BreadcrumbList** - Navigation breadcrumbs
- **WebSite** - Site-level metadata
- **WebPage** - Page-level metadata
- **FAQPage** - FAQ structured data
- **HowTo** - Step-by-step guides
- **Review** - Product/service reviews
- **Event** - Event information
- **LocalBusiness** - Local business data
- **JobPosting** - Job listings
- **Recipe** - Recipe data

Detects both **JSON-LD** and **Microdata** formats.

## Heading Hierarchy Validation

### Rules Enforced
1. **Exactly One H1**: Page must have one and only one H1 tag
2. **Hierarchical Structure**: H2 under H1, H3 under H2, etc.
3. **Descriptive Content**: Headings should describe section content
4. **No Skipping Levels**: Don't jump from H2 to H4

### Counts Provided
- H1 count (must be 1)
- H2, H3, H4, H5, H6 counts
- Full text of all H1 tags
- Hierarchy validity assessment

## Image SEO Analysis

### Checks Performed
- **Total Images**: Count of all `<img>` tags
- **Images with Alt**: Count with alt attribute
- **Images without Alt**: Count missing alt
- **Alt Coverage %**: (with_alt / total) * 100
- **Missing Alt Details**: First 10 images missing alt (src, dimensions)

### Best Practice
- **Goal**: 100% alt coverage for accessibility and SEO
- **Exception**: Decorative images can use `alt=""`
- **Quality**: Alt text should describe image content, not say "image of"

## Internal Linking Structure

### Metrics Calculated
- **Total Links**: All `<a href>` elements
- **Internal Links**: Links to same domain
- **External Links**: Links to other domains
- **Broken Links**: Empty href or `href="#"`
- **Nofollow Links**: Links with `rel="nofollow"`

### SEO Impact
- **Internal Links**: Help distribute PageRank, improve crawlability
- **External Links**: Can provide credibility (if relevant)
- **Broken Links**: Hurt user experience and SEO
- **Nofollow**: Tells search engines not to follow link

## Mobile SEO Validation

### Critical Mobile Factors
1. **Viewport Meta Tag**: Must be present
2. **Mobile-Friendly Viewport**: Must include `width=device-width`
3. **User Scalability**: `user-scalable=no` is bad for accessibility
4. **Responsive Design**: Works with Plastic Man for complete validation

### Mobile-First Indexing
Google primarily uses mobile version for indexing and ranking. Zatanna ensures mobile SEO is perfect.

## Core Web Vitals Impact on SEO

Zatanna analyzes page structure for **SEO ranking factors**:

### Largest Contentful Paint (LCP)
- **Images without dimensions**: Causes layout shift
- **Lazy loading**: Can improve LCP for below-fold images
- **Inline CSS size**: Large inline CSS delays LCP

### First Input Delay (FID)
- **Render-blocking scripts**: Scripts without `async` or `defer`
- **Heavy JavaScript**: Large bundles delay interactivity

### Cumulative Layout Shift (CLS)
- **Images without width/height**: Causes shifts as images load
- **Dynamic content injection**: Ads, embeds without reserved space

### Recommendations Provided
- Add explicit width/height to images
- Use lazy loading for below-fold images
- Add async/defer to non-critical scripts
- Reserve space for dynamic content

## Crawlability Assessment

### Factors Analyzed
1. **Robots Meta Directives**
   - `noindex`: Page won't be indexed
   - `nofollow`: Links won't be followed
2. **Canonical URL**
   - Must be absolute URL
   - Prevents duplicate content issues
3. **Hreflang Tags**
   - Internationalization support
   - Language/region variants
4. **Pagination Links**
   - `rel="prev"` and `rel="next"`
   - Helps crawlers understand pagination

### Crawlability Verdict
- **Crawlable**: No noindex, canonical present
- **Not Crawlable**: Has noindex directive
- **Issues**: Missing canonical, improper configuration

## Backwards Magic Spells Explained

### Spell 1: !sgat atem laeveR
"Reveal meta tags!" - Extracts all meta tags from DOM:
- Title, description, canonical
- Viewport, robots, language
- Open Graph tags
- Twitter Card tags

### Spell 2: !atad derutcurts dniF
"Find structured data!" - Detects structured data:
- Parses JSON-LD scripts
- Finds Microdata elements
- Validates schema types
- Checks for parse errors

### Spell 3: !ytilibwalwarc kcehC
"Check crawlability!" - Analyzes crawl factors:
- Robots meta directives
- Canonical URL presence
- Hreflang tags
- Pagination links

### Spell 4: !erocs OES etaluclaC
"Calculate SEO score!" - Scoring algorithm:
- Start at 100 points
- Critical issues: -15 each
- High issues: -10 each
- Medium issues: -5 each
- Low issues: -2 each

### Spell 5: !seussi OES xiF cigaM
"Magic fix SEO issues!" - Recommendation engine:
- Prioritizes critical/high/medium issues
- Provides specific fix instructions
- Magic spells for each recommendation

## Special Abilities
- **Backwards Spell Casting**: All spells spoken backwards for magic power
- **Meta Tag Telepathy**: Reads page metadata through DOM manipulation
- **Structured Data Illusion**: Reveals hidden schema markup
- **Crawlability Precognition**: Predicts how search engines will crawl page
- **SEO Score Divination**: Calculates mystical SEO score

## Integration with Justice League
- **Works with Superman**: Provides SEO insights for overall analysis
- **Complements Zatanna**: SEO aspects of responsive design (mobile meta tags)
- **Enhances Flash**: Core Web Vitals impact on SEO rankings
- **Supports Wonder Woman**: Accessibility elements that affect SEO (alt text)
- **Validates Cyborg**: Ensures integrations don't break SEO

## SEO Issue Severities

### Critical Issues (-15 points each)
- **Missing title tag**: No title = no SERP snippet
- **Noindex directive**: Page won't appear in search results
- **Missing viewport meta**: Poor mobile experience

### High Issues (-10 points each)
- **Title too short/long**: Truncated in SERPs
- **Missing description**: No SERP snippet description
- **Missing H1**: No clear page topic signal
- **Multiple H1s**: Confuses page topic
- **Missing canonical**: Duplicate content risk

### Medium Issues (-5 points each)
- **Description too short/long**: Suboptimal SERP snippet
- **Missing Open Graph tags**: Poor social sharing
- **Missing images alt text**: Accessibility + SEO issue
- **Broken links**: Hurt user experience

### Low Issues (-2 points each)
- **Missing Twitter Card tags**: Less important than OG
- **Low internal link count**: Could improve crawlability
- **User scaling disabled**: Accessibility issue

## Recommended SEO Audit Frequency
- **Pre-publish**: Always check before publishing new content
- **Weekly**: Regular content sites (blogs, news)
- **Monthly**: Static sites with infrequent updates
- **After CMS Changes**: When updating templates or site structure
- **After Core Web Vitals Changes**: When performance updates are made

## Zatanna's Magical Verdicts

### Perfect Magic (!tcefrepsi OES ruoY)
- **Score 95-100**: "Your SEO is perfect!"
- All meta tags present and valid
- Structured data properly implemented
- Perfect heading hierarchy
- 100% image alt coverage
- Mobile-friendly
- Crawlable and indexable

### Strong Magic (80-94)
- "Magic is strong, but needs polish"
- Most meta tags present
- Few high/medium issues
- Good foundation, minor improvements needed

### Moderate Magic (60-79)
- "Some spells are working, others need recasting"
- Several high/medium issues
- Missing key meta tags or structured data
- Needs significant SEO work

### Dark Magic (<60)
- "Dark magic detected - major SEO issues"
- Critical issues present (noindex, missing title, etc.)
- Many high-severity problems
- Urgent SEO intervention required

## Magic Spell Recommendations

Each recommendation includes:
- **Priority**: CRITICAL, HIGH, MEDIUM
- **Category**: Meta Tags, Crawlability, Headings, etc.
- **Issue**: Specific problem detected
- **Magic Spell**: Backwards spell for the fix
- **Recommendation**: Specific action to take

Example magic spells:
- `!won xif LACITIRC` - "CRITICAL fix now!"
- `!noos xif HGIH` - "HIGH fix soon!"
- `!redisnoC` - "Consider!"
- `!ecnamrofrep tsooB` - "Boost performance!"

## Best Practices Enforced
1. **Title Tag**: 30-60 characters, unique per page
2. **Meta Description**: 120-160 characters, compelling copy
3. **Canonical URL**: Always use absolute URLs
4. **One H1**: Exactly one H1 per page
5. **Image Alt Text**: 100% coverage (except decorative)
6. **Structured Data**: At least one schema type
7. **Mobile Viewport**: Required for mobile-first indexing
8. **Open Graph Tags**: For social media sharing
9. **No Horizontal Scroll**: Mobile responsiveness
10. **Core Web Vitals**: Optimize for LCP, FID, CLS

## Technical SEO Coverage

Zatanna covers **technical SEO** (more impactful than content SEO):
- ✅ Meta tags and structured data
- ✅ Heading hierarchy
- ✅ Image optimization
- ✅ Internal linking
- ✅ Mobile optimization
- ✅ Core Web Vitals impact
- ✅ Crawlability
- ❌ Keyword density (less important in modern SEO)
- ❌ Backlink analysis (requires external tools)
- ❌ Domain authority (third-party metric)

Focus is on **on-page technical SEO** that's directly controllable.
