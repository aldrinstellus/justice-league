"""
🦸🌊 SUPERMAN NETWORK TIMING ANALYSIS - Feature #5
Justice League Enhancement: Advanced Network Performance Analysis

Superman enhances Aquaman with advanced network timing capabilities:
- Detailed waterfall chart data generation
- Critical path detection with timing
- Blocking resource identification with impact analysis
- Request/response timing breakdown
- Network bottleneck detection
- Performance budget tracking
- CDN optimization analysis

"With X-ray vision, I see through every network request!" - Superman

MCP Tools Used:
- mcp__chrome-devtools__list_network_requests()
- mcp__chrome-devtools__get_network_request(url)
"""

import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from collections import defaultdict
import json
from pathlib import Path

logger = logging.getLogger(__name__)


class SupermanNetworkAnalysis:
    """
    🦸🌊 SUPERMAN NETWORK TIMING ANALYSIS

    Superman's Advanced Network Powers:
    1. Generate detailed waterfall chart data
    2. Detect critical rendering path with timing
    3. Identify blocking resources with impact scores
    4. Analyze request/response timing phases
    5. Detect network bottlenecks
    6. Track performance budgets
    7. Analyze CDN effectiveness
    8. Generate optimization roadmap
    """

    def __init__(self, baseline_dir: str = '/tmp/aldo-vision-network-baselines'):
        """
        Initialize Superman's network analysis system

        Args:
            baseline_dir: Directory for storing network baselines
        """
        self.baseline_dir = Path(baseline_dir)
        self.baseline_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"🦸🌊 Superman Network Timing Analysis initialized")

    def analyze_network_complete(
        self,
        mcp_tools: Dict,
        url: str,
        test_name: str = 'default',
        store_baseline: bool = True,
        performance_budget: Optional[Dict[str, int]] = None
    ) -> Dict[str, Any]:
        """
        🦸🌊 Superman's complete network timing analysis

        10-Step Analysis Workflow:
        1. List all network requests
        2. Generate waterfall chart data
        3. Detect critical rendering path
        4. Identify blocking resources with impact
        5. Analyze request/response timing phases
        6. Detect network bottlenecks
        7. Check performance budget
        8. Analyze CDN effectiveness
        9. Calculate Superman network score
        10. Generate optimization recommendations

        Args:
            mcp_tools: Dictionary of MCP tool functions
            url: URL being tested
            test_name: Test identifier for baselines
            store_baseline: Whether to store results as baseline
            performance_budget: Optional performance budget
                {
                    'total_requests': 100,
                    'total_size_kb': 2000,
                    'scripts_kb': 500,
                    'images_kb': 800,
                    'css_kb': 200
                }

        Returns:
            Complete network timing analysis with Superman enhancements
        """
        logger.info(f"🦸🌊 Superman analyzing network for: {url}")

        results = {
            'status': 'success',
            'hero': '🦸🌊 Superman + Aquaman Network Analysis',
            'timestamp': datetime.now().isoformat(),
            'url': url,
            'test_name': test_name
        }

        try:
            # Step 1: List all network requests
            logger.info(f"🦸 Step 1: Collecting all network requests...")
            list_func = mcp_tools.get('list_network_requests')
            get_func = mcp_tools.get('get_network_request')

            if not list_func:
                raise ValueError("list_network_requests MCP tool required")

            # Get all requests
            all_requests = self._collect_all_requests(list_func)
            logger.info(f"  ✓ Collected {len(all_requests)} network requests")

            results['total_requests'] = len(all_requests)
            results['all_requests'] = all_requests

            # Step 2: Generate waterfall chart data
            logger.info(f"🦸 Step 2: Generating waterfall chart data...")
            waterfall = self._generate_waterfall_data(all_requests)
            results['waterfall'] = waterfall
            logger.info(f"  ✓ Waterfall generated with {len(waterfall['entries'])} entries")

            # Step 3: Detect critical rendering path
            logger.info(f"🦸 Step 3: Detecting critical rendering path...")
            critical_path = self._detect_critical_path_advanced(all_requests)
            results['critical_path'] = critical_path
            logger.info(f"  ✓ Found {critical_path['critical_resource_count']} critical resources")

            # Step 4: Identify blocking resources with impact
            logger.info(f"🦸 Step 4: Identifying blocking resources...")
            blocking = self._identify_blocking_resources_advanced(all_requests, waterfall)
            results['blocking_resources'] = blocking
            logger.info(f"  ✓ Found {blocking['blocking_count']} blocking resources")

            # Step 5: Analyze request/response timing phases
            logger.info(f"🦸 Step 5: Analyzing timing phases...")
            timing_phases = self._analyze_timing_phases(all_requests)
            results['timing_phases'] = timing_phases
            logger.info(f"  ✓ Analyzed {timing_phases['requests_analyzed']} request timings")

            # Step 6: Detect network bottlenecks
            logger.info(f"🦸 Step 6: Detecting network bottlenecks...")
            bottlenecks = self._detect_network_bottlenecks(all_requests, timing_phases)
            results['bottlenecks'] = bottlenecks
            logger.info(f"  ✓ Found {len(bottlenecks['bottlenecks'])} bottlenecks")

            # Step 7: Check performance budget
            logger.info(f"🦸 Step 7: Checking performance budget...")
            budget_check = self._check_performance_budget(
                all_requests,
                performance_budget or self._get_default_budget()
            )
            results['performance_budget'] = budget_check
            logger.info(f"  ✓ Budget status: {budget_check['status']}")

            # Step 8: Analyze CDN effectiveness
            logger.info(f"🦸 Step 8: Analyzing CDN effectiveness...")
            cdn_analysis = self._analyze_cdn_effectiveness(all_requests)
            results['cdn_analysis'] = cdn_analysis
            logger.info(f"  ✓ CDN usage: {cdn_analysis['cdn_usage_percent']:.1f}%")

            # Step 9: Calculate Superman network score
            logger.info(f"🦸 Step 9: Calculating Superman network score...")
            network_score = self._calculate_superman_network_score(results)
            results['superman_network_score'] = network_score
            logger.info(f"  ✓ Network Score: {network_score['score']}/100 ({network_score['grade']})")

            # Step 10: Generate optimization recommendations
            logger.info(f"🦸 Step 10: Generating recommendations...")
            recommendations = self._generate_superman_network_recommendations(results)
            results['superman_recommendations'] = recommendations
            logger.info(f"  ✓ Generated {len(recommendations)} recommendations")

            # Store baseline if requested
            if store_baseline:
                self._store_baseline(test_name, results)
                logger.info(f"  ✓ Baseline stored for '{test_name}'")

            logger.info(f"🦸🌊 SUPERMAN NETWORK ANALYSIS COMPLETE!")
            logger.info(f"🦸 Score: {network_score['score']}/100 ({network_score['grade']})")
            logger.info(f"🦸 Superman says: {network_score['verdict']}")

        except Exception as e:
            logger.error(f"🦸 Superman encountered error: {e}")
            results['status'] = 'error'
            results['error'] = str(e)

        return results

    def _collect_all_requests(self, list_func) -> List[Dict]:
        """
        Collect all network requests with pagination

        Args:
            list_func: MCP list_network_requests function

        Returns:
            List of all network requests
        """
        all_requests = []
        page_idx = 0
        page_size = 100

        while True:
            try:
                response = list_func(pageIdx=page_idx, pageSize=page_size)
                requests = response.get('requests', [])

                if not requests:
                    break

                all_requests.extend(requests)

                # Check if more pages
                if len(requests) < page_size:
                    break

                page_idx += 1

            except Exception as e:
                logger.warning(f"Error paginating requests: {e}")
                break

        return all_requests

    def _generate_waterfall_data(self, requests: List[Dict]) -> Dict[str, Any]:
        """
        🦸 Generate detailed waterfall chart data

        Waterfall shows:
        - Request start time (relative to page load)
        - Timing phases (DNS, Connect, SSL, Send, Wait, Receive)
        - Total duration
        - Resource type
        - Status code
        - Size

        Args:
            requests: List of network requests

        Returns:
            Waterfall chart data in HAR-like format
        """
        # Find earliest request time as baseline
        start_times = [r.get('startTime', 0) for r in requests if r.get('startTime')]
        page_start_time = min(start_times) if start_times else 0

        waterfall_entries = []

        for idx, req in enumerate(requests):
            url = req.get('url', '')
            timing = req.get('timing', {})
            start_time = req.get('startTime', 0)

            # Calculate relative start time
            relative_start = (start_time - page_start_time) * 1000  # Convert to ms

            # Extract timing phases (all in ms)
            dns_time = timing.get('dns', 0)
            connect_time = timing.get('connect', 0)
            ssl_time = timing.get('ssl', 0)
            send_time = timing.get('send', 0)
            wait_time = timing.get('wait', 0)  # TTFB - Time to First Byte
            receive_time = timing.get('receive', 0)

            # Calculate total duration
            total_duration = (
                dns_time + connect_time + ssl_time +
                send_time + wait_time + receive_time
            )

            waterfall_entry = {
                'index': idx,
                'url': url,
                'method': req.get('method', 'GET'),
                'status': req.get('status', 0),
                'resourceType': req.get('resourceType', 'other'),
                'size': req.get('size', 0),

                # Timing data
                'startTime': relative_start,
                'duration': total_duration,

                # Timing phases
                'timings': {
                    'blocked': 0,  # Chrome doesn't expose this directly
                    'dns': dns_time,
                    'connect': connect_time,
                    'ssl': ssl_time,
                    'send': send_time,
                    'wait': wait_time,  # TTFB
                    'receive': receive_time
                },

                # Additional metadata
                'priority': req.get('priority', 'medium'),
                'fromCache': req.get('fromCache', False),
                'initiator': req.get('initiator', {}).get('type', 'unknown')
            }

            waterfall_entries.append(waterfall_entry)

        # Sort by start time
        waterfall_entries.sort(key=lambda x: x['startTime'])

        # Calculate summary statistics
        total_time = max(
            [e['startTime'] + e['duration'] for e in waterfall_entries]
        ) if waterfall_entries else 0

        return {
            'page_start_time': page_start_time,
            'total_time_ms': total_time,
            'entry_count': len(waterfall_entries),
            'entries': waterfall_entries,

            # HAR-compatible format
            'version': '1.2',
            'creator': {
                'name': 'Superman Network Analysis',
                'version': '1.0.0'
            }
        }

    def _detect_critical_path_advanced(self, requests: List[Dict]) -> Dict[str, Any]:
        """
        🦸 Detect critical rendering path with advanced timing analysis

        Critical path = resources that block initial render

        Args:
            requests: List of network requests

        Returns:
            Advanced critical path analysis
        """
        critical_resources = []
        critical_path_length = 0

        for req in requests:
            res_type = req.get('resourceType', '')
            url = req.get('url', '')
            timing = req.get('timing', {})
            priority = req.get('priority', 'low')

            is_critical = False
            reason = []

            # Document is always critical
            if res_type == 'document':
                is_critical = True
                reason.append('Main HTML document')

            # Blocking CSS is critical
            elif res_type == 'stylesheet':
                is_critical = True
                reason.append('Render-blocking CSS')

            # High priority scripts are critical
            elif res_type == 'script' and priority in ['high', 'very-high']:
                is_critical = True
                reason.append('High priority JavaScript')

            # Fonts can be critical
            elif res_type == 'font':
                is_critical = True
                reason.append('Web font (may block text render)')

            if is_critical:
                # Calculate resource time
                resource_time = (
                    timing.get('dns', 0) + timing.get('connect', 0) +
                    timing.get('ssl', 0) + timing.get('send', 0) +
                    timing.get('wait', 0) + timing.get('receive', 0)
                )

                critical_resources.append({
                    'url': url,
                    'type': res_type,
                    'priority': priority,
                    'size': req.get('size', 0),
                    'time_ms': resource_time,
                    'reasons': reason,
                    'superman_analysis': ', '.join(reason)
                })

                critical_path_length += resource_time

        # Sort by time (slowest first)
        critical_resources.sort(key=lambda x: x['time_ms'], reverse=True)

        return {
            'critical_resource_count': len(critical_resources),
            'critical_resources': critical_resources,
            'critical_path_length_ms': critical_path_length,
            'optimization_potential_ms': critical_path_length * 0.3,  # Estimate 30% reduction
            'superman_verdict': (
                '🦸 Critical path is lean!' if critical_path_length < 2000
                else '🦸 Critical path needs optimization' if critical_path_length < 4000
                else '🦸 Critical path is too long - major optimization needed!'
            )
        }

    def _identify_blocking_resources_advanced(
        self,
        requests: List[Dict],
        waterfall: Dict
    ) -> Dict[str, Any]:
        """
        🦸 Identify blocking resources with impact analysis

        Args:
            requests: List of network requests
            waterfall: Waterfall data

        Returns:
            Advanced blocking resource analysis with impact scores
        """
        blocking_resources = []

        for req in requests:
            res_type = req.get('resourceType', '')
            url = req.get('url', '')
            timing = req.get('timing', {})
            priority = req.get('priority', 'low')

            is_blocking = False
            impact_score = 0
            blocking_reason = []

            # Check for blocking scripts
            if res_type == 'script':
                # Check if synchronous (high priority usually means blocking)
                if priority in ['high', 'very-high']:
                    is_blocking = True
                    impact_score = 8
                    blocking_reason.append('Synchronous script blocks HTML parsing')

            # Check for blocking CSS
            elif res_type == 'stylesheet':
                is_blocking = True
                impact_score = 9  # CSS almost always blocks render
                blocking_reason.append('CSS blocks rendering')

            # Check for blocking fonts
            elif res_type == 'font':
                is_blocking = True
                impact_score = 6  # Fonts can block text rendering
                blocking_reason.append('Font may block text rendering (FOIT/FOUT)')

            if is_blocking:
                # Calculate blocking time
                blocking_time = (
                    timing.get('wait', 0) + timing.get('receive', 0)
                )

                # Adjust impact based on timing
                if blocking_time > 1000:
                    impact_score += 2
                elif blocking_time > 500:
                    impact_score += 1

                blocking_resources.append({
                    'url': url,
                    'type': res_type,
                    'impact_score': min(10, impact_score),  # Cap at 10
                    'blocking_time_ms': blocking_time,
                    'size': req.get('size', 0),
                    'reasons': blocking_reason,
                    'superman_says': (
                        '🦸 CRITICAL - Fix immediately!' if impact_score >= 9
                        else '🦸 HIGH - Optimize soon' if impact_score >= 7
                        else '🦸 MEDIUM - Consider optimization'
                    )
                })

        # Sort by impact score (highest first)
        blocking_resources.sort(key=lambda x: x['impact_score'], reverse=True)

        # Calculate total blocking impact
        total_blocking_time = sum(r['blocking_time_ms'] for r in blocking_resources)

        return {
            'blocking_count': len(blocking_resources),
            'blocking_resources': blocking_resources,
            'total_blocking_time_ms': total_blocking_time,
            'critical_blocking': [r for r in blocking_resources if r['impact_score'] >= 9],
            'high_impact_blocking': [r for r in blocking_resources if r['impact_score'] >= 7],
            'superman_assessment': (
                '🦸 Blocking resources under control' if len(blocking_resources) <= 3
                else '🦸 Moderate blocking issues' if len(blocking_resources) <= 6
                else '🦸 Severe blocking - needs immediate attention!'
            )
        }

    def _analyze_timing_phases(self, requests: List[Dict]) -> Dict[str, Any]:
        """
        🦸 Analyze request/response timing phases in detail

        Phases:
        - DNS: Domain name resolution
        - Connect: TCP connection
        - SSL: TLS negotiation
        - Send: Request sent
        - Wait: Server processing (TTFB)
        - Receive: Response download

        Args:
            requests: List of network requests

        Returns:
            Detailed timing phase analysis
        """
        phase_totals = {
            'dns': 0,
            'connect': 0,
            'ssl': 0,
            'send': 0,
            'wait': 0,
            'receive': 0
        }

        phase_counts = {
            'dns': 0,
            'connect': 0,
            'ssl': 0,
            'send': 0,
            'wait': 0,
            'receive': 0
        }

        slowest_by_phase = {
            'dns': None,
            'connect': None,
            'ssl': None,
            'send': None,
            'wait': None,
            'receive': None
        }

        for req in requests:
            timing = req.get('timing', {})
            url = req.get('url', '')

            for phase in phase_totals.keys():
                phase_time = timing.get(phase, 0)

                if phase_time > 0:
                    phase_totals[phase] += phase_time
                    phase_counts[phase] += 1

                    # Track slowest
                    if (slowest_by_phase[phase] is None or
                        phase_time > slowest_by_phase[phase]['time']):
                        slowest_by_phase[phase] = {
                            'url': url,
                            'time': phase_time,
                            'resourceType': req.get('resourceType', 'unknown')
                        }

        # Calculate averages
        phase_averages = {
            phase: (phase_totals[phase] / phase_counts[phase])
            if phase_counts[phase] > 0 else 0
            for phase in phase_totals.keys()
        }

        return {
            'requests_analyzed': len(requests),
            'phase_totals_ms': phase_totals,
            'phase_averages_ms': phase_averages,
            'phase_counts': phase_counts,
            'slowest_by_phase': slowest_by_phase,

            # Superman insights
            'superman_insights': {
                'dns_optimization': (
                    'Use DNS prefetch for third-party domains'
                    if phase_averages['dns'] > 50 else 'DNS timing is good'
                ),
                'connection_optimization': (
                    'Use preconnect or HTTP/2'
                    if phase_averages['connect'] > 100 else 'Connection timing is good'
                ),
                'ssl_optimization': (
                    'Optimize TLS configuration'
                    if phase_averages['ssl'] > 100 else 'SSL timing is good'
                ),
                'ttfb_optimization': (
                    'Server response time too slow - optimize backend'
                    if phase_averages['wait'] > 200 else 'TTFB is good'
                )
            }
        }

    def _detect_network_bottlenecks(
        self,
        requests: List[Dict],
        timing_phases: Dict
    ) -> Dict[str, Any]:
        """
        🦸 Detect network bottlenecks

        Bottlenecks:
        - Slow DNS resolution
        - Slow connections
        - Slow SSL
        - High TTFB (slow server)
        - Large downloads
        - Too many requests to same domain (queue blocking)

        Args:
            requests: List of network requests
            timing_phases: Timing phase analysis

        Returns:
            Bottleneck detection results
        """
        bottlenecks = []

        # Check DNS bottlenecks
        avg_dns = timing_phases['phase_averages_ms']['dns']
        if avg_dns > 100:
            bottlenecks.append({
                'type': 'dns',
                'severity': 'high' if avg_dns > 200 else 'medium',
                'value': avg_dns,
                'issue': f'Slow DNS resolution ({avg_dns:.0f}ms average)',
                'superman_says': '🦸 DNS is slowing you down - use DNS prefetch!',
                'fix': 'Add <link rel="dns-prefetch" href="//domain.com"> for third-party domains'
            })

        # Check connection bottlenecks
        avg_connect = timing_phases['phase_averages_ms']['connect']
        if avg_connect > 150:
            bottlenecks.append({
                'type': 'connection',
                'severity': 'high' if avg_connect > 300 else 'medium',
                'value': avg_connect,
                'issue': f'Slow TCP connections ({avg_connect:.0f}ms average)',
                'superman_says': '🦸 Connection setup is too slow - use HTTP/2 or preconnect!',
                'fix': 'Enable HTTP/2, use <link rel="preconnect">, or use CDN'
            })

        # Check TTFB bottlenecks
        avg_wait = timing_phases['phase_averages_ms']['wait']
        if avg_wait > 300:
            bottlenecks.append({
                'type': 'ttfb',
                'severity': 'critical' if avg_wait > 600 else 'high',
                'value': avg_wait,
                'issue': f'Slow server response ({avg_wait:.0f}ms TTFB)',
                'superman_says': '🦸 Server is too slow - optimize backend or use caching!',
                'fix': 'Optimize database queries, add server caching, use CDN'
            })

        # Check for large downloads
        large_resources = [
            r for r in requests
            if r.get('size', 0) > 1024 * 1024  # > 1MB
        ]

        if large_resources:
            total_large_size = sum(r.get('size', 0) for r in large_resources)
            bottlenecks.append({
                'type': 'large_resources',
                'severity': 'high' if len(large_resources) > 5 else 'medium',
                'value': len(large_resources),
                'issue': f'{len(large_resources)} resources over 1MB ({total_large_size / 1024 / 1024:.1f}MB total)',
                'superman_says': '🦸 Large files detected - compress or lazy load!',
                'fix': 'Compress images, use lazy loading, split bundles'
            })

        # Check request count per domain
        domain_counts = defaultdict(int)
        for req in requests:
            url = req.get('url', '')
            # Extract domain
            import re
            match = re.search(r'https?://([^/]+)', url)
            if match:
                domain_counts[match.group(1)] += 1

        high_traffic_domains = {
            domain: count for domain, count in domain_counts.items()
            if count > 20
        }

        if high_traffic_domains:
            bottlenecks.append({
                'type': 'domain_queueing',
                'severity': 'medium',
                'value': len(high_traffic_domains),
                'issue': f'{len(high_traffic_domains)} domains with 20+ requests (possible queue blocking)',
                'superman_says': '🦸 Too many requests to same domains - use HTTP/2 or domain sharding!',
                'fix': 'Enable HTTP/2 or spread requests across multiple domains'
            })

        return {
            'bottleneck_count': len(bottlenecks),
            'bottlenecks': bottlenecks,
            'critical_bottlenecks': [b for b in bottlenecks if b.get('severity') == 'critical'],
            'high_severity_bottlenecks': [b for b in bottlenecks if b.get('severity') == 'high'],
            'superman_status': (
                '🦸 No major bottlenecks detected!' if len(bottlenecks) == 0
                else '🦸 Some bottlenecks found - optimization recommended' if len(bottlenecks) <= 2
                else '🦸 Multiple bottlenecks - needs immediate attention!'
            )
        }

    def _check_performance_budget(
        self,
        requests: List[Dict],
        budget: Dict[str, int]
    ) -> Dict[str, Any]:
        """
        🦸 Check performance budget compliance

        Args:
            requests: List of network requests
            budget: Performance budget thresholds

        Returns:
            Budget compliance check
        """
        # Calculate actual metrics
        actual = {
            'total_requests': len(requests),
            'total_size_kb': sum(r.get('size', 0) for r in requests) / 1024,
            'scripts_kb': sum(
                r.get('size', 0) for r in requests
                if r.get('resourceType') == 'script'
            ) / 1024,
            'images_kb': sum(
                r.get('size', 0) for r in requests
                if r.get('resourceType') == 'image'
            ) / 1024,
            'css_kb': sum(
                r.get('size', 0) for r in requests
                if r.get('resourceType') == 'stylesheet'
            ) / 1024
        }

        # Compare to budget
        violations = []
        for key, value in actual.items():
            budget_value = budget.get(key, float('inf'))

            if value > budget_value:
                over_by = value - budget_value
                over_percent = (over_by / budget_value * 100) if budget_value > 0 else 0

                violations.append({
                    'metric': key,
                    'budget': budget_value,
                    'actual': round(value, 1),
                    'over_by': round(over_by, 1),
                    'over_percent': round(over_percent, 1),
                    'superman_says': f'🦸 Over budget by {over_percent:.0f}%!'
                })

        return {
            'budget': budget,
            'actual': {k: round(v, 1) for k, v in actual.items()},
            'violations': violations,
            'violation_count': len(violations),
            'status': 'over_budget' if violations else 'within_budget',
            'superman_verdict': (
                '🦸 Perfect! Within performance budget!' if not violations
                else f'🦸 {len(violations)} budget violations - optimize!'
            )
        }

    def _analyze_cdn_effectiveness(self, requests: List[Dict]) -> Dict[str, Any]:
        """
        🦸 Analyze CDN usage and effectiveness

        Args:
            requests: List of network requests

        Returns:
            CDN analysis
        """
        cdn_patterns = [
            'cdn.', 'cloudfront.net', 'fastly.net', 'akamai.net',
            'cloudflare.com', 'jsdelivr.net', 'unpkg.com'
        ]

        cdn_requests = []
        cdn_size = 0

        for req in requests:
            url = req.get('url', '')

            if any(pattern in url.lower() for pattern in cdn_patterns):
                cdn_requests.append({
                    'url': url,
                    'size': req.get('size', 0),
                    'type': req.get('resourceType', 'unknown')
                })
                cdn_size += req.get('size', 0)

        total_size = sum(r.get('size', 0) for r in requests)
        cdn_usage_percent = (cdn_size / total_size * 100) if total_size > 0 else 0

        return {
            'cdn_request_count': len(cdn_requests),
            'cdn_size_kb': cdn_size / 1024,
            'cdn_usage_percent': round(cdn_usage_percent, 1),
            'cdn_requests': cdn_requests[:10],  # Top 10
            'superman_assessment': (
                '🦸 Excellent CDN usage!' if cdn_usage_percent > 70
                else '🦸 Good CDN usage' if cdn_usage_percent > 40
                else '🦸 Low CDN usage - consider using CDN for static assets'
            )
        }

    def _calculate_superman_network_score(self, results: Dict) -> Dict[str, Any]:
        """
        🦸 Calculate Superman's network performance score (0-100)

        Weighted scoring:
        - Critical path length (25%)
        - Blocking resources (25%)
        - Network bottlenecks (20%)
        - Performance budget (15%)
        - Timing phases (15%)

        Args:
            results: Network analysis results

        Returns:
            Superman network score
        """
        score = 100  # Start perfect

        # Critical path length (25%)
        critical_path_ms = results.get('critical_path', {}).get('critical_path_length_ms', 0)
        if critical_path_ms > 5000:
            score -= 25
        elif critical_path_ms > 3000:
            score -= 15
        elif critical_path_ms > 2000:
            score -= 10
        elif critical_path_ms > 1000:
            score -= 5

        # Blocking resources (25%)
        blocking_count = results.get('blocking_resources', {}).get('blocking_count', 0)
        critical_blocking = len(results.get('blocking_resources', {}).get('critical_blocking', []))

        if critical_blocking > 3:
            score -= 25
        elif critical_blocking > 1:
            score -= 15
        elif blocking_count > 5:
            score -= 10
        elif blocking_count > 2:
            score -= 5

        # Network bottlenecks (20%)
        critical_bottlenecks = len(results.get('bottlenecks', {}).get('critical_bottlenecks', []))
        high_bottlenecks = len(results.get('bottlenecks', {}).get('high_severity_bottlenecks', []))

        if critical_bottlenecks > 0:
            score -= 20
        elif high_bottlenecks > 2:
            score -= 15
        elif high_bottlenecks > 0:
            score -= 10

        # Performance budget (15%)
        budget_violations = results.get('performance_budget', {}).get('violation_count', 0)
        if budget_violations > 3:
            score -= 15
        elif budget_violations > 1:
            score -= 10
        elif budget_violations > 0:
            score -= 5

        # Timing phases (15%)
        timing = results.get('timing_phases', {}).get('phase_averages_ms', {})
        avg_wait = timing.get('wait', 0)

        if avg_wait > 600:
            score -= 15
        elif avg_wait > 300:
            score -= 10
        elif avg_wait > 200:
            score -= 5

        # Floor at 0
        score = max(0, score)

        # Determine grade and verdict
        if score >= 98:
            grade = "S+"
            verdict = "🦸 PERFECT NETWORK PERFORMANCE - Superman approved!"
        elif score >= 95:
            grade = "S"
            verdict = "🦸 OUTSTANDING network performance!"
        elif score >= 90:
            grade = "A+"
            verdict = "🦸 Excellent network performance!"
        elif score >= 85:
            grade = "A"
            verdict = "🦸 Very good network performance"
        elif score >= 80:
            grade = "B+"
            verdict = "🦸 Good network performance"
        elif score >= 75:
            grade = "B"
            verdict = "🦸 Acceptable network performance"
        elif score >= 70:
            grade = "C"
            verdict = "🦸 Network needs optimization"
        else:
            grade = "D"
            verdict = "🦸 Critical network issues - optimize immediately!"

        return {
            'score': score,
            'grade': grade,
            'verdict': verdict,
            'breakdown': {
                'critical_path_ms': critical_path_ms,
                'blocking_resources': blocking_count,
                'bottlenecks': len(results.get('bottlenecks', {}).get('bottlenecks', [])),
                'budget_violations': budget_violations,
                'avg_ttfb_ms': avg_wait
            }
        }

    def _generate_superman_network_recommendations(self, results: Dict) -> List[Dict]:
        """
        🦸 Generate Superman's network optimization recommendations

        Args:
            results: Network analysis results

        Returns:
            Prioritized recommendations
        """
        recommendations = []

        # Critical path recommendations
        critical_path_ms = results.get('critical_path', {}).get('critical_path_length_ms', 0)
        if critical_path_ms > 2000:
            recommendations.append({
                'priority': 'critical' if critical_path_ms > 4000 else 'high',
                'area': 'Critical Rendering Path',
                'issue': f'Critical path is {critical_path_ms:.0f}ms (target: <2000ms)',
                'superman_says': '🦸 Your critical path is blocking fast renders!',
                'actions': [
                    'Inline critical CSS',
                    'Defer non-critical JavaScript',
                    'Preload critical resources',
                    'Reduce critical resource count',
                    'Use resource hints (preconnect, dns-prefetch)'
                ]
            })

        # Blocking resource recommendations
        blocking = results.get('blocking_resources', {})
        critical_blocking = len(blocking.get('critical_blocking', []))

        if critical_blocking > 0 or blocking.get('blocking_count', 0) > 3:
            recommendations.append({
                'priority': 'critical' if critical_blocking > 2 else 'high',
                'area': 'Render Blocking Resources',
                'issue': f'{blocking.get("blocking_count")} blocking resources found',
                'superman_says': '🦸 Blocking resources are slowing your page!',
                'actions': [
                    'Add async or defer attributes to scripts',
                    'Extract and inline critical CSS',
                    'Use media queries for non-critical CSS',
                    'Font-display: swap for web fonts',
                    'Preload critical fonts'
                ]
            })

        # Bottleneck recommendations
        bottlenecks = results.get('bottlenecks', {}).get('bottlenecks', [])
        for bottleneck in bottlenecks:
            if bottleneck.get('severity') in ['critical', 'high']:
                recommendations.append({
                    'priority': bottleneck.get('severity', 'medium'),
                    'area': f'Network Bottleneck - {bottleneck["type"]}',
                    'issue': bottleneck['issue'],
                    'superman_says': bottleneck['superman_says'],
                    'actions': [bottleneck['fix']]
                })

        # Budget recommendations
        budget = results.get('performance_budget', {})
        for violation in budget.get('violations', []):
            recommendations.append({
                'priority': 'high' if violation['over_percent'] > 50 else 'medium',
                'area': 'Performance Budget',
                'issue': f'{violation["metric"]} over budget by {violation["over_percent"]:.0f}%',
                'superman_says': violation['superman_says'],
                'actions': [
                    'Audit and remove unnecessary resources',
                    'Compress and optimize assets',
                    'Implement lazy loading',
                    'Use code splitting'
                ]
            })

        # CDN recommendation
        cdn = results.get('cdn_analysis', {})
        if cdn.get('cdn_usage_percent', 0) < 40:
            recommendations.append({
                'priority': 'medium',
                'area': 'CDN Usage',
                'issue': f'Only {cdn.get("cdn_usage_percent", 0):.0f}% of resources use CDN',
                'superman_says': '🦸 Use CDN for better global performance!',
                'actions': [
                    'Move static assets to CDN',
                    'Use CDN for images, CSS, JS',
                    'Consider multi-CDN strategy',
                    'Enable CDN caching'
                ]
            })

        # Sort by priority
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 3))

        return recommendations

    def _get_default_budget(self) -> Dict[str, int]:
        """Get default performance budget"""
        return {
            'total_requests': 100,
            'total_size_kb': 2000,
            'scripts_kb': 500,
            'images_kb': 800,
            'css_kb': 200
        }

    def _store_baseline(self, test_name: str, results: Dict) -> None:
        """
        Store network analysis results as baseline

        Args:
            test_name: Test identifier
            results: Analysis results
        """
        baseline_file = self.baseline_dir / f"{test_name}_network_baseline.json"

        baseline_data = {
            'test_name': test_name,
            'timestamp': datetime.now().isoformat(),
            'url': results.get('url'),
            'superman_network_score': results.get('superman_network_score'),
            'critical_path': results.get('critical_path'),
            'blocking_resources': results.get('blocking_resources'),
            'performance_budget': results.get('performance_budget'),
            'bottlenecks': results.get('bottlenecks')
        }

        with open(baseline_file, 'w') as f:
            json.dump(baseline_data, f, indent=2)

        logger.info(f"  ✓ Network baseline stored: {baseline_file}")


