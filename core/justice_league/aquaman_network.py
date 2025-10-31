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
