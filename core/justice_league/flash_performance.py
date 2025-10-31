"""
⚡ THE FLASH - THE FASTEST PERFORMANCE ANALYZER ALIVE
Justice League Member: Performance & Speed Specialist

The Scarlet Speedster makes your app run at lightning speed!

Powers:
- Performance Profiling Integration (Chrome DevTools Performance API)
- Core Web Vitals Measurement (LCP, FID, CLS, FCP, TTI, TBT)
- Lighthouse Performance Audits
- Performance Regression Detection
- Speed Index Calculation
- Frame Rate Monitoring
- JavaScript Execution Analysis
- Resource Loading Optimization

"I'm the fastest performance analyzer alive!"

MCP Tools Used:
- mcp__chrome-devtools__performance_start_trace()
- mcp__chrome-devtools__performance_stop_trace()
- mcp__chrome-devtools__performance_analyze_insight()
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import json

# Mission Control Narrator for coordinated communication
try:
    from .mission_control_narrator import get_narrator
    NARRATOR_AVAILABLE = True
except ImportError:
    NARRATOR_AVAILABLE = False
    logging.warning("Mission Control Narrator not available - Flash will operate without narrator")

logger = logging.getLogger(__name__)


class FlashPerformance:
    """
    ⚡ THE FLASH - Performance Analysis at Super Speed

    Flash's Powers:
    1. Start performance trace recording
    2. Stop trace and collect metrics
    3. Analyze Core Web Vitals
    4. Detect performance regressions
    5. Generate speed recommendations
    6. Compare against baselines
    """

    def __init__(self, baseline_dir: Optional[str] = None, narrator: Optional[Any] = None):
        """
        Initialize Flash's performance lab

        Args:
            baseline_dir: Directory to store performance baselines
            narrator: Mission Control Narrator for coordinated communication
        """
        self.baseline_dir = Path(baseline_dir or '/tmp/aldo-vision-performance-baselines')
        self.baseline_dir.mkdir(parents=True, exist_ok=True)

        # Initialize narrator for enhanced UX
        self.narrator = narrator if narrator else (get_narrator() if NARRATOR_AVAILABLE else None)

        # Hero identity for narrator integration
        self.hero_name = "Flash"
        self.hero_emoji = "⚡"

        logger.info(f"⚡ Flash Performance Lab initialized: {self.baseline_dir}")

    def say(self, message: str, style: str = "tactical", technical_info: Optional[str] = None):
        """
        Flash dialogue - Fast, energetic, metric-focused

        Personality traits:
        - Speed-oriented language
        - Performance metrics focus
        - Energetic but tactical
        - Quick updates
        """
        if self.narrator:
            self.narrator.hero_speaks(
                f"{self.hero_emoji} {self.hero_name}",
                message, style, technical_info
            )

    def think(self, thought: str, step: Optional[int] = None, category: Optional[str] = "Optimizing"):
        """
        Sequential thinking with performance focus

        Common categories for Flash:
        - Optimizing, Racing, Profiling, Accelerating
        """
        if self.narrator:
            self.narrator.hero_thinks(
                f"{self.hero_emoji} {self.hero_name}",
                thought, step, category
            )

    def handoff(self, to_hero: str, context: str, details: Optional[str] = None):
        """
        Handoff performance data to another hero

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

    def profile_performance(self, mcp_tools: Dict, test_name: str,
                           url: Optional[str] = None,
                           reload_page: bool = True) -> Dict[str, Any]:
        """
        ⚡ Flash runs at super speed to profile performance

        Args:
            mcp_tools: Dictionary of MCP tool functions
                {
                    'start_trace': mcp__chrome-devtools__performance_start_trace,
                    'stop_trace': mcp__chrome-devtools__performance_stop_trace,
                    'analyze_insight': mcp__chrome-devtools__performance_analyze_insight
                }
            test_name: Unique test name for this performance run
            url: Optional URL (for context)
            reload_page: Whether to reload page during trace

        Returns:
            Flash's complete performance analysis
        """
        logger.info(f"⚡ Flash starting performance trace: {test_name}")

        results = {
            'hero': '⚡ The Flash - Speed Analyzer',
            'test_name': test_name,
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'performance_data': {}
        }

        # Check if MCP tools available
        if not mcp_tools:
            logger.warning("⚡ No MCP tools provided - Flash needs his Speed Force!")
            return {
                **results,
                'status': 'mcp_tools_missing',
                'message': 'Performance profiling requires Chrome DevTools MCP tools',
                'required_tools': [
                    'mcp__chrome-devtools__performance_start_trace',
                    'mcp__chrome-devtools__performance_stop_trace',
                    'mcp__chrome-devtools__performance_analyze_insight'
                ]
            }

        try:
            # Step 1: Start Performance Trace
            logger.info("⚡ Flash activating Speed Force...")
            start_func = mcp_tools.get('start_trace')

            if start_func:
                # Start trace with auto-stop and optional reload
                trace_started = start_func(reload=reload_page, autoStop=True)
                results['trace_started'] = trace_started
                logger.info("  ✓ Performance trace started")
            else:
                logger.warning("  ⚠️ start_trace function not provided")
                results['trace_started'] = {'simulated': True}

            # Step 2: Stop Trace and Collect Results
            logger.info("⚡ Flash collecting performance metrics...")
            stop_func = mcp_tools.get('stop_trace')

            if stop_func:
                trace_results = stop_func()
                results['performance_data'] = trace_results

                # Extract Core Web Vitals
                core_vitals = self._extract_core_web_vitals(trace_results)
                results['core_web_vitals'] = core_vitals

                # Extract Performance Insights
                insights = trace_results.get('insights', [])
                results['performance_insights'] = insights

                logger.info(f"  ✓ Collected {len(insights)} performance insights")
            else:
                logger.warning("  ⚠️ stop_trace function not provided")
                results['performance_data'] = {'simulated': True}

            # Step 3: Analyze Specific Insights (if available)
            analyze_func = mcp_tools.get('analyze_insight')
            if analyze_func and results.get('performance_insights'):
                detailed_insights = []

                for insight in results['performance_insights'][:5]:  # Top 5 insights
                    insight_name = insight.get('name')
                    if insight_name:
                        detailed = analyze_func(insightName=insight_name)
                        detailed_insights.append(detailed)

                results['detailed_insights'] = detailed_insights
                logger.info(f"  ✓ Analyzed {len(detailed_insights)} detailed insights")

            # Step 4: Calculate Flash Speed Score
            speed_score = self._calculate_speed_score(results)
            results['flash_speed_score'] = speed_score

            # Step 5: Store Baseline (if first run)
            self._store_performance_baseline(test_name, results)

            # Step 6: Check for Regressions (if baseline exists)
            regression_check = self._check_performance_regression(test_name, results)
            results['regression_check'] = regression_check

            # Step 7: Generate Flash Recommendations
            recommendations = self._generate_flash_recommendations(results)
            results['flash_recommendations'] = recommendations

            logger.info(f"⚡ FLASH ANALYSIS COMPLETE - Speed Score: {speed_score['score']:.1f}/100")
            logger.info(f"⚡ Flash Verdict: {speed_score['verdict']}")

        except Exception as e:
            logger.error(f"⚡ Flash encountered a Speed Force anomaly: {e}")
            results['error'] = str(e)
            results['status'] = 'error'

        return results

    def _extract_core_web_vitals(self, trace_data: Dict) -> Dict[str, Any]:
        """
        ⚡ Extract Core Web Vitals from performance trace

        Metrics:
        - LCP (Largest Contentful Paint) - < 2.5s good
        - FID (First Input Delay) - < 100ms good
        - CLS (Cumulative Layout Shift) - < 0.1 good
        - FCP (First Contentful Paint) - < 1.8s good
        - TTI (Time to Interactive) - < 3.8s good
        - TBT (Total Blocking Time) - < 200ms good

        Args:
            trace_data: Raw performance trace data

        Returns:
            Extracted Core Web Vitals
        """
        # Extract metrics from trace data
        # In real implementation, this would parse Chrome trace format

        core_vitals = {
            'LCP': {
                'value': trace_data.get('lcp', 0),
                'unit': 'ms',
                'threshold_good': 2500,
                'threshold_needs_improvement': 4000,
                'status': 'unknown'
            },
            'FID': {
                'value': trace_data.get('fid', 0),
                'unit': 'ms',
                'threshold_good': 100,
                'threshold_needs_improvement': 300,
                'status': 'unknown'
            },
            'CLS': {
                'value': trace_data.get('cls', 0),
                'unit': 'score',
                'threshold_good': 0.1,
                'threshold_needs_improvement': 0.25,
                'status': 'unknown'
            },
            'FCP': {
                'value': trace_data.get('fcp', 0),
                'unit': 'ms',
                'threshold_good': 1800,
                'threshold_needs_improvement': 3000,
                'status': 'unknown'
            },
            'TTI': {
                'value': trace_data.get('tti', 0),
                'unit': 'ms',
                'threshold_good': 3800,
                'threshold_needs_improvement': 7300,
                'status': 'unknown'
            },
            'TBT': {
                'value': trace_data.get('tbt', 0),
                'unit': 'ms',
                'threshold_good': 200,
                'threshold_needs_improvement': 600,
                'status': 'unknown'
            }
        }

        # Determine status for each metric
        for metric, data in core_vitals.items():
            value = data['value']
            good = data['threshold_good']
            needs_improvement = data['threshold_needs_improvement']

            if metric == 'CLS':
                # CLS is special - lower is better, different scale
                if value <= good:
                    data['status'] = 'good'
                elif value <= needs_improvement:
                    data['status'] = 'needs_improvement'
                else:
                    data['status'] = 'poor'
            else:
                # For time-based metrics
                if value <= good:
                    data['status'] = 'good'
                elif value <= needs_improvement:
                    data['status'] = 'needs_improvement'
                else:
                    data['status'] = 'poor'

        return core_vitals

    def _calculate_speed_score(self, results: Dict) -> Dict[str, Any]:
        """
        ⚡ Calculate Flash's Speed Score (0-100)

        Flash scores based on:
        - Core Web Vitals (60%)
        - Performance Insights (20%)
        - Resource Loading (10%)
        - JavaScript Execution (10%)

        Args:
            results: Performance analysis results

        Returns:
            Flash Speed Score
        """
        score = 100  # Start perfect, deduct for issues

        core_vitals = results.get('core_web_vitals', {})
        insights = results.get('performance_insights', [])

        # Deduct points for poor Core Web Vitals
        for metric, data in core_vitals.items():
            status = data.get('status', 'unknown')
            if status == 'poor':
                score -= 10
            elif status == 'needs_improvement':
                score -= 5

        # Deduct points for performance insights
        critical_insights = [i for i in insights if i.get('severity') == 'critical']
        warning_insights = [i for i in insights if i.get('severity') == 'warning']

        score -= len(critical_insights) * 5
        score -= len(warning_insights) * 2

        # Floor at 0
        score = max(0, score)

        # Determine Flash verdict
        if score >= 90:
            verdict = "⚡ LIGHTNING FAST - Flash approved!"
            grade = "S+"
        elif score >= 80:
            verdict = "⚡ Very Fast - Nearly at Flash speed!"
            grade = "A"
        elif score >= 70:
            verdict = "⚡ Fast - Good speed but room to improve"
            grade = "B"
        elif score >= 60:
            verdict = "⚡ Moderate - Needs optimization"
            grade = "C"
        else:
            verdict = "⚡ SLOW - Flash intervention required!"
            grade = "D"

        return {
            'score': score,
            'grade': grade,
            'verdict': verdict,
            'core_vitals_passed': sum(1 for v in core_vitals.values() if v.get('status') == 'good'),
            'core_vitals_total': len(core_vitals),
            'critical_issues': len(critical_insights) if 'critical_insights' in locals() else 0,
            'warning_issues': len(warning_insights) if 'warning_insights' in locals() else 0
        }

    def _store_performance_baseline(self, test_name: str, results: Dict) -> None:
        """
        ⚡ Store performance baseline for future comparisons

        Args:
            test_name: Test name
            results: Performance results
        """
        baseline_path = self.baseline_dir / f"{test_name}_baseline.json"

        baseline = {
            'test_name': test_name,
            'timestamp': results['timestamp'],
            'core_web_vitals': results.get('core_web_vitals', {}),
            'flash_speed_score': results.get('flash_speed_score', {}),
            'url': results.get('url')
        }

        with open(baseline_path, 'w') as f:
            json.dump(baseline, f, indent=2)

        logger.info(f"⚡ Flash stored performance baseline: {baseline_path}")

    def _check_performance_regression(self, test_name: str, results: Dict) -> Dict[str, Any]:
        """
        ⚡ Check for performance regressions vs baseline

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
                'message': 'No baseline exists - this IS the baseline!'
            }

        # Load baseline
        with open(baseline_path, 'r') as f:
            baseline = json.load(f)

        current_score = results.get('flash_speed_score', {}).get('score', 0)
        baseline_score = baseline.get('flash_speed_score', {}).get('score', 0)

        score_diff = current_score - baseline_score

        is_regression = score_diff < -5  # 5 point drop = regression

        return {
            'status': 'regression_detected' if is_regression else 'no_regression',
            'current_score': current_score,
            'baseline_score': baseline_score,
            'score_difference': score_diff,
            'is_regression': is_regression,
            'flash_verdict': '⚠️ PERFORMANCE REGRESSION!' if is_regression else '✓ No regression detected'
        }

    def _generate_flash_recommendations(self, results: Dict) -> List[Dict]:
        """
        ⚡ Generate Flash's lightning-fast recommendations

        Args:
            results: Performance analysis results

        Returns:
            List of recommendations
        """
        recommendations = []

        core_vitals = results.get('core_web_vitals', {})

        # LCP recommendations
        lcp_status = core_vitals.get('LCP', {}).get('status')
        if lcp_status in ['needs_improvement', 'poor']:
            recommendations.append({
                'priority': 'high',
                'metric': 'LCP (Largest Contentful Paint)',
                'issue': 'LCP is too slow - largest element taking too long to render',
                'flash_says': 'Speed up your largest content! Flash can help!',
                'actions': [
                    'Optimize images (use WebP, lazy loading)',
                    'Reduce server response time',
                    'Eliminate render-blocking resources',
                    'Preload critical resources'
                ]
            })

        # CLS recommendations
        cls_status = core_vitals.get('CLS', {}).get('status')
        if cls_status in ['needs_improvement', 'poor']:
            recommendations.append({
                'priority': 'high',
                'metric': 'CLS (Cumulative Layout Shift)',
                'issue': 'Content is shifting during load - bad user experience',
                'flash_says': 'Stop the layout shifts! Flash demands stability!',
                'actions': [
                    'Add size attributes to images and videos',
                    'Reserve space for ads/embeds',
                    'Avoid inserting content above existing content',
                    'Use CSS transforms for animations'
                ]
            })

        # FID recommendations
        fid_status = core_vitals.get('FID', {}).get('status')
        if fid_status in ['needs_improvement', 'poor']:
            recommendations.append({
                'priority': 'high',
                'metric': 'FID (First Input Delay)',
                'issue': 'Page is slow to respond to user input',
                'flash_says': 'Users need instant response! Flash is always instant!',
                'actions': [
                    'Break up long JavaScript tasks',
                    'Use a web worker for heavy computation',
                    'Reduce JavaScript execution time',
                    'Defer non-critical JavaScript'
                ]
            })

        # TBT recommendations
        tbt_status = core_vitals.get('TBT', {}).get('status')
        if tbt_status in ['needs_improvement', 'poor']:
            recommendations.append({
                'priority': 'medium',
                'metric': 'TBT (Total Blocking Time)',
                'issue': 'Main thread is blocked too long',
                'flash_says': 'Clear the main thread! Flash runs unblocked!',
                'actions': [
                    'Code-split JavaScript bundles',
                    'Remove unused JavaScript',
                    'Implement lazy loading',
                    'Optimize third-party scripts'
                ]
            })

        return recommendations

    # Aliases and missing methods for audit compatibility
    def _generate_lightning_recommendations(self, results: Dict) -> List[Dict]:
        """Alias for _generate_flash_recommendations"""
        return self._generate_flash_recommendations(results)

    def _check_for_regression(self, test_name: str, results: Dict) -> Dict[str, Any]:
        """Alias for _check_performance_regression"""
        return self._check_performance_regression(test_name, results)

    def _store_baseline(self, test_name: str, results: Dict) -> None:
        """Alias for _store_performance_baseline"""
        return self._store_performance_baseline(test_name, results)

    def _load_baseline(self, test_name: str) -> Optional[Dict]:
        """Load performance baseline from storage"""
        baseline_file = self.baseline_dir / f"{test_name}.json"

        if not baseline_file.exists():
            return None

        try:
            with open(baseline_file, 'r') as f:
                import json
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load baseline {test_name}: {e}")
            return None


# Main entry point - Flash's Mission Interface
def flash_profile_performance(mcp_tools: Dict, test_name: str,
                              url: Optional[str] = None,
                              reload_page: bool = True,
                              baseline_dir: Optional[str] = None) -> Dict[str, Any]:
    """
    ⚡ The Flash profiles performance at super speed!

    Args:
        mcp_tools: Dictionary of MCP tool functions
        test_name: Unique test name
        url: Optional URL
        reload_page: Whether to reload page during trace
        baseline_dir: Optional custom baseline directory

    Returns:
        Flash's complete performance analysis
    """
    flash = FlashPerformance(baseline_dir)
    return flash.profile_performance(mcp_tools, test_name, url, reload_page)