# Main entry point - Superman's Network Analysis Mission
def analyze_network_timing_complete(
    mcp_tools: Dict,
    url: str,
    test_name: str = 'default',
    store_baseline: bool = True,
    performance_budget: Optional[Dict[str, int]] = None
) -> Dict[str, Any]:
    """
    🦸🌊 Superman's Complete Network Timing Analysis

    Enhances Aquaman with advanced network performance analysis!

    Args:
        mcp_tools: Dictionary of MCP tool functions
        url: URL being tested
        test_name: Test identifier for baselines
        store_baseline: Whether to store results as baseline
        performance_budget: Optional performance budget

    Returns:
        Complete network timing analysis with Superman enhancements

    Example:
        >>> results = analyze_network_timing_complete(
        ...     mcp_tools={'list_network_requests': mcp_func, ...},
        ...     url='https://example.com',
        ...     test_name='homepage',
        ...     performance_budget={'total_requests': 100, 'total_size_kb': 2000}
        ... )
        >>> print(f"Score: {results['superman_network_score']['score']}/100")
    """
    analyzer = SupermanNetworkAnalysis()
    return analyzer.analyze_network_complete(
        mcp_tools=mcp_tools,
        url=url,
        test_name=test_name,
        store_baseline=store_baseline,
        performance_budget=performance_budget
    )
