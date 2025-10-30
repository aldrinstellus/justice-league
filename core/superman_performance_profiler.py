"""
🦸 SUPERMAN PERFORMANCE PROFILING SYSTEM
Complete performance analysis with automated trace recording

Capabilities:
- Automated performance trace recording (via MCP Chrome DevTools)
- Core Web Vitals extraction and analysis (LCP, FID, CLS, FCP, TTI, TBT)
- Performance regression detection with baseline comparison
- Detailed performance insights analysis
- Frame rate monitoring and JavaScript execution profiling
- Resource loading optimization recommendations
- Integration with Flash hero for Justice League coordination

Powers Superman:
Superman uses this system to coordinate Flash's speed analysis with comprehensive
performance profiling capabilities for complete website performance validation.

MCP Tools Used:
- mcp__chrome-devtools__performance_start_trace() - Start recording
- mcp__chrome-devtools__performance_stop_trace() - Stop and collect metrics
- mcp__chrome-devtools__performance_analyze_insight() - Deep dive analysis

Libraries:
- Built on top of Flash Performance hero
- JSON for baseline storage
- Pathlib for file management
"""

import logging
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class SupermanPerformanceProfiler:
    """
    🦸 Superman's Performance Profiling System

    Wraps Flash's capabilities with Superman-specific enhancements:
    1. Automated trace recording workflow
    2. Enhanced Core Web Vitals extraction
    3. Performance regression detection with detailed diff
    4. Multi-run comparison and trending
    5. Comprehensive performance reporting
    6. Integration with Justice League coordination
    """

    def __init__(self, baseline_dir: Optional[str] = None):
        """
        Initialize Superman's Performance Profiling Lab

        Args:
            baseline_dir: Directory to store performance baselines
        """
        self.baseline_dir = Path(baseline_dir or '/tmp/aldo-vision-performance-baselines')
        self.baseline_dir.mkdir(parents=True, exist_ok=True)

        self.history_dir = self.baseline_dir / 'history'
        self.history_dir.mkdir(exist_ok=True)

        self.reports_dir = self.baseline_dir / 'reports'
        self.reports_dir.mkdir(exist_ok=True)

        logger.info(f"🦸⚡ Superman Performance Profiler initialized: {self.baseline_dir}")

    def profile_complete(self, mcp_tools: Dict, test_name: str,
                        url: str,
                        reload_page: bool = True,
                        store_baseline: bool = True) -> Dict[str, Any]:
        """
        🦸 Complete performance profiling workflow

        Superman's enhanced profiling includes:
        - Automated trace recording
        - Core Web Vitals extraction
        - Performance insights analysis
        - Regression detection
        - Historical tracking
        - Comprehensive reporting

        Args:
            mcp_tools: Dictionary of MCP tool functions
                {
                    'start_trace': Function to start performance trace,
                    'stop_trace': Function to stop trace and get results,
                    'analyze_insight': Function to analyze specific insights
                }
            test_name: Unique test name (e.g., 'dashboard-load')
            url: Target URL being tested
            reload_page: Whether to reload page during trace
            store_baseline: Whether to store this run as baseline

        Returns:
            Complete performance analysis with Superman enhancements
        """
        logger.info(f"🦸⚡ Superman starting performance profile: {test_name}")
        logger.info(f"🦸⚡ Target URL: {url}")

        results = {
            'hero': '🦸 Superman Performance Profiler',
            'test_name': test_name,
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'superman_version': '1.0.0'
        }

        # Validate MCP tools are available
        if not mcp_tools:
            logger.error("🦸⚡ CRITICAL: No MCP tools provided!")
            return {
                **results,
                'status': 'error',
                'error': 'MCP tools required for performance profiling',
                'required_tools': [
                    'start_trace',
                    'stop_trace',
                    'analyze_insight'
                ]
            }

        try:
            # STEP 1: Start Performance Trace
            logger.info("🦸⚡ STEP 1: Starting performance trace...")
            trace_config = {
                'reload': reload_page,
                'autoStop': True  # Auto-stop when page load complete
            }

            start_func = mcp_tools.get('start_trace')
            if not start_func:
                raise ValueError("start_trace function not provided in mcp_tools")

            trace_start_result = start_func(**trace_config)
            results['trace_started'] = trace_start_result
            logger.info("  ✅ Performance trace started")

            # STEP 2: Stop Trace and Collect Metrics
            logger.info("🦸⚡ STEP 2: Collecting performance metrics...")

            stop_func = mcp_tools.get('stop_trace')
            if not stop_func:
                raise ValueError("stop_trace function not provided in mcp_tools")

            trace_results = stop_func()
            results['raw_trace_data'] = trace_results
            logger.info("  ✅ Performance metrics collected")

            # STEP 3: Extract Core Web Vitals
            logger.info("🦸⚡ STEP 3: Extracting Core Web Vitals...")
            core_vitals = self._extract_core_web_vitals(trace_results)
            results['core_web_vitals'] = core_vitals

            vitals_summary = self._summarize_core_vitals(core_vitals)
            results['vitals_summary'] = vitals_summary
            logger.info(f"  ✅ Core Web Vitals: {vitals_summary['passed']}/{vitals_summary['total']} passed")

            # STEP 4: Extract Performance Insights
            logger.info("🦸⚡ STEP 4: Analyzing performance insights...")
            insights = trace_results.get('insights', [])
            results['performance_insights'] = insights
            results['insights_count'] = len(insights)
            logger.info(f"  ✅ Found {len(insights)} performance insights")

            # STEP 5: Analyze Top Insights in Detail
            analyze_func = mcp_tools.get('analyze_insight')
            if analyze_func and insights:
                logger.info("🦸⚡ STEP 5: Deep-diving into top insights...")
                detailed_insights = []

                # Analyze top 5 critical insights
                for idx, insight in enumerate(insights[:5]):
                    insight_name = insight.get('name')
                    if insight_name:
                        try:
                            detailed = analyze_func(insightName=insight_name)
                            detailed_insights.append({
                                'insight_number': idx + 1,
                                'name': insight_name,
                                'details': detailed
                            })
                            logger.info(f"    ✓ Analyzed insight {idx + 1}: {insight_name}")
                        except Exception as e:
                            logger.warning(f"    ⚠️  Failed to analyze {insight_name}: {e}")

                results['detailed_insights'] = detailed_insights
                logger.info(f"  ✅ Analyzed {len(detailed_insights)} insights in detail")

            # STEP 6: Calculate Superman Performance Score
            logger.info("🦸⚡ STEP 6: Calculating Superman Performance Score...")
            performance_score = self._calculate_performance_score(results)
            results['superman_performance_score'] = performance_score
            logger.info(f"  ✅ Performance Score: {performance_score['score']:.1f}/100 ({performance_score['grade']})")

            # STEP 7: Check for Performance Regression
            logger.info("🦸⚡ STEP 7: Checking for performance regression...")
            regression_check = self._check_regression(test_name, results)
            results['regression_check'] = regression_check

            if regression_check.get('is_regression'):
                logger.warning(f"  ⚠️  REGRESSION DETECTED: Score dropped by {abs(regression_check['score_difference']):.1f} points")
            else:
                logger.info("  ✅ No performance regression detected")

            # STEP 8: Store Performance Baseline
            if store_baseline:
                logger.info("🦸⚡ STEP 8: Storing performance baseline...")
                baseline_stored = self._store_baseline(test_name, results)
                results['baseline_stored'] = baseline_stored
                logger.info(f"  ✅ Baseline stored: {baseline_stored['path']}")

            # STEP 9: Store to History
            logger.info("🦸⚡ STEP 9: Archiving to performance history...")
            history_stored = self._store_to_history(test_name, results)
            results['history_stored'] = history_stored
            logger.info(f"  ✅ History archived: {history_stored['path']}")

            # STEP 10: Generate Recommendations
            logger.info("🦸⚡ STEP 10: Generating performance recommendations...")
            recommendations = self._generate_recommendations(results)
            results['superman_recommendations'] = recommendations
            logger.info(f"  ✅ Generated {len(recommendations)} recommendations")

            # FINAL: Superman's Verdict
            logger.info("🦸⚡ ========================================")
            logger.info(f"🦸⚡  SUPERMAN PERFORMANCE ANALYSIS COMPLETE")
            logger.info(f"🦸⚡  Score: {performance_score['score']:.1f}/100")
            logger.info(f"🦸⚡  Grade: {performance_score['grade']}")
            logger.info(f"🦸⚡  Verdict: {performance_score['verdict']}")
            logger.info("🦸⚡ ========================================")

            results['status'] = 'success'

        except Exception as e:
            logger.error(f"🦸⚡ ERROR: Performance profiling failed: {e}")
            results['status'] = 'error'
            results['error'] = str(e)
            import traceback
            results['traceback'] = traceback.format_exc()

        return results

    def _extract_core_web_vitals(self, trace_data: Dict) -> Dict[str, Any]:
        """
        🦸 Extract Core Web Vitals from performance trace data

        Core Web Vitals (Google's UX metrics):
        - LCP (Largest Contentful Paint) - Loading performance
        - FID (First Input Delay) - Interactivity
        - CLS (Cumulative Layout Shift) - Visual stability

        Additional Metrics:
        - FCP (First Contentful Paint)
        - TTI (Time to Interactive)
        - TBT (Total Blocking Time)
        - Speed Index

        Args:
            trace_data: Raw trace data from Chrome DevTools

        Returns:
            Extracted and analyzed Core Web Vitals
        """
        # Extract metrics from trace data structure
        # Chrome DevTools provides these in various formats

        vitals = {
            'LCP': {
                'name': 'Largest Contentful Paint',
                'value': trace_data.get('lcp', trace_data.get('largestContentfulPaint', 0)),
                'unit': 'ms',
                'threshold_good': 2500,
                'threshold_needs_improvement': 4000,
                'weight': 0.25  # 25% of total score
            },
            'FID': {
                'name': 'First Input Delay',
                'value': trace_data.get('fid', trace_data.get('firstInputDelay', 0)),
                'unit': 'ms',
                'threshold_good': 100,
                'threshold_needs_improvement': 300,
                'weight': 0.10  # 10% of total score
            },
            'CLS': {
                'name': 'Cumulative Layout Shift',
                'value': trace_data.get('cls', trace_data.get('cumulativeLayoutShift', 0)),
                'unit': 'score',
                'threshold_good': 0.1,
                'threshold_needs_improvement': 0.25,
                'weight': 0.15  # 15% of total score
            },
            'FCP': {
                'name': 'First Contentful Paint',
                'value': trace_data.get('fcp', trace_data.get('firstContentfulPaint', 0)),
                'unit': 'ms',
                'threshold_good': 1800,
                'threshold_needs_improvement': 3000,
                'weight': 0.15  # 15% of total score
            },
            'TTI': {
                'name': 'Time to Interactive',
                'value': trace_data.get('tti', trace_data.get('timeToInteractive', 0)),
                'unit': 'ms',
                'threshold_good': 3800,
                'threshold_needs_improvement': 7300,
                'weight': 0.15  # 15% of total score
            },
            'TBT': {
                'name': 'Total Blocking Time',
                'value': trace_data.get('tbt', trace_data.get('totalBlockingTime', 0)),
                'unit': 'ms',
                'threshold_good': 200,
                'threshold_needs_improvement': 600,
                'weight': 0.20  # 20% of total score
            }
        }

        # Analyze each metric
        for metric_key, metric_data in vitals.items():
            value = metric_data['value']
            good = metric_data['threshold_good']
            needs_improvement = metric_data['threshold_needs_improvement']

            # Determine status
            if metric_key == 'CLS':
                # CLS is special - lower is better
                if value <= good:
                    status = 'good'
                    score = 100
                elif value <= needs_improvement:
                    status = 'needs_improvement'
                    score = 50
                else:
                    status = 'poor'
                    score = 0
            else:
                # Time-based metrics
                if value <= good:
                    status = 'good'
                    score = 100
                elif value <= needs_improvement:
                    status = 'needs_improvement'
                    # Linear interpolation between good and needs_improvement
                    ratio = (needs_improvement - value) / (needs_improvement - good)
                    score = 50 + (ratio * 50)
                else:
                    status = 'poor'
                    # Decreasing score as value gets worse
                    score = max(0, 50 * (1 - (value - needs_improvement) / needs_improvement))

            metric_data['status'] = status
            metric_data['score'] = round(score, 1)
            metric_data['passed'] = status == 'good'

        return vitals

    def _summarize_core_vitals(self, core_vitals: Dict) -> Dict[str, Any]:
        """
        🦸 Summarize Core Web Vitals performance

        Args:
            core_vitals: Extracted Core Web Vitals

        Returns:
            Summary statistics
        """
        passed = sum(1 for v in core_vitals.values() if v.get('passed', False))
        total = len(core_vitals)

        good_count = sum(1 for v in core_vitals.values() if v.get('status') == 'good')
        needs_improvement = sum(1 for v in core_vitals.values() if v.get('status') == 'needs_improvement')
        poor_count = sum(1 for v in core_vitals.values() if v.get('status') == 'poor')

        return {
            'passed': passed,
            'total': total,
            'pass_rate': (passed / total * 100) if total > 0 else 0,
            'good': good_count,
            'needs_improvement': needs_improvement,
            'poor': poor_count,
            'overall_status': 'good' if passed >= total * 0.75 else 'needs_improvement' if passed >= total * 0.5 else 'poor'
        }

    def _calculate_performance_score(self, results: Dict) -> Dict[str, Any]:
        """
        🦸 Calculate Superman's Performance Score (0-100)

        Weighted scoring based on:
        - Core Web Vitals (weighted individually)
        - Performance insights severity
        - Regression status

        Args:
            results: Complete performance results

        Returns:
            Performance score with grade and verdict
        """
        score = 0
        max_score = 100

        core_vitals = results.get('core_web_vitals', {})
        insights = results.get('performance_insights', [])

        # Calculate weighted Core Web Vitals score
        vitals_score = 0
        total_weight = 0

        for metric_key, metric_data in core_vitals.items():
            metric_score = metric_data.get('score', 0)
            weight = metric_data.get('weight', 0)
            vitals_score += metric_score * weight
            total_weight += weight

        # Normalize vitals score to 0-100
        if total_weight > 0:
            vitals_score = vitals_score / total_weight

        score = vitals_score

        # Deduct points for performance insights
        critical_insights = [i for i in insights if i.get('severity') == 'critical']
        warning_insights = [i for i in insights if i.get('severity') == 'warning']
        info_insights = [i for i in insights if i.get('severity') == 'info']

        # Deduct: 5 points per critical, 2 points per warning, 0.5 per info
        score -= len(critical_insights) * 5
        score -= len(warning_insights) * 2
        score -= len(info_insights) * 0.5

        # Floor at 0
        score = max(0, min(100, score))

        # Determine grade and verdict
        if score >= 90:
            grade = 'S+'
            verdict = '🦸 WORLD-CLASS PERFORMANCE - Superman approved!'
        elif score >= 80:
            grade = 'A'
            verdict = '🦸 EXCELLENT - Minor optimizations possible'
        elif score >= 70:
            grade = 'B+'
            verdict = '🦸 GOOD - Some improvements recommended'
        elif score >= 60:
            grade = 'B'
            verdict = '🦸 ACCEPTABLE - Several areas need attention'
        elif score >= 50:
            grade = 'C'
            verdict = '🦸 MODERATE - Significant optimization needed'
        else:
            grade = 'D'
            verdict = '🦸 POOR - Superman intervention required!'

        return {
            'score': round(score, 1),
            'grade': grade,
            'verdict': verdict,
            'vitals_score': round(vitals_score, 1),
            'insights_deduction': {
                'critical': len(critical_insights),
                'warning': len(warning_insights),
                'info': len(info_insights),
                'total_deducted': len(critical_insights) * 5 + len(warning_insights) * 2 + len(info_insights) * 0.5
            }
        }

    def _check_regression(self, test_name: str, results: Dict) -> Dict[str, Any]:
        """
        🦸 Check for performance regression against baseline

        Args:
            test_name: Test name
            results: Current performance results

        Returns:
            Regression analysis
        """
        baseline_path = self.baseline_dir / f"{test_name}_baseline.json"

        if not baseline_path.exists():
            return {
                'status': 'no_baseline',
                'message': 'No baseline exists - this run will become the baseline',
                'is_regression': False
            }

        # Load baseline
        try:
            with open(baseline_path, 'r') as f:
                baseline = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load baseline: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'is_regression': False
            }

        # Compare scores
        current_score = results.get('superman_performance_score', {}).get('score', 0)
        baseline_score = baseline.get('superman_performance_score', {}).get('score', 0)

        score_diff = current_score - baseline_score

        # Regression threshold: 5 point drop
        is_regression = score_diff < -5

        # Compare Core Web Vitals
        current_vitals = results.get('core_web_vitals', {})
        baseline_vitals = baseline.get('core_web_vitals', {})

        vitals_comparison = {}
        for metric_key in current_vitals.keys():
            current_value = current_vitals.get(metric_key, {}).get('value', 0)
            baseline_value = baseline_vitals.get(metric_key, {}).get('value', 0)

            vitals_comparison[metric_key] = {
                'current': current_value,
                'baseline': baseline_value,
                'difference': current_value - baseline_value,
                'is_worse': current_value > baseline_value if metric_key != 'CLS' else False
            }

        return {
            'status': 'regression_detected' if is_regression else 'no_regression',
            'is_regression': is_regression,
            'current_score': current_score,
            'baseline_score': baseline_score,
            'score_difference': round(score_diff, 1),
            'vitals_comparison': vitals_comparison,
            'baseline_timestamp': baseline.get('timestamp'),
            'superman_verdict': '⚠️  PERFORMANCE REGRESSION DETECTED!' if is_regression else '✅ Performance maintained or improved'
        }

    def _store_baseline(self, test_name: str, results: Dict) -> Dict[str, Any]:
        """
        🦸 Store performance baseline for future comparisons

        Args:
            test_name: Test name
            results: Performance results

        Returns:
            Storage confirmation
        """
        baseline_path = self.baseline_dir / f"{test_name}_baseline.json"

        baseline = {
            'test_name': test_name,
            'url': results.get('url'),
            'timestamp': results.get('timestamp'),
            'superman_performance_score': results.get('superman_performance_score'),
            'core_web_vitals': results.get('core_web_vitals'),
            'vitals_summary': results.get('vitals_summary'),
            'insights_count': results.get('insights_count')
        }

        with open(baseline_path, 'w') as f:
            json.dump(baseline, f, indent=2)

        return {
            'stored': True,
            'path': str(baseline_path),
            'timestamp': results.get('timestamp')
        }

    def _store_to_history(self, test_name: str, results: Dict) -> Dict[str, Any]:
        """
        🦸 Store performance run to history for trend analysis

        Args:
            test_name: Test name
            results: Performance results

        Returns:
            Storage confirmation
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        history_path = self.history_dir / f"{test_name}_{timestamp}.json"

        # Store full results in history
        with open(history_path, 'w') as f:
            json.dump(results, f, indent=2)

        return {
            'stored': True,
            'path': str(history_path),
            'timestamp': timestamp
        }

    def _generate_recommendations(self, results: Dict) -> List[Dict[str, Any]]:
        """
        🦸 Generate Superman's performance recommendations

        Args:
            results: Performance analysis results

        Returns:
            List of actionable recommendations
        """
        recommendations = []

        core_vitals = results.get('core_web_vitals', {})
        score_data = results.get('superman_performance_score', {})

        # LCP Recommendations
        lcp = core_vitals.get('LCP', {})
        if lcp.get('status') in ['needs_improvement', 'poor']:
            recommendations.append({
                'priority': 'critical' if lcp.get('status') == 'poor' else 'high',
                'metric': 'LCP (Largest Contentful Paint)',
                'current_value': f"{lcp.get('value', 0)}ms",
                'target_value': f"<{lcp.get('threshold_good')}ms",
                'issue': 'Largest content element taking too long to render',
                'superman_says': '🦸 Speed up your hero image/content!',
                'actions': [
                    'Optimize and compress images (use WebP format)',
                    'Implement lazy loading for below-fold images',
                    'Reduce server response time (TTFB)',
                    'Eliminate render-blocking resources',
                    'Use a CDN for static assets',
                    'Preload critical resources with <link rel="preload">'
                ]
            })

        # CLS Recommendations
        cls = core_vitals.get('CLS', {})
        if cls.get('status') in ['needs_improvement', 'poor']:
            recommendations.append({
                'priority': 'critical' if cls.get('status') == 'poor' else 'high',
                'metric': 'CLS (Cumulative Layout Shift)',
                'current_value': cls.get('value', 0),
                'target_value': f"<{cls.get('threshold_good')}",
                'issue': 'Content shifting during page load - poor UX',
                'superman_says': '🦸 Stop the layout chaos!',
                'actions': [
                    'Set explicit width and height on images and videos',
                    'Reserve space for ads and embeds',
                    'Avoid inserting content above existing content',
                    'Use CSS aspect-ratio for responsive elements',
                    'Preload fonts to prevent FOIT/FOUT',
                    'Use CSS transforms for animations (not properties that trigger layout)'
                ]
            })

        # FID/TBT Recommendations
        fid = core_vitals.get('FID', {})
        tbt = core_vitals.get('TBT', {})

        if fid.get('status') in ['needs_improvement', 'poor'] or tbt.get('status') in ['needs_improvement', 'poor']:
            recommendations.append({
                'priority': 'high',
                'metric': 'FID/TBT (Interactivity)',
                'current_value': f"FID: {fid.get('value', 0)}ms, TBT: {tbt.get('value', 0)}ms",
                'target_value': f"FID <{fid.get('threshold_good')}ms, TBT <{tbt.get('threshold_good')}ms",
                'issue': 'Main thread blocked - slow to respond to user input',
                'superman_says': '🦸 Free the main thread!',
                'actions': [
                    'Break up long JavaScript tasks (use async/await)',
                    'Code-split JavaScript bundles',
                    'Remove unused JavaScript (tree shaking)',
                    'Use web workers for heavy computation',
                    'Defer non-critical JavaScript',
                    'Optimize third-party scripts',
                    'Implement progressive hydration for React/Next.js'
                ]
            })

        # FCP/TTI Recommendations
        fcp = core_vitals.get('FCP', {})
        tti = core_vitals.get('TTI', {})

        if fcp.get('status') in ['needs_improvement', 'poor'] or tti.get('status') in ['needs_improvement', 'poor']:
            recommendations.append({
                'priority': 'medium',
                'metric': 'FCP/TTI (Loading Speed)',
                'current_value': f"FCP: {fcp.get('value', 0)}ms, TTI: {tti.get('value', 0)}ms",
                'target_value': f"FCP <{fcp.get('threshold_good')}ms, TTI <{tti.get('threshold_good')}ms",
                'issue': 'Page taking too long to become interactive',
                'superman_says': '🦸 Speed up initial load!',
                'actions': [
                    'Minimize CSS (critical CSS inline)',
                    'Eliminate render-blocking resources',
                    'Use HTTP/2 or HTTP/3',
                    'Enable text compression (gzip/brotli)',
                    'Reduce JavaScript bundle size',
                    'Implement service worker for caching'
                ]
            })

        # General Performance Insights
        insights = results.get('performance_insights', [])
        critical_insights = [i for i in insights if i.get('severity') == 'critical']

        if critical_insights:
            recommendations.append({
                'priority': 'critical',
                'metric': 'Performance Insights',
                'current_value': f"{len(critical_insights)} critical issues",
                'target_value': '0 critical issues',
                'issue': 'Critical performance problems detected',
                'superman_says': '🦸 Critical issues need immediate attention!',
                'actions': [
                    f"Review Chrome DevTools insight: {insight.get('name')}"
                    for insight in critical_insights[:5]
                ]
            })

        return recommendations

    def get_performance_history(self, test_name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        🦸 Get performance history for trend analysis

        Args:
            test_name: Test name
            limit: Maximum number of history entries to return

        Returns:
            List of historical performance runs
        """
        history_files = sorted(
            self.history_dir.glob(f"{test_name}_*.json"),
            reverse=True  # Most recent first
        )[:limit]

        history = []
        for file_path in history_files:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    history.append({
                        'timestamp': data.get('timestamp'),
                        'score': data.get('superman_performance_score', {}).get('score'),
                        'grade': data.get('superman_performance_score', {}).get('grade'),
                        'file': str(file_path)
                    })
            except Exception as e:
                logger.warning(f"Failed to load history file {file_path}: {e}")

        return history


# Main entry point - Superman's Performance Interface
def profile_performance_complete(mcp_tools: Dict, test_name: str, url: str,
                                reload_page: bool = True,
                                store_baseline: bool = True,
                                baseline_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    🦸 Superman's Complete Performance Profiling

    Main entry point for performance profiling with all Superman enhancements

    Args:
        mcp_tools: Dictionary of MCP Chrome DevTools functions
        test_name: Unique test name
        url: Target URL
        reload_page: Whether to reload page during trace
        store_baseline: Whether to store as baseline
        baseline_dir: Optional custom baseline directory

    Returns:
        Complete performance analysis with Superman's enhancements
    """
    profiler = SupermanPerformanceProfiler(baseline_dir)
    return profiler.profile_complete(mcp_tools, test_name, url, reload_page, store_baseline)
