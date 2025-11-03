"""
🌊 AQUAMAN - KING OF THE NETWORK SEAS
Justice League Member: Network & Resource Loading Specialist

The King of Atlantis commands all network traffic with hydrokinetic power!

Powers:
- Network request monitoring (all HTTP/HTTPS traffic)
- Resource waterfall analysis
- Critical path detection
- Blocking resource identification
- Request/Response timing analysis
- Cache efficiency analysis
- CDN performance validation
- Third-party resource tracking

"I speak to all network requests - they reveal their secrets to the King of Atlantis!"

MCP Tools Used:
- mcp__chrome-devtools__list_network_requests()
- mcp__chrome-devtools__get_network_request(url)
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict
import re

# Mission Control Narrator for coordinated communication
try:
    from .mission_control_narrator import get_narrator
    NARRATOR_AVAILABLE = True
except ImportError:
    NARRATOR_AVAILABLE = False
    logging.warning("Mission Control Narrator not available - Aquaman will operate without narrator")

logger = logging.getLogger(__name__)


class AquamanNetwork:
    """
    🌊 AQUAMAN - King of the Network Seas

    Aquaman's Powers:
    1. Monitor all network requests
    2. Analyze waterfall timing
    3. Detect blocking resources
    4. Identify critical path
    5. Analyze cache efficiency
    6. Track third-party resources
    7. Generate optimization recommendations
    """

    def __init__(self, narrator: Optional[Any] = None):
        """
        Initialize Aquaman's network command center

        Args:
            narrator: Mission Control Narrator for coordinated communication
        """
        # Initialize narrator for enhanced UX
        self.narrator = narrator if narrator else (get_narrator() if NARRATOR_AVAILABLE else None)

        # Hero identity for narrator integration
        self.hero_name = "Aquaman"
        self.hero_emoji = "🌊"

        logger.info(f"🌊 Aquaman - King of Network Seas initialized")

    def say(self, message: str, style: str = "tactical", technical_info: Optional[str] = None):
        """
        Aquaman dialogue - Deep-diver, investigative, fluid

        Personality traits:
        - Water and ocean metaphors
        - Deep investigation approach
        - Fluid tactical language
        - Network flow focused
        """
        if self.narrator:
            self.narrator.hero_speaks(
                f"{self.hero_emoji} {self.hero_name}",
                message, style, technical_info
            )

    def think(self, thought: str, step: Optional[int] = None, category: Optional[str] = "Diving"):
        """
        Sequential thinking with network focus

        Common categories for Aquaman:
        - Diving, Analyzing, Mapping, Investigating
        """
        if self.narrator:
            self.narrator.hero_thinks(
                f"{self.hero_emoji} {self.hero_name}",
                thought, step, category
            )

    def handoff(self, to_hero: str, context: str, details: Optional[str] = None):
        """
        Handoff network analysis to another hero

        Args:
            to_hero: Name of hero receiving the handoff (with emoji)
            context: What is being handed off
            details: Optional additional details
        """
        if self.narrator:
            self.narrator.hero_handoff(
                f"{self.hero_emoji} {self.hero_name}",
                to_hero,
                context,
                details
            )

    def analyze_network_traffic(self, mcp_tools: Dict,
                                resource_types: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        🌊 Aquaman analyzes all network traffic with hydrokinetic precision

        Args:
            mcp_tools: Dictionary of MCP tool functions
                {
                    'list_network_requests': mcp__chrome-devtools__list_network_requests,
                    'get_network_request': mcp__chrome-devtools__get_network_request
                }
            resource_types: Optional filter for resource types
                ['document', 'stylesheet', 'script', 'image', 'font', 'xhr', 'fetch', etc.]

        Returns:
            Aquaman's complete network analysis
        """
        logger.info(f"🌊 Aquaman diving into network traffic...")

        results = {
            'hero': '🌊 Aquaman - King of Network Seas',
            'timestamp': datetime.now().isoformat(),
            'network_analysis': {}
        }

        # Check if MCP tools available
        if not mcp_tools:
            logger.warning("🌊 No MCP tools provided - Aquaman needs his trident!")
            return {
                **results,
                'status': 'mcp_tools_missing',
                'message': 'Network analysis requires Chrome DevTools MCP tools',
                'required_tools': [
                    'mcp__chrome-devtools__list_network_requests',
                    'mcp__chrome-devtools__get_network_request'
                ]
            }

        try:
            # Step 1: List all network requests
            logger.info("🌊 Aquaman commanding the network seas...")
            list_func = mcp_tools.get('list_network_requests')

            all_requests = []

            if list_func:
                # Get all requests (paginated if needed)
                requests = list_func(resourceTypes=resource_types or [])
                all_requests.extend(requests.get('requests', []))

                logger.info(f"  ✓ Aquaman found {len(all_requests)} network requests")
            else:
                logger.warning("  ⚠️ list_network_requests function not provided")
                all_requests = []

            results['total_requests'] = len(all_requests)
            results['all_requests'] = all_requests

            # Step 2: Analyze Request Types
            type_analysis = self._analyze_request_types(all_requests)
            results['request_types'] = type_analysis

            # Step 3: Analyze Timing (Waterfall)
            timing_analysis = self._analyze_timing_waterfall(all_requests)
            results['timing_analysis'] = timing_analysis

            # Step 4: Detect Blocking Resources
            blocking_resources = self._detect_blocking_resources(all_requests)
            results['blocking_resources'] = blocking_resources

            # Step 5: Identify Critical Path
            critical_path = self._identify_critical_path(all_requests)
            results['critical_path'] = critical_path

            # Step 6: Analyze Cache Efficiency
            cache_analysis = self._analyze_cache_efficiency(all_requests)
            results['cache_analysis'] = cache_analysis

            # Step 7: Track Third-Party Resources
            third_party = self._track_third_party_resources(all_requests)
            results['third_party_analysis'] = third_party

            # Step 8: Calculate Aquaman Network Score
            network_score = self._calculate_network_score(results)
            results['aquaman_score'] = network_score

            # Step 9: Generate Recommendations
            recommendations = self._generate_aquaman_recommendations(results)
            results['aquaman_recommendations'] = recommendations

            logger.info(f"🌊 AQUAMAN NETWORK ANALYSIS COMPLETE")
            logger.info(f"🌊 Network Score: {network_score['score']:.1f}/100")
            logger.info(f"🌊 Aquaman says: {network_score['verdict']}")

        except Exception as e:
            logger.error(f"🌊 Aquaman encountered a tsunami: {e}")
            results['error'] = str(e)
            results['status'] = 'error'

        return results

    def _analyze_request_types(self, requests: List[Dict]) -> Dict[str, Any]:
        """
        🌊 Analyze distribution of resource types

        Args:
            requests: List of network requests

        Returns:
            Resource type analysis
        """
        type_counts = defaultdict(int)
        type_sizes = defaultdict(int)

        for req in requests:
            res_type = req.get('resourceType', 'other')
            size = req.get('size', 0)

            type_counts[res_type] += 1
            type_sizes[res_type] += size

        return {
            'type_counts': dict(type_counts),
            'type_sizes': dict(type_sizes),
            'total_size': sum(type_sizes.values()),
            'aquaman_observation': f'Aquaman sees {len(type_counts)} different resource types'
        }

    def _analyze_timing_waterfall(self, requests: List[Dict]) -> Dict[str, Any]:
        """
        🌊 Analyze request timing waterfall

        Timing phases:
        - DNS lookup
        - Connection setup
        - SSL/TLS negotiation
        - Request sent
        - Waiting (TTFB)
        - Content download

        Args:
            requests: List of network requests

        Returns:
            Waterfall timing analysis
        """
        total_time = 0
        slowest_requests = []

        for req in requests:
            timing = req.get('timing', {})

            # Calculate total request time
            request_time = (
                timing.get('dns', 0) +
                timing.get('connect', 0) +
                timing.get('ssl', 0) +
                timing.get('send', 0) +
                timing.get('wait', 0) +
                timing.get('receive', 0)
            )

            total_time += request_time

            slowest_requests.append({
                'url': req.get('url', ''),
                'time': request_time,
                'resource_type': req.get('resourceType', 'unknown')
            })

        # Sort by time (slowest first)
        slowest_requests.sort(key=lambda x: x['time'], reverse=True)

        return {
            'total_time_ms': total_time,
            'average_time_ms': total_time / len(requests) if requests else 0,
            'slowest_5_requests': slowest_requests[:5],
            'aquaman_verdict': 'Waters are calm' if total_time < 5000 else 'Stormy seas ahead!'
        }

    def _detect_blocking_resources(self, requests: List[Dict]) -> Dict[str, Any]:
        """
        🌊 Detect render-blocking resources

        Blocking resources:
        - Synchronous scripts in <head>
        - Stylesheets without media queries
        - Large critical resources

        Args:
            requests: List of network requests

        Returns:
            Blocking resource analysis
        """
        blocking = []

        for req in requests:
            res_type = req.get('resourceType', '')
            url = req.get('url', '')

            # Check for blocking scripts
            if res_type == 'script':
                # Scripts in head are typically blocking
                if not ('async' in url or 'defer' in url):
                    blocking.append({
                        'url': url,
                        'type': 'script',
                        'reason': 'Synchronous script - blocks parsing',
                        'aquaman_says': 'This script is a whirlpool - blocking the flow!'
                    })

            # Check for blocking stylesheets
            elif res_type == 'stylesheet':
                blocking.append({
                    'url': url,
                    'type': 'stylesheet',
                    'reason': 'CSS blocks rendering',
                    'aquaman_says': 'Stylesheet creating currents - consider critical CSS!'
                })

        return {
            'blocking_count': len(blocking),
            'blocking_resources': blocking[:10],  # Top 10
            'severity': 'high' if len(blocking) > 5 else 'moderate' if len(blocking) > 2 else 'low',
            'aquaman_command': 'Use async/defer for scripts! Use critical CSS!'
        }

    def _identify_critical_path(self, requests: List[Dict]) -> Dict[str, Any]:
        """
        🌊 Identify critical rendering path

        Critical path = resources needed for initial render:
        - HTML document
        - Critical CSS
        - Critical JavaScript
        - Above-the-fold images

        Args:
            requests: List of network requests

        Returns:
            Critical path analysis
        """
        critical_resources = []

        for req in requests:
            res_type = req.get('resourceType', '')
            url = req.get('url', '')

            # Document is always critical
            if res_type == 'document':
                critical_resources.append({
                    'url': url,
                    'type': 'document',
                    'priority': 'highest',
                    'aquaman_says': 'The main vessel - foundation of all!'
                })

            # CSS is critical
            elif res_type == 'stylesheet':
                critical_resources.append({
                    'url': url,
                    'type': 'stylesheet',
                    'priority': 'high',
                    'aquaman_says': 'These styles shape the waters!'
                })

            # Fonts can be critical
            elif res_type == 'font':
                critical_resources.append({
                    'url': url,
                    'type': 'font',
                    'priority': 'medium',
                    'aquaman_says': 'Font treasures from the deep!'
                })

        return {
            'critical_resource_count': len(critical_resources),
            'critical_resources': critical_resources[:10],
            'optimization_opportunity': 'Minimize critical path length for faster render',
            'aquaman_strategy': 'Reduce critical resources, inline critical CSS, preload fonts'
        }

    def _analyze_cache_efficiency(self, requests: List[Dict]) -> Dict[str, Any]:
        """
        🌊 Analyze cache efficiency

        Args:
            requests: List of network requests

        Returns:
            Cache analysis
        """
        cached_count = 0
        not_cached_count = 0
        cacheable_but_not_cached = []

        for req in requests:
            from_cache = req.get('fromCache', False)
            res_type = req.get('resourceType', '')

            if from_cache:
                cached_count += 1
            else:
                not_cached_count += 1

                # Check if should be cached
                if res_type in ['stylesheet', 'script', 'font', 'image']:
                    cacheable_but_not_cached.append({
                        'url': req.get('url', ''),
                        'type': res_type,
                        'aquaman_says': f'This {res_type} should swim in the cache!'
                    })

        cache_hit_rate = (cached_count / len(requests) * 100) if requests else 0

        return {
            'total_requests': len(requests),
            'cached_requests': cached_count,
            'not_cached_requests': not_cached_count,
            'cache_hit_rate_percent': round(cache_hit_rate, 1),
            'cacheable_but_not_cached': cacheable_but_not_cached[:10],
            'aquaman_verdict': 'Excellent caching!' if cache_hit_rate > 70 else 'Cache needs improvement!'
        }

    def _track_third_party_resources(self, requests: List[Dict]) -> Dict[str, Any]:
        """
        🌊 Track third-party resources

        Third-party = different domain from main site

        Args:
            requests: List of network requests

        Returns:
            Third-party analysis
        """
        # Get primary domain (from first request)
        primary_domain = None
        if requests:
            first_url = requests[0].get('url', '')
            primary_domain = self._extract_domain(first_url)

        third_party_domains = defaultdict(int)
        third_party_requests = []

        for req in requests:
            url = req.get('url', '')
            domain = self._extract_domain(url)

            if domain and domain != primary_domain:
                third_party_domains[domain] += 1
                third_party_requests.append({
                    'url': url,
                    'domain': domain,
                    'type': req.get('resourceType', 'unknown')
                })

        return {
            'third_party_domain_count': len(third_party_domains),
            'third_party_request_count': len(third_party_requests),
            'third_party_domains': dict(third_party_domains),
            'top_third_parties': sorted(
                third_party_domains.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5],
            'aquaman_warning': 'Too many third-party ships in these waters!' if len(third_party_domains) > 10 else 'Third-party traffic acceptable'
        }

    def _extract_domain(self, url: str) -> Optional[str]:
        """Extract domain from URL"""
        try:
            match = re.search(r'https?://([^/]+)', url)
            return match.group(1) if match else None
        except:
            return None

    def _calculate_network_score(self, results: Dict) -> Dict[str, Any]:
        """
        🌊 Calculate Aquaman's Network Score (0-100)

        Scoring:
        - Cache efficiency (25%)
        - Blocking resources (25%)
        - Third-party overhead (20%)
        - Request count (15%)
        - Resource timing (15%)

        Args:
            results: Network analysis results

        Returns:
            Network score
        """
        score = 100  # Start perfect

        # Cache efficiency
        cache_hit_rate = results.get('cache_analysis', {}).get('cache_hit_rate_percent', 0)
        if cache_hit_rate < 50:
            score -= 25
        elif cache_hit_rate < 70:
            score -= 15
        elif cache_hit_rate < 85:
            score -= 5

        # Blocking resources
        blocking_count = results.get('blocking_resources', {}).get('blocking_count', 0)
        if blocking_count > 10:
            score -= 25
        elif blocking_count > 5:
            score -= 15
        elif blocking_count > 2:
            score -= 5

        # Third-party overhead
        third_party_count = results.get('third_party_analysis', {}).get('third_party_domain_count', 0)
        if third_party_count > 15:
            score -= 20
        elif third_party_count > 10:
            score -= 10
        elif third_party_count > 5:
            score -= 5

        # Request count
        total_requests = results.get('total_requests', 0)
        if total_requests > 150:
            score -= 15
        elif total_requests > 100:
            score -= 10
        elif total_requests > 75:
            score -= 5

        # Floor at 0
        score = max(0, score)

        # Determine Aquaman verdict
        if score >= 90:
            verdict = "🌊 CRYSTAL CLEAR WATERS - Perfect network flow!"
            grade = "S+"
        elif score >= 80:
            verdict = "🌊 CALM SEAS - Excellent network performance!"
            grade = "A"
        elif score >= 70:
            verdict = "🌊 CHOPPY WATERS - Good but room for improvement"
            grade = "B"
        elif score >= 60:
            verdict = "🌊 ROUGH SEAS - Needs optimization"
            grade = "C"
        else:
            verdict = "🌊 TSUNAMI WARNING - Critical network issues!"
            grade = "D"

        return {
            'score': score,
            'grade': grade,
            'verdict': verdict,
            'cache_hit_rate': cache_hit_rate,
            'blocking_resources': blocking_count,
            'third_party_domains': third_party_count,
            'total_requests': total_requests
        }

    def _generate_aquaman_recommendations(self, results: Dict) -> List[Dict]:
        """
        🌊 Generate Aquaman's network optimization recommendations

        Args:
            results: Network analysis results

        Returns:
            List of recommendations
        """
        recommendations = []

        # Cache recommendations
        cache_hit_rate = results.get('cache_analysis', {}).get('cache_hit_rate_percent', 0)
        if cache_hit_rate < 70:
            recommendations.append({
                'priority': 'high',
                'area': 'Caching',
                'issue': f'Low cache hit rate ({cache_hit_rate:.1f}%)',
                'aquaman_says': 'Your cache is leaking like a damaged hull!',
                'actions': [
                    'Add cache-control headers to static resources',
                    'Use versioned URLs for cache busting',
                    'Implement service worker for offline caching',
                    'Use CDN for static assets'
                ]
            })

        # Blocking resource recommendations
        blocking_count = results.get('blocking_resources', {}).get('blocking_count', 0)
        if blocking_count > 3:
            recommendations.append({
                'priority': 'high',
                'area': 'Render Blocking',
                'issue': f'{blocking_count} render-blocking resources detected',
                'aquaman_says': 'These resources are anchors slowing your ship!',
                'actions': [
                    'Add async or defer to non-critical scripts',
                    'Inline critical CSS',
                    'Use media queries for non-critical CSS',
                    'Preload critical resources'
                ]
            })

        # Third-party recommendations
        third_party_count = results.get('third_party_analysis', {}).get('third_party_domain_count', 0)
        if third_party_count > 10:
            recommendations.append({
                'priority': 'medium',
                'area': 'Third-Party Resources',
                'issue': f'{third_party_count} third-party domains detected',
                'aquaman_says': 'Too many foreign vessels in Atlantean waters!',
                'actions': [
                    'Audit third-party scripts - remove unnecessary ones',
                    'Use resource hints (dns-prefetch, preconnect)',
                    'Consider self-hosting critical third-party resources',
                    'Lazy load third-party embeds'
                ]
            })

        # Request count recommendations
        total_requests = results.get('total_requests', 0)
        if total_requests > 100:
            recommendations.append({
                'priority': 'medium',
                'area': 'Request Count',
                'issue': f'{total_requests} total requests - too many!',
                'aquaman_says': 'The seas are crowded with too many ships!',
                'actions': [
                    'Combine CSS/JS files (bundle)',
                    'Use image sprites for icons',
                    'Implement HTTP/2 server push',
                    'Remove unnecessary requests'
                ]
            })

        return recommendations

    # Aliases for audit compatibility
    def _calculate_aquaman_score(self, results: Dict) -> Dict[str, Any]:
        """Alias for _calculate_network_score"""
        return self._calculate_network_score(results)

    def _generate_ocean_recommendations(self, results: Dict) -> List[Dict]:
        """Alias for _generate_aquaman_recommendations"""
        return self._generate_aquaman_recommendations(results)

    def detect_third_party_resources(self, mcp_tools: Dict) -> Dict[str, Any]:
        """
        🌊 Detect and analyze third-party resource domains

        Identifies all third-party resources loading on the page and analyzes their
        impact on performance. Useful for privacy audits and performance optimization.

        Args:
            mcp_tools: Dictionary of MCP tool functions
                {
                    'list_network_requests': mcp__chrome-devtools__list_network_requests
                }

        Returns:
            Third-party resource analysis with domain breakdown
        """
        self.say("Diving deep to track third-party resources", style="tactical")
        self.think("Scanning network traffic for foreign vessels", category="Diving")

        results = {
            'hero': '🌊 Aquaman',
            'timestamp': datetime.now().isoformat(),
            'third_party_analysis': {}
        }

        # Check if MCP tools available
        if not mcp_tools:
            return {
                **results,
                'status': 'mcp_tools_missing',
                'message': 'Aquaman needs MCP tools to command the seas'
            }

        try:
            # Get all network requests
            list_func = mcp_tools.get('list_network_requests')
            if not list_func:
                return {**results, 'status': 'error', 'message': 'list_network_requests not available'}

            all_requests = list_func().get('requests', [])
            self.think(f"Found {len(all_requests)} network requests", category="Analyzing")

            # Extract primary domain
            primary_domain = None
            if all_requests:
                first_url = all_requests[0].get('url', '')
                primary_domain = self._extract_domain(first_url)

            # Analyze third-party domains
            third_party_domains = defaultdict(lambda: {
                'count': 0,
                'total_size': 0,
                'resource_types': defaultdict(int),
                'urls': []
            })

            first_party_count = 0
            third_party_count = 0

            for req in all_requests:
                url = req.get('url', '')
                domain = self._extract_domain(url)
                size = req.get('size', 0)
                res_type = req.get('resourceType', 'unknown')

                if domain == primary_domain:
                    first_party_count += 1
                elif domain:
                    third_party_count += 1
                    third_party_domains[domain]['count'] += 1
                    third_party_domains[domain]['total_size'] += size
                    third_party_domains[domain]['resource_types'][res_type] += 1
                    third_party_domains[domain]['urls'].append(url)

            # Sort domains by request count
            sorted_domains = sorted(
                third_party_domains.items(),
                key=lambda x: x[1]['count'],
                reverse=True
            )

            # Calculate metrics
            total_third_party_size = sum(d['total_size'] for d in third_party_domains.values())
            total_requests = len(all_requests)
            third_party_percentage = (third_party_count / total_requests * 100) if total_requests > 0 else 0

            self.think("Mapping third-party domain distribution", category="Investigating")

            # Categorize domains by purpose
            tracking_domains = []
            cdn_domains = []
            analytics_domains = []
            other_domains = []

            for domain, data in sorted_domains:
                domain_lower = domain.lower()
                if any(keyword in domain_lower for keyword in ['track', 'analytics', 'metric', 'telemetry']):
                    analytics_domains.append(domain)
                elif any(keyword in domain_lower for keyword in ['cdn', 'cloudfront', 'akamai', 'fastly']):
                    cdn_domains.append(domain)
                elif any(keyword in domain_lower for keyword in ['ad', 'doubleclick', 'adsense', 'advertising']):
                    tracking_domains.append(domain)
                else:
                    other_domains.append(domain)

            results['third_party_analysis'] = {
                'total_requests': total_requests,
                'first_party_count': first_party_count,
                'third_party_count': third_party_count,
                'third_party_percentage': round(third_party_percentage, 1),
                'third_party_domain_count': len(third_party_domains),
                'total_third_party_size_bytes': total_third_party_size,
                'primary_domain': primary_domain,
                'top_10_domains': [
                    {
                        'domain': domain,
                        'request_count': data['count'],
                        'total_size_bytes': data['total_size'],
                        'resource_types': dict(data['resource_types'])
                    }
                    for domain, data in sorted_domains[:10]
                ],
                'domain_categories': {
                    'tracking_domains': tracking_domains,
                    'cdn_domains': cdn_domains,
                    'analytics_domains': analytics_domains,
                    'other_domains': other_domains[:10]
                }
            }

            # Aquaman's verdict
            if third_party_percentage > 50:
                verdict = "🌊 TSUNAMI WARNING - Too many foreign vessels!"
                severity = "critical"
            elif third_party_percentage > 30:
                verdict = "🌊 ROUGH SEAS - High third-party traffic"
                severity = "high"
            elif third_party_percentage > 15:
                verdict = "🌊 CHOPPY WATERS - Moderate third-party load"
                severity = "moderate"
            else:
                verdict = "🌊 CALM SEAS - Minimal third-party impact"
                severity = "low"

            results['aquaman_verdict'] = verdict
            results['severity'] = severity

            self.say(verdict, style="tactical", technical_info=f"{third_party_count}/{total_requests} requests ({third_party_percentage:.1f}%)")

        except Exception as e:
            logger.error(f"🌊 Aquaman encountered rough seas: {e}")
            results['error'] = str(e)
            results['status'] = 'error'

        return results

    def validate_resource_compression(self, mcp_tools: Dict) -> Dict[str, Any]:
        """
        🌊 Validate resource compression efficiency

        Analyzes which resources are compressed (gzip/brotli) and identifies
        opportunities for compression improvements.

        Args:
            mcp_tools: Dictionary of MCP tool functions
                {
                    'list_network_requests': mcp__chrome-devtools__list_network_requests,
                    'get_network_request': mcp__chrome-devtools__get_network_request
                }

        Returns:
            Compression analysis with optimization recommendations
        """
        self.say("Analyzing resource compression across the network", style="tactical")
        self.think("Checking compression headers and efficiency", category="Diving")

        results = {
            'hero': '🌊 Aquaman',
            'timestamp': datetime.now().isoformat(),
            'compression_analysis': {}
        }

        # Check if MCP tools available
        if not mcp_tools:
            return {
                **results,
                'status': 'mcp_tools_missing',
                'message': 'Aquaman needs MCP tools to analyze compression'
            }

        try:
            # Get all network requests
            list_func = mcp_tools.get('list_network_requests')
            if not list_func:
                return {**results, 'status': 'error', 'message': 'list_network_requests not available'}

            all_requests = list_func().get('requests', [])
            self.think(f"Scanning {len(all_requests)} resources for compression", category="Analyzing")

            # Analyze compression
            compressed_count = 0
            uncompressed_count = 0
            compressible_types = ['script', 'stylesheet', 'document', 'xhr', 'fetch', 'font']

            compression_stats = {
                'gzip': 0,
                'br': 0,  # brotli
                'deflate': 0,
                'none': 0
            }

            uncompressed_opportunities = []
            total_uncompressed_size = 0

            for req in all_requests:
                url = req.get('url', '')
                headers = req.get('responseHeaders', {})
                res_type = req.get('resourceType', 'unknown')
                size = req.get('size', 0)

                # Check content-encoding header
                content_encoding = headers.get('content-encoding', '').lower()

                if content_encoding:
                    compressed_count += 1
                    if 'br' in content_encoding:
                        compression_stats['br'] += 1
                    elif 'gzip' in content_encoding:
                        compression_stats['gzip'] += 1
                    elif 'deflate' in content_encoding:
                        compression_stats['deflate'] += 1
                else:
                    uncompressed_count += 1
                    compression_stats['none'] += 1

                    # Check if resource should be compressed
                    if res_type in compressible_types and size > 1024:  # > 1KB
                        uncompressed_opportunities.append({
                            'url': url,
                            'type': res_type,
                            'size_bytes': size,
                            'size_kb': round(size / 1024, 1),
                            'aquaman_says': f'This {res_type} should be compressed!'
                        })
                        total_uncompressed_size += size

            # Calculate metrics
            total_resources = len(all_requests)
            compression_rate = (compressed_count / total_resources * 100) if total_resources > 0 else 0

            # Sort uncompressed opportunities by size
            uncompressed_opportunities.sort(key=lambda x: x['size_bytes'], reverse=True)

            self.think("Calculating compression efficiency", category="Investigating")

            results['compression_analysis'] = {
                'total_resources': total_resources,
                'compressed_count': compressed_count,
                'uncompressed_count': uncompressed_count,
                'compression_rate_percent': round(compression_rate, 1),
                'compression_types': compression_stats,
                'uncompressed_opportunities': uncompressed_opportunities[:10],
                'total_uncompressed_size_bytes': total_uncompressed_size,
                'total_uncompressed_size_mb': round(total_uncompressed_size / (1024 * 1024), 2),
                'potential_savings_estimate_mb': round(total_uncompressed_size * 0.7 / (1024 * 1024), 2)  # ~70% compression
            }

            # Aquaman's verdict
            if compression_rate >= 90:
                verdict = "🌊 CRYSTAL CLEAR - Excellent compression!"
                grade = "S+"
            elif compression_rate >= 75:
                verdict = "🌊 CALM SEAS - Good compression coverage"
                grade = "A"
            elif compression_rate >= 60:
                verdict = "🌊 CHOPPY WATERS - Moderate compression"
                grade = "B"
            elif compression_rate >= 40:
                verdict = "🌊 ROUGH SEAS - Poor compression"
                grade = "C"
            else:
                verdict = "🌊 TSUNAMI WARNING - Critical compression issues!"
                grade = "D"

            results['aquaman_verdict'] = verdict
            results['compression_grade'] = grade
            results['recommendations'] = []

            # Generate recommendations
            if len(uncompressed_opportunities) > 0:
                self.think("Generating compression recommendations", category="Result")
                results['recommendations'].append({
                    'priority': 'high',
                    'area': 'Text Compression',
                    'issue': f'{len(uncompressed_opportunities)} uncompressed resources ({total_uncompressed_size / (1024 * 1024):.2f} MB)',
                    'aquaman_says': 'These resources are leaking bandwidth like a damaged hull!',
                    'actions': [
                        'Enable gzip or brotli compression on server',
                        'Configure compression for JS, CSS, HTML, JSON',
                        'Use brotli for better compression (5-20% smaller than gzip)',
                        'Verify compression headers: Content-Encoding: gzip/br'
                    ]
                })

            self.say(verdict, style="tactical", technical_info=f"{compression_rate:.1f}% compression rate, {len(uncompressed_opportunities)} opportunities")

        except Exception as e:
            logger.error(f"🌊 Aquaman encountered turbulence: {e}")
            results['error'] = str(e)
            results['status'] = 'error'

        return results

    def analyze_slow_responses(self, mcp_tools: Dict, threshold_ms: int = 1000) -> Dict[str, Any]:
        """
        🌊 Analyze slow API and XHR responses

        Identifies slow network responses (XHR, fetch, API calls) that may be
        degrading user experience.

        Args:
            mcp_tools: Dictionary of MCP tool functions
                {
                    'list_network_requests': mcp__chrome-devtools__list_network_requests
                }
            threshold_ms: Response time threshold in milliseconds (default: 1000ms)

        Returns:
            Slow response analysis with timing breakdown
        """
        self.say(f"Detecting slow responses over {threshold_ms}ms", style="tactical")
        self.think("Analyzing API and XHR response times", category="Diving")

        results = {
            'hero': '🌊 Aquaman',
            'timestamp': datetime.now().isoformat(),
            'slow_response_analysis': {}
        }

        # Check if MCP tools available
        if not mcp_tools:
            return {
                **results,
                'status': 'mcp_tools_missing',
                'message': 'Aquaman needs MCP tools to analyze responses'
            }

        try:
            # Get all network requests
            list_func = mcp_tools.get('list_network_requests')
            if not list_func:
                return {**results, 'status': 'error', 'message': 'list_network_requests not available'}

            all_requests = list_func().get('requests', [])

            # Filter for API/XHR/Fetch requests
            api_requests = [req for req in all_requests if req.get('resourceType') in ['xhr', 'fetch']]

            self.think(f"Scanning {len(api_requests)} API/XHR requests", category="Analyzing")

            slow_responses = []
            fast_responses = []
            timing_distribution = {
                '0-100ms': 0,
                '100-500ms': 0,
                '500-1000ms': 0,
                '1000-3000ms': 0,
                '3000ms+': 0
            }

            for req in api_requests:
                timing = req.get('timing', {})

                # Calculate total response time (TTFB + download)
                wait_time = timing.get('wait', 0)  # Time to first byte
                receive_time = timing.get('receive', 0)  # Download time
                total_time = wait_time + receive_time

                url = req.get('url', '')
                method = req.get('method', 'GET')
                status = req.get('status', 0)

                # Categorize timing
                if total_time < 100:
                    timing_distribution['0-100ms'] += 1
                    fast_responses.append({'url': url, 'time_ms': total_time})
                elif total_time < 500:
                    timing_distribution['100-500ms'] += 1
                    fast_responses.append({'url': url, 'time_ms': total_time})
                elif total_time < 1000:
                    timing_distribution['500-1000ms'] += 1
                elif total_time < 3000:
                    timing_distribution['1000-3000ms'] += 1
                else:
                    timing_distribution['3000ms+'] += 1

                # Check if slow
                if total_time >= threshold_ms:
                    slow_responses.append({
                        'url': url,
                        'method': method,
                        'status': status,
                        'total_time_ms': round(total_time, 2),
                        'ttfb_ms': round(wait_time, 2),
                        'download_ms': round(receive_time, 2),
                        'severity': 'critical' if total_time > 3000 else 'high' if total_time > 2000 else 'moderate',
                        'aquaman_says': self._get_slow_response_message(total_time)
                    })

            # Sort slow responses by time (slowest first)
            slow_responses.sort(key=lambda x: x['total_time_ms'], reverse=True)

            self.think("Calculating response time statistics", category="Investigating")

            # Calculate statistics
            if api_requests:
                all_times = []
                for req in api_requests:
                    timing = req.get('timing', {})
                    total = timing.get('wait', 0) + timing.get('receive', 0)
                    all_times.append(total)

                avg_response_time = sum(all_times) / len(all_times)
                median_response_time = sorted(all_times)[len(all_times) // 2]
                p95_response_time = sorted(all_times)[int(len(all_times) * 0.95)]
            else:
                avg_response_time = 0
                median_response_time = 0
                p95_response_time = 0

            results['slow_response_analysis'] = {
                'threshold_ms': threshold_ms,
                'total_api_requests': len(api_requests),
                'slow_response_count': len(slow_responses),
                'slow_response_percentage': round(len(slow_responses) / len(api_requests) * 100, 1) if api_requests else 0,
                'timing_distribution': timing_distribution,
                'statistics': {
                    'avg_response_time_ms': round(avg_response_time, 2),
                    'median_response_time_ms': round(median_response_time, 2),
                    'p95_response_time_ms': round(p95_response_time, 2)
                },
                'slowest_10_responses': slow_responses[:10],
                'fastest_5_responses': sorted(fast_responses, key=lambda x: x['time_ms'])[:5]
            }

            # Aquaman's verdict
            slow_percentage = len(slow_responses) / len(api_requests) * 100 if api_requests else 0

            if slow_percentage == 0:
                verdict = "🌊 CRYSTAL CLEAR WATERS - All responses fast!"
                grade = "S+"
            elif slow_percentage < 5:
                verdict = "🌊 CALM SEAS - Minimal slow responses"
                grade = "A"
            elif slow_percentage < 15:
                verdict = "🌊 CHOPPY WATERS - Some slow responses"
                grade = "B"
            elif slow_percentage < 30:
                verdict = "🌊 ROUGH SEAS - Many slow responses"
                grade = "C"
            else:
                verdict = "🌊 TSUNAMI WARNING - Critical API slowness!"
                grade = "D"

            results['aquaman_verdict'] = verdict
            results['response_time_grade'] = grade
            results['recommendations'] = []

            # Generate recommendations
            if len(slow_responses) > 0:
                self.think("Generating optimization recommendations", category="Result")
                results['recommendations'].append({
                    'priority': 'high',
                    'area': 'API Response Time',
                    'issue': f'{len(slow_responses)} slow API responses detected',
                    'aquaman_says': 'These API calls are stuck in deep ocean currents!',
                    'actions': [
                        'Optimize database queries for slow endpoints',
                        'Implement caching for frequently accessed data',
                        'Use CDN for API responses when possible',
                        'Consider pagination for large data sets',
                        'Add response compression',
                        'Profile server-side code for bottlenecks'
                    ]
                })

            self.say(verdict, style="tactical", technical_info=f"{len(slow_responses)}/{len(api_requests)} slow responses, avg {avg_response_time:.0f}ms")

        except Exception as e:
            logger.error(f"🌊 Aquaman encountered a whirlpool: {e}")
            results['error'] = str(e)
            results['status'] = 'error'

        return results

    def _get_slow_response_message(self, time_ms: float) -> str:
        """Generate Aquaman's message for slow response based on severity"""
        if time_ms > 5000:
            return "Trapped in the Mariana Trench - extremely slow!"
        elif time_ms > 3000:
            return "Swimming through molasses - very slow!"
        elif time_ms > 2000:
            return "Fighting strong currents - quite slow"
        else:
            return "Choppy waters detected - moderately slow"


# Main entry point - Aquaman's Mission Interface
def aquaman_analyze_network(mcp_tools: Dict,
                            resource_types: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    🌊 Aquaman analyzes all network traffic!

    The King of Atlantis commands the network seas!

    Args:
        mcp_tools: Dictionary of MCP tool functions
        resource_types: Optional filter for specific resource types

    Returns:
        Aquaman's complete network analysis
    """
    aquaman = AquamanNetwork()
    return aquaman.analyze_network_traffic(mcp_tools, resource_types)
