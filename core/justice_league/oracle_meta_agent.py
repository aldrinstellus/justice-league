"""
🔮 ORACLE - THE META-AGENT
Justice League Member: Knowledge Keeper, System Architect & Continuous Improvement Engine

Barbara Gordon's Oracle - Master of Information, Self-Healing, and Evolution

Powers:
- 📚 Knowledge Management - Never forget any error or solution
- 🧠 Continuous Learning - Get smarter with every mission
- 🔧 Self-Healing - Detect and fix issues automatically (semi-autonomous)
- 📊 Performance Monitoring - Track all agent metrics
- 🔄 Version Control - Manage agent versions, rollback capability
- 🔮 Predictive Maintenance - Predict failures before they occur
- 🔌 MCP Integration - Monitor and integrate MCP server updates
- 🧪 Automated Testing - Generate and run tests for all changes

"I see everything. I know everything. I improve everything." - Oracle

Architecture: SQLite knowledge base + Pattern recognition + ML predictions
Integration: Works with all heroes, coordinates with Superman
"""

import logging
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path
import hashlib
import subprocess

# Import Mission Control Narrator (v2.0)
try:
    from .mission_control_narrator import get_narrator
    NARRATOR_AVAILABLE = True
except ImportError:
    NARRATOR_AVAILABLE = False
    logging.warning("Mission Control Narrator not available for Oracle")

# Import strategic thinking
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from superman_strategic_thinking import SupermanStrategicThinking
    STRATEGIC_THINKING_AVAILABLE = True
except ImportError:
    STRATEGIC_THINKING_AVAILABLE = False
    logging.warning("Strategic thinking not available for Oracle")

logger = logging.getLogger(__name__)


class OracleMeta:
    """
    🔮 ORACLE - The Meta-Agent

    Barbara Gordon's Oracle serves as the Justice League's:
    - Information hub and knowledge keeper
    - System architect and code quality guardian
    - Self-healing engine with predictive capabilities
    - MCP integration manager
    - Continuous improvement coordinator
    - Strategic reasoning advisor (NEW!)

    Powers:
    1. Strategic Reasoning - Think through patterns before storing (NEW!)
    2. Knowledge Management - Store all errors, solutions, patterns
    3. Learning Engine - Learn from every mission, improve agents
    4. Self-Healing - Detect issues, propose fixes (require approval)
    5. Performance Monitoring - Track metrics, optimize performance
    6. Version Control - Manage versions, enable rollback
    7. Predictive Maintenance - Predict and prevent failures
    8. MCP Integration - Monitor and integrate MCP servers
    9. Testing Pipeline - Generate and validate tests

    "I see everything. I know everything. I think strategically." - Oracle
    """

    def __init__(self, knowledge_base_dir: Optional[str] = None, narrator: Optional[Any] = None):
        """
        Initialize Oracle's information network

        Args:
            knowledge_base_dir: Directory for knowledge base storage
            narrator: Optional MissionControlNarrator for enhanced UX
        """
        self.knowledge_base_dir = Path(knowledge_base_dir) if knowledge_base_dir else Path('/tmp/aldo-vision-justice-league/oracle')
        self.knowledge_base_dir.mkdir(parents=True, exist_ok=True)

        # Mission Control Narrator (v2.0)
        self.narrator = narrator if narrator else (get_narrator() if NARRATOR_AVAILABLE else None)

        # Knowledge base files
        self.errors_db = self.knowledge_base_dir / 'errors_solutions.json'
        self.patterns_db = self.knowledge_base_dir / 'patterns.json'
        self.metrics_db = self.knowledge_base_dir / 'agent_metrics.json'
        self.mcp_db = self.knowledge_base_dir / 'mcp_capabilities.json'
        self.best_practices_db = self.knowledge_base_dir / 'best_practices.json'
        self.versions_db = self.knowledge_base_dir / 'agent_versions.json'

        # Project-level pattern tracking (NEW - for cross-component patterns)
        self.project_patterns_db = Path('/Users/admin/Documents/claudecode/Projects/aldo-vision/data/oracle_project_patterns.json')
        self.shared_components_db = Path('/Users/admin/Documents/claudecode/Projects/aldo-vision/data/oracle_shared_components.json')

        # Initialize databases
        self._init_databases()

        # Current agent versions
        self.agent_versions = self._load_agent_versions()

        # Performance thresholds
        self.performance_thresholds = {
            'success_rate_min': 0.95,  # 95% minimum success rate
            'response_time_max': 5000,  # 5 seconds max response time
            'error_rate_max': 0.05  # 5% maximum error rate
        }

        # MCP servers to monitor
        self.mcp_servers = [
            'claude-code-sdk',
            'figma-mcp',
            'penpot-mcp',
            'chrome-devtools-mcp',
            'brightdata-mcp',
            'sequential-thinking-mcp'
        ]

        # Strategic thinking engine (NEW!)
        if STRATEGIC_THINKING_AVAILABLE:
            self.strategic_thinking = SupermanStrategicThinking(
                knowledge_base=None,  # Oracle has its own KB
                max_thoughts=8,
                verbose=False  # Oracle thinks silently
            )
            logger.info("🔮 ORACLE - Strategic Thinking: Enabled")
        else:
            self.strategic_thinking = None
            logger.info("🔮 ORACLE - Strategic Thinking: Disabled (module not available)")

        logger.info("🔮 ORACLE - Meta-Agent initialized")
        logger.info(f"🔮 Knowledge Base: {self.knowledge_base_dir}")
        logger.info(f"🔮 Monitoring {len(self.mcp_servers)} MCP servers")

    def _init_databases(self):
        """Initialize all knowledge base databases"""
        databases = [
            (self.errors_db, {'errors': [], 'solutions': [], 'error_solution_map': {}}),
            (self.patterns_db, {'patterns': [], 'trends': []}),
            (self.metrics_db, {'agents': {}}),
            (self.mcp_db, {'servers': {}}),
            (self.best_practices_db, {'practices': []}),
            (self.versions_db, {'agents': {}})
        ]

        for db_file, default_data in databases:
            if not db_file.exists():
                with open(db_file, 'w') as f:
                    json.dump(default_data, f, indent=2)

    def _load_agent_versions(self) -> Dict[str, str]:
        """Load current agent versions"""
        with open(self.versions_db, 'r') as f:
            data = json.load(f)
            return data.get('agents', {})

    def _save_agent_versions(self):
        """Save agent versions to database"""
        with open(self.versions_db, 'w') as f:
            json.dump({'agents': self.agent_versions}, f, indent=2)

    # ==================== KNOWLEDGE MANAGEMENT ====================

    def store_error_solution(self,
                            agent_name: str,
                            error_type: str,
                            error_details: Dict[str, Any],
                            solution: str,
                            context: Dict[str, Any]) -> str:
        """
        🔮 Store an error and its solution in knowledge base

        Args:
            agent_name: Name of agent that encountered error
            error_type: Type of error (timeout, validation, api_error, etc.)
            error_details: Detailed error information
            solution: Solution that fixed the error
            context: Context in which error occurred

        Returns:
            Error ID for future reference
        """
        error_id = f"ERR-{hashlib.md5(f'{agent_name}{error_type}{datetime.now()}'.encode()).hexdigest()[:8].upper()}"

        error_record = {
            'id': error_id,
            'agent': agent_name,
            'error_type': error_type,
            'error_details': error_details,
            'solution': solution,
            'context': context,
            'timestamp': datetime.now().isoformat(),
            'times_encountered': 1,
            'success_rate': 1.0  # Initial success rate
        }

        # Load existing errors
        with open(self.errors_db, 'r') as f:
            data = json.load(f)

        # Check if similar error exists
        similar_error = self._find_similar_error(agent_name, error_type, error_details, data['errors'])

        if similar_error:
            # Update existing error
            similar_error['times_encountered'] += 1
            similar_error['last_seen'] = datetime.now().isoformat()
            logger.info(f"🔮 Updated existing error: {similar_error['id']}")
        else:
            # Add new error
            data['errors'].append(error_record)
            logger.info(f"🔮 Stored new error: {error_id}")

        # Save back to database
        with open(self.errors_db, 'w') as f:
            json.dump(data, f, indent=2)

        # Analyze for patterns
        self._analyze_error_patterns(agent_name, error_type)

        return error_id

    def _find_similar_error(self, agent_name: str, error_type: str, error_details: Dict, existing_errors: List) -> Optional[Dict]:
        """Find similar error in database"""
        for error in existing_errors:
            if (error['agent'] == agent_name and
                error['error_type'] == error_type and
                self._errors_are_similar(error['error_details'], error_details)):
                return error
        return None

    def _errors_are_similar(self, error1: Dict, error2: Dict) -> bool:
        """Check if two errors are similar enough to be considered the same"""
        # Simple similarity check - can be enhanced with ML
        error1_str = json.dumps(error1, sort_keys=True)
        error2_str = json.dumps(error2, sort_keys=True)

        # If 80% of content is similar, consider them the same
        matching_chars = sum(1 for a, b in zip(error1_str, error2_str) if a == b)
        similarity = matching_chars / max(len(error1_str), len(error2_str))

        return similarity > 0.8

    def query_error_solutions(
        self,
        error: Dict[str, Any],
        min_similarity: float = 0.8
    ) -> List[Dict[str, Any]]:
        """
        🔮 Query error solutions from knowledge base for auto-fix

        Args:
            error: Error dict with 'type', 'message', 'context'
            min_similarity: Minimum similarity threshold (default: 0.8)

        Returns:
            List of matching error-solution pairs sorted by confidence
        """
        # Check if error recovery patterns exist in Oracle's knowledge base
        if not self.project_patterns_db.exists():
            return []

        try:
            with open(self.project_patterns_db, 'r') as f:
                patterns = json.load(f)

            # Check error_recovery_patterns section
            recovery_patterns = patterns.get('error_recovery_patterns', {})

            # Match error type to known patterns
            error_type = error.get('type', '').lower()
            error_msg = str(error.get('message', '')).lower()

            matches = []

            for pattern_key, pattern_data in recovery_patterns.items():
                # Check if this pattern matches the error
                problem = pattern_data.get('problem', {})
                pattern_symptom = problem.get('symptom', '').lower()
                pattern_context = problem.get('context', '').lower()

                # Calculate similarity
                similarity = 0.0

                if error_type in pattern_symptom or pattern_symptom in error_msg:
                    similarity += 0.5

                if pattern_context in error_msg or any(keyword in error_msg for keyword in pattern_context.split()):
                    similarity += 0.3

                # Check error recovery patterns from file
                if similarity >= min_similarity or error_type == pattern_data.get('pattern_type', ''):
                    matches.append({
                        'pattern': pattern_key,
                        'solution': pattern_data.get('solution', {}),
                        'confidence': pattern_data.get('confidence_score', similarity),
                        'similarity': similarity,
                        'reusable_for': pattern_data.get('reusable_for', [])
                    })

            # Sort by confidence (highest first)
            matches.sort(key=lambda x: x['confidence'], reverse=True)

            return matches

        except Exception as e:
            logger.warning(f"🔮 Error querying knowledge base: {e}")
            return []

    def reinforce_solution(
        self,
        error: Dict[str, Any],
        solution: Dict[str, Any],
        success: bool
    ):
        """
        🔮 Reinforce or penalize solution confidence based on outcome

        Args:
            error: The error that occurred
            solution: The solution that was applied
            success: Whether the solution worked

        Updates confidence scores in knowledge base for learning
        """
        try:
            if not self.project_patterns_db.exists():
                return

            with open(self.project_patterns_db, 'r') as f:
                patterns = json.load(f)

            recovery_patterns = patterns.get('error_recovery_patterns', {})

            # Find matching pattern
            for pattern_key, pattern_data in recovery_patterns.items():
                if pattern_data.get('solution') == solution:
                    current_confidence = pattern_data.get('confidence_score', 0.5)

                    # Reinforce or penalize
                    if success:
                        # Increase confidence (max 1.0)
                        new_confidence = min(1.0, current_confidence + 0.05)
                        logger.info(f"🔮 Oracle: Reinforcing solution confidence: {current_confidence:.2f} → {new_confidence:.2f}")
                    else:
                        # Decrease confidence (min 0.0)
                        new_confidence = max(0.0, current_confidence - 0.1)
                        logger.info(f"🔮 Oracle: Penalizing solution confidence: {current_confidence:.2f} → {new_confidence:.2f}")

                    pattern_data['confidence_score'] = new_confidence

                    # Update last used timestamp
                    pattern_data['last_used'] = datetime.now().isoformat()

                    # Track success/failure count
                    if 'usage_stats' not in pattern_data:
                        pattern_data['usage_stats'] = {
                            'total_attempts': 0,
                            'successful': 0,
                            'failed': 0
                        }

                    pattern_data['usage_stats']['total_attempts'] += 1
                    if success:
                        pattern_data['usage_stats']['successful'] += 1
                    else:
                        pattern_data['usage_stats']['failed'] += 1

                    # Calculate success rate
                    total = pattern_data['usage_stats']['total_attempts']
                    successful = pattern_data['usage_stats']['successful']
                    pattern_data['usage_stats']['success_rate'] = successful / total if total > 0 else 0.0

                    break

            # Save updated patterns
            with open(self.project_patterns_db, 'w') as f:
                json.dump(patterns, f, indent=2)

        except Exception as e:
            logger.warning(f"🔮 Error reinforcing solution: {e}")

    # ===========================================
    # NARRATIVE INTERFACE (v2.0)
    # ===========================================

    def think(self, thought: str, step: Optional[int] = None, category: Optional[str] = None):
        """
        Convenience method for Oracle's sequential thinking display.

        Args:
            thought: The reasoning step
            step: Step number (auto-increments if None)
            category: Label like "Scanning", "Analyzing", "Pattern Recognition", "Learning"

        Example:
            self.think("Checking knowledge base for patterns", category="Scanning")
        """
        if self.narrator:
            self.narrator.hero_thinks("🔮 Oracle", thought, step, category)

    # ===========================================
    # KNOWLEDGE BASE OPERATIONS
    # ===========================================

    def query_knowledge_base(self, query: str, agent_name: Optional[str] = None) -> List[Dict]:
        """
        🔮 Query knowledge base for relevant errors/solutions

        Args:
            query: Search query (error message, keywords, etc.)
            agent_name: Optional filter by agent name

        Returns:
            List of relevant error/solution records
        """
        # Sequential thinking display
        self.think(f"Searching knowledge base for: {query[:50]}...", category="Scanning")

        with open(self.errors_db, 'r') as f:
            data = json.load(f)

        results = []
        query_lower = query.lower()

        for error in data['errors']:
            # Filter by agent if specified
            if agent_name and error['agent'] != agent_name:
                continue

            # Search in error details and solution
            error_str = json.dumps(error).lower()
            if query_lower in error_str:
                results.append(error)

        # Sort by relevance (times encountered and success rate)
        results.sort(key=lambda x: (x['times_encountered'], x['success_rate']), reverse=True)

        # Sequential thinking display
        if results:
            self.think(f"Found {len(results)} relevant solutions", category="Result")

        logger.info(f"🔮 Knowledge query '{query}' returned {len(results)} results")
        return results

    def get_best_practices(self, category: str) -> List[Dict]:
        """
        🔮 Get best practices for a category

        Args:
            category: Category (coding, testing, performance, security, etc.)

        Returns:
            List of best practices
        """
        with open(self.best_practices_db, 'r') as f:
            data = json.load(f)

        practices = [p for p in data['practices'] if p.get('category') == category]

        logger.info(f"🔮 Retrieved {len(practices)} best practices for {category}")
        return practices

    def add_best_practice(self, category: str, title: str, description: str, source: str):
        """Add a new best practice to the knowledge base"""
        practice = {
            'category': category,
            'title': title,
            'description': description,
            'source': source,
            'added_at': datetime.now().isoformat()
        }

        with open(self.best_practices_db, 'r') as f:
            data = json.load(f)

        data['practices'].append(practice)

        with open(self.best_practices_db, 'w') as f:
            json.dump(data, f, indent=2)

        logger.info(f"🔮 Added best practice: {title}")

    # ==================== LEARNING & ANALYSIS ====================

    def analyze_mission_results(self, mission_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        🔮 Analyze mission results and learn from them

        Args:
            mission_results: Complete mission results from Superman

        Returns:
            Analysis and recommendations
        """
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'mission_id': mission_results.get('mission_id', 'unknown'),
            'insights': [],
            'recommendations': [],
            'patterns_detected': [],
            'oracle_says': ''
        }

        # Analyze each hero's performance
        for hero_name, hero_results in mission_results.get('hero_reports', {}).items():
            hero_analysis = self._analyze_hero_performance(hero_name, hero_results)
            analysis['insights'].extend(hero_analysis['insights'])
            analysis['recommendations'].extend(hero_analysis['recommendations'])

        # Detect patterns
        patterns = self._detect_patterns(mission_results)
        analysis['patterns_detected'] = patterns

        # Store insights in knowledge base
        self._store_mission_insights(analysis)

        # Oracle's verdict
        if len(analysis['recommendations']) == 0:
            analysis['oracle_says'] = "Perfect mission! All systems optimal. Knowledge base updated."
        elif len(analysis['recommendations']) < 3:
            analysis['oracle_says'] = "Minor optimizations detected. Implementing improvements."
        else:
            analysis['oracle_says'] = f"Critical analysis complete. {len(analysis['recommendations'])} improvements identified."

        logger.info(f"🔮 Mission analysis complete: {len(analysis['insights'])} insights, {len(analysis['recommendations'])} recommendations")

        return analysis

    def _analyze_hero_performance(self, hero_name: str, results: Dict) -> Dict[str, Any]:
        """Analyze individual hero performance"""
        insights = []
        recommendations = []

        # Check for errors
        if 'error' in results:
            insights.append(f"{hero_name} encountered error: {results['error']}")
            recommendations.append({
                'hero': hero_name,
                'priority': 'high',
                'issue': 'Error encountered',
                'recommendation': 'Review error logs and implement fix',
                'auto_fixable': False
            })

        # Check performance metrics
        if 'performance' in results:
            perf = results['performance']
            if perf.get('execution_time', 0) > self.performance_thresholds['response_time_max']:
                recommendations.append({
                    'hero': hero_name,
                    'priority': 'medium',
                    'issue': f"Slow execution time: {perf['execution_time']}ms",
                    'recommendation': 'Optimize performance or increase timeout',
                    'auto_fixable': False
                })

        # Check success rate
        if 'score' in results:
            score = results['score']
            if isinstance(score, dict) and score.get('score', 100) < 80:
                recommendations.append({
                    'hero': hero_name,
                    'priority': 'high',
                    'issue': f"Low quality score: {score['score']}",
                    'recommendation': 'Review and improve agent capabilities',
                    'auto_fixable': False
                })

        return {'insights': insights, 'recommendations': recommendations}

    def _detect_patterns(self, data: Dict) -> List[Dict]:
        """Detect patterns in mission data"""
        patterns = []

        # This is a placeholder for more sophisticated pattern detection
        # Could use ML models in the future

        return patterns

    def _store_mission_insights(self, analysis: Dict):
        """Store mission insights in patterns database"""
        with open(self.patterns_db, 'r') as f:
            data = json.load(f)

        data['trends'].append({
            'timestamp': analysis['timestamp'],
            'insights_count': len(analysis['insights']),
            'recommendations_count': len(analysis['recommendations']),
            'patterns_count': len(analysis['patterns_detected'])
        })

        # Keep only last 100 trends
        data['trends'] = data['trends'][-100:]

        with open(self.patterns_db, 'w') as f:
            json.dump(data, f, indent=2)

    def _analyze_error_patterns(self, agent_name: str, error_type: str):
        """Analyze if error is part of a pattern"""
        with open(self.errors_db, 'r') as f:
            data = json.load(f)

        # Count similar errors in last 24 hours
        recent_errors = [
            e for e in data['errors']
            if e['agent'] == agent_name and
            e['error_type'] == error_type and
            (datetime.now() - datetime.fromisoformat(e['timestamp'])) < timedelta(hours=24)
        ]

        if len(recent_errors) >= 3:
            logger.warning(f"🔮 PATTERN DETECTED: {agent_name} has {len(recent_errors)} {error_type} errors in last 24h")

            # NEW: Use strategic thinking to analyze pattern deeply
            if self.strategic_thinking:
                strategic_analysis = self._analyze_pattern_strategically({
                    'agent': agent_name,
                    'error_type': error_type,
                    'occurrences': len(recent_errors),
                    'recent_errors': recent_errors[:3]  # Last 3 for context
                })
                logger.info(f"🔮 Strategic Analysis: {strategic_analysis.get('hypothesis', 'N/A')}")

            # Store pattern
            self._store_pattern({
                'pattern_type': 'recurring_error',
                'agent': agent_name,
                'error_type': error_type,
                'occurrences': len(recent_errors),
                'detected_at': datetime.now().isoformat()
            })

    def _analyze_pattern_strategically(self, pattern_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        🧠 NEW: Oracle uses strategic thinking to deeply analyze patterns

        This makes Oracle intelligent - she THINKS about patterns instead of
        just counting them!

        Args:
            pattern_data: Data about the pattern to analyze

        Returns:
            Strategic insights about the pattern
        """
        if not self.strategic_thinking:
            return {"hypothesis": "Strategic thinking not available"}

        # Use strategic thinking engine
        insight = self.strategic_thinking.analyze_pattern(
            pattern_data=pattern_data,
            pattern_type=pattern_data.get('pattern_type', 'unknown')
        )

        return {
            "hypothesis": insight.hypothesis,
            "confidence": insight.confidence,
            "recommendations": insight.recommendations
        }

    def _store_pattern(self, pattern: Dict):
        """Store detected pattern"""
        with open(self.patterns_db, 'r') as f:
            data = json.load(f)

        data['patterns'].append(pattern)

        with open(self.patterns_db, 'w') as f:
            json.dump(data, f, indent=2)

    def predict_failures(self, agent_name: str) -> Dict[str, Any]:
        """
        🔮 Predict potential failures for an agent

        Args:
            agent_name: Name of agent to analyze

        Returns:
            Prediction report with probability and recommendations
        """
        prediction = {
            'agent': agent_name,
            'failure_probability': 0.0,
            'risk_level': 'low',
            'predicted_issues': [],
            'preventive_actions': [],
            'oracle_prediction': ''
        }

        # Analyze recent performance
        metrics = self.get_agent_metrics(agent_name)

        if metrics:
            # Calculate failure probability based on trends
            total_errors = metrics.get('total_errors', 0)
            success_rate = metrics.get('success_rate', 1.0)

            if total_errors > 5:
                prediction['failure_probability'] += 0.3
                prediction['predicted_issues'].append('High error rate detected')

            if success_rate < 0.9:
                prediction['failure_probability'] += 0.2
                prediction['predicted_issues'].append('Declining success rate')

            if success_rate < 0.5:
                prediction['failure_probability'] += 0.3
                prediction['predicted_issues'].append('Critical success rate - immediate attention required')

            # Determine risk level
            if prediction['failure_probability'] > 0.7:
                prediction['risk_level'] = 'critical'
                prediction['oracle_prediction'] = f"CRITICAL: {agent_name} likely to fail soon!"
            elif prediction['failure_probability'] > 0.4:
                prediction['risk_level'] = 'high'
                prediction['oracle_prediction'] = f"HIGH RISK: {agent_name} needs attention"
            elif prediction['failure_probability'] > 0.2:
                prediction['risk_level'] = 'medium'
                prediction['oracle_prediction'] = f"Monitor {agent_name} closely"
            else:
                prediction['oracle_prediction'] = f"{agent_name} is healthy"

        logger.info(f"🔮 Prediction for {agent_name}: {prediction['risk_level']} risk ({prediction['failure_probability']:.0%})")

        return prediction

    # ==================== PERFORMANCE MONITORING ====================

    def track_agent_performance(self,
                               agent_name: str,
                               metrics: Dict[str, Any]):
        """
        🔮 Track agent performance metrics

        Args:
            agent_name: Name of agent
            metrics: Performance metrics dictionary
        """
        with open(self.metrics_db, 'r') as f:
            data = json.load(f)

        if agent_name not in data['agents']:
            data['agents'][agent_name] = {
                'metrics_history': [],
                'total_missions': 0,
                'total_errors': 0,
                'success_rate': 1.0
            }

        agent_data = data['agents'][agent_name]

        # Add metrics with timestamp
        metrics_record = {
            **metrics,
            'timestamp': datetime.now().isoformat()
        }
        agent_data['metrics_history'].append(metrics_record)

        # Update aggregates
        agent_data['total_missions'] += 1
        if metrics.get('success', True):
            agent_data['success_rate'] = (agent_data['success_rate'] * (agent_data['total_missions'] - 1) + 1) / agent_data['total_missions']
        else:
            agent_data['total_errors'] += 1
            agent_data['success_rate'] = (agent_data['success_rate'] * (agent_data['total_missions'] - 1)) / agent_data['total_missions']

        # Keep only last 100 metrics
        agent_data['metrics_history'] = agent_data['metrics_history'][-100:]

        with open(self.metrics_db, 'w') as f:
            json.dump(data, f, indent=2)

        logger.info(f"🔮 Tracked performance for {agent_name}: Success rate {agent_data['success_rate']:.1%}")

    def get_agent_metrics(self, agent_name: str) -> Optional[Dict]:
        """Get current metrics for an agent"""
        with open(self.metrics_db, 'r') as f:
            data = json.load(f)

        return data['agents'].get(agent_name)

    def generate_performance_report(self) -> Dict[str, Any]:
        """
        🔮 Generate comprehensive performance report for all agents

        Returns:
            Performance report with recommendations
        """
        with open(self.metrics_db, 'r') as f:
            data = json.load(f)

        report = {
            'generated_at': datetime.now().isoformat(),
            'total_agents': len(data['agents']),
            'agents': {},
            'recommendations': [],
            'overall_health': 'healthy'
        }

        unhealthy_agents = 0

        for agent_name, agent_data in data['agents'].items():
            agent_report = {
                'total_missions': agent_data['total_missions'],
                'success_rate': agent_data['success_rate'],
                'total_errors': agent_data['total_errors'],
                'health_status': 'healthy'
            }

            # Determine health status
            if agent_data['success_rate'] < 0.8:
                agent_report['health_status'] = 'unhealthy'
                unhealthy_agents += 1
                report['recommendations'].append({
                    'agent': agent_name,
                    'issue': f"Low success rate: {agent_data['success_rate']:.1%}",
                    'action': 'Review and fix agent implementation'
                })
            elif agent_data['success_rate'] < 0.95:
                agent_report['health_status'] = 'warning'

            report['agents'][agent_name] = agent_report

        # Overall health
        if unhealthy_agents > 2:
            report['overall_health'] = 'critical'
        elif unhealthy_agents > 0:
            report['overall_health'] = 'warning'

        logger.info(f"🔮 Performance report generated: {report['overall_health']} - {unhealthy_agents} unhealthy agents")

        return report

    # ==================== VERSION CONTROL ====================

    def create_agent_version(self,
                            agent_name: str,
                            version: str,
                            changes: str,
                            code_hash: Optional[str] = None) -> bool:
        """
        🔮 Create a new version of an agent

        Args:
            agent_name: Name of agent
            version: Version number (e.g., "1.2.0")
            changes: Description of changes
            code_hash: Optional hash of agent code for verification

        Returns:
            Success status
        """
        version_record = {
            'version': version,
            'created_at': datetime.now().isoformat(),
            'changes': changes,
            'code_hash': code_hash or 'unknown',
            'status': 'active'
        }

        if agent_name not in self.agent_versions:
            self.agent_versions[agent_name] = {
                'current_version': version,
                'versions': []
            }

        self.agent_versions[agent_name]['versions'].append(version_record)
        self.agent_versions[agent_name]['current_version'] = version

        self._save_agent_versions()

        logger.info(f"🔮 Created version {version} for {agent_name}")
        return True

    def rollback_agent(self, agent_name: str, target_version: str) -> bool:
        """
        🔮 Rollback agent to a previous version

        Args:
            agent_name: Name of agent
            target_version: Version to rollback to

        Returns:
            Success status
        """
        if agent_name not in self.agent_versions:
            logger.error(f"🔮 Agent {agent_name} not found in version history")
            return False

        versions = self.agent_versions[agent_name]['versions']
        target = next((v for v in versions if v['version'] == target_version), None)

        if not target:
            logger.error(f"🔮 Version {target_version} not found for {agent_name}")
            return False

        self.agent_versions[agent_name]['current_version'] = target_version
        self._save_agent_versions()

        logger.warning(f"🔮 ROLLBACK: {agent_name} rolled back to version {target_version}")
        return True

    def get_agent_version_history(self, agent_name: str) -> List[Dict]:
        """Get version history for an agent"""
        if agent_name not in self.agent_versions:
            return []

        return self.agent_versions[agent_name]['versions']

    # ==================== ORACLE'S MAIN INTERFACE ====================

    def oracle_report(self) -> Dict[str, Any]:
        """
        🔮 Generate Oracle's comprehensive system report

        Returns:
            Complete system health and knowledge report
        """
        report = {
            'oracle': '🔮 Oracle - Meta-Agent',
            'timestamp': datetime.now().isoformat(),
            'knowledge_base': {},
            'performance': {},
            'predictions': {},
            'recommendations': [],
            'oracle_says': ''
        }

        # Knowledge base stats
        with open(self.errors_db, 'r') as f:
            errors_data = json.load(f)
        with open(self.patterns_db, 'r') as f:
            patterns_data = json.load(f)

        report['knowledge_base'] = {
            'total_errors_documented': len(errors_data['errors']),
            'total_patterns_detected': len(patterns_data['patterns']),
            'knowledge_base_size_mb': sum(f.stat().st_size for f in self.knowledge_base_dir.glob('*.json')) / (1024 * 1024)
        }

        # Performance report
        perf_report = self.generate_performance_report()
        report['performance'] = perf_report

        # Generate predictions for all agents
        predictions = {}
        with open(self.metrics_db, 'r') as f:
            metrics_data = json.load(f)

        for agent_name in metrics_data['agents'].keys():
            predictions[agent_name] = self.predict_failures(agent_name)

        report['predictions'] = predictions

        # Compile recommendations
        report['recommendations'] = perf_report['recommendations']

        # Oracle's final message
        critical_predictions = sum(1 for p in predictions.values() if p['risk_level'] == 'critical')
        if critical_predictions > 0:
            report['oracle_says'] = f"⚠️ ALERT: {critical_predictions} agents at critical risk!"
        elif report['performance']['overall_health'] == 'critical':
            report['oracle_says'] = "⚠️ System health critical. Immediate attention required."
        elif len(report['recommendations']) > 5:
            report['oracle_says'] = f"System stable but {len(report['recommendations'])} improvements recommended."
        else:
            report['oracle_says'] = "✅ All systems optimal. Justice League operating at peak efficiency."

        logger.info(f"🔮 Oracle report generated: {report['oracle_says']}")

        return report

    # ==================== PROJECT PATTERN TRACKING ====================

    def get_project_context(self, file_key: str) -> Dict[str, Any]:
        """
        🔮 Get project-level context for Figma conversions

        This method is called by Superman/Artemis to retrieve existing patterns
        from the same Figma project, enabling component reuse and consistency.

        Args:
            file_key: Figma file key (e.g., "6Pmf9gCcUccyqbCO9nN6Ts")

        Returns:
            Project context including:
            - project_known: bool
            - conversions_count: int
            - shared_components: List of components to reuse
            - design_system: Colors, spacing, typography
            - common_patterns: List of pattern names
            - recommendation: String recommendation
        """
        # Sequential thinking display
        self.think(f"Analyzing project context for: {file_key[:12]}...", category="Analyzing")

        try:
            with open(self.project_patterns_db, 'r') as f:
                data = json.load(f)

            project = data.get('projects', {}).get(file_key)

            if not project:
                # Sequential thinking: New project discovery
                self.think("No previous patterns found - new project", category="Learning")
                logger.info(f"🔮 Project {file_key} is unknown - first conversion")
                return {
                    'project_known': False,
                    'conversions_count': 0,
                    'shared_components': [],
                    'design_system': {},
                    'common_patterns': [],
                    'recommendation': 'First conversion - establish baseline patterns'
                }

            # Extract shared component names
            shared_components = list(project.get('shared_elements', {}).keys())

            # Sequential thinking: Pattern recognition
            self.think(
                f"Project recognized! {project.get('conversions_count', 0)} previous conversions, {len(shared_components)} shared components",
                category="Pattern Recognition"
            )

            logger.info(f"🔮 Project {file_key} known! {project['conversions_count']} previous conversions")
            logger.info(f"🔮 Shared components available: {', '.join(shared_components)}")

            return {
                'project_known': True,
                'project_name': project.get('project_name', 'Unknown'),
                'conversions_count': project.get('conversions_count', 0),
                'shared_components': shared_components,
                'shared_component_details': project.get('shared_elements', {}),
                'design_system': project.get('design_system', {}),
                'common_patterns': project.get('common_patterns', []),
                'recommendation': f"Reuse {len(shared_components)} shared components: {', '.join(shared_components)}"
            }

        except FileNotFoundError:
            logger.warning(f"🔮 Project patterns database not found")
            return {
                'project_known': False,
                'conversions_count': 0,
                'shared_components': [],
                'design_system': {},
                'common_patterns': [],
                'recommendation': 'Database not initialized'
            }
        except Exception as e:
            logger.error(f"🔮 Error loading project context: {e}")
            return {
                'project_known': False,
                'error': str(e)
            }

    def update_project_patterns(self,
                                file_key: str,
                                component_name: str,
                                node_id: str,
                                new_shared_elements: Optional[Dict[str, Any]] = None,
                                new_patterns: Optional[List[str]] = None) -> bool:
        """
        🔮 Update project patterns after a conversion

        Called by Artemis after generating a component to record:
        - New conversions
        - New shared elements discovered
        - New patterns identified

        Args:
            file_key: Figma file key
            component_name: Name of converted component
            node_id: Figma node ID
            new_shared_elements: New shared elements to track
            new_patterns: New patterns discovered

        Returns:
            Success status
        """
        try:
            with open(self.project_patterns_db, 'r') as f:
                data = json.load(f)

            # Initialize project if it doesn't exist
            if file_key not in data.get('projects', {}):
                data['projects'] = data.get('projects', {})
                data['projects'][file_key] = {
                    'figma_file_key': file_key,
                    'project_name': 'Unknown',
                    'conversions_count': 0,
                    'conversions': [],
                    'shared_elements': {},
                    'design_system': {},
                    'common_patterns': []
                }

            project = data['projects'][file_key]

            # Add conversion record
            conversion_record = {
                'component_name': component_name,
                'node_id': node_id,
                'converted_at': datetime.now().isoformat(),
                'file_path': f'preview-app/src/components/{component_name}.tsx'
            }
            project['conversions'].append(conversion_record)
            project['conversions_count'] = len(project['conversions'])

            # Update shared elements
            if new_shared_elements:
                for element_name, element_data in new_shared_elements.items():
                    if element_name not in project['shared_elements']:
                        project['shared_elements'][element_name] = element_data
                        logger.info(f"🔮 New shared element tracked: {element_name}")
                    else:
                        # Update found_in list
                        if component_name not in project['shared_elements'][element_name].get('found_in', []):
                            project['shared_elements'][element_name]['found_in'].append(component_name)

            # Update patterns
            if new_patterns:
                for pattern in new_patterns:
                    if pattern not in project['common_patterns']:
                        project['common_patterns'].append(pattern)
                        logger.info(f"🔮 New pattern tracked: {pattern}")

            # Save back
            with open(self.project_patterns_db, 'w') as f:
                json.dump(data, f, indent=2)

            logger.info(f"🔮 Project patterns updated for {file_key}")
            logger.info(f"🔮 Total conversions: {project['conversions_count']}")
            logger.info(f"🔮 Shared elements: {len(project['shared_elements'])}")

            return True

        except Exception as e:
            logger.error(f"🔮 Error updating project patterns: {e}")
            return False

    def get_shared_component_status(self, component_name: str) -> Dict[str, Any]:
        """
        🔮 Get status of a shared component

        Args:
            component_name: Name of shared component (e.g., "AppHeader")

        Returns:
            Component status including extraction status, file path, etc.
        """
        try:
            with open(self.shared_components_db, 'r') as f:
                data = json.load(f)

            component = data.get('shared_components', {}).get(component_name)

            if not component:
                return {'exists': False, 'status': 'not_tracked'}

            return {
                'exists': True,
                'status': component.get('status', 'unknown'),
                'file_path': component.get('file_path'),
                'description': component.get('description'),
                'used_in_projects': component.get('used_in_projects', []),
                'used_in_components': component.get('used_in_components', [])
            }

        except Exception as e:
            logger.error(f"🔮 Error getting shared component status: {e}")
            return {'exists': False, 'error': str(e)}

    def mark_shared_component_extracted(self,
                                       component_name: str,
                                       file_path: str) -> bool:
        """
        🔮 Mark a shared component as extracted

        Args:
            component_name: Name of shared component
            file_path: Path to the extracted component file

        Returns:
            Success status
        """
        try:
            with open(self.shared_components_db, 'r') as f:
                data = json.load(f)

            if component_name in data.get('shared_components', {}):
                data['shared_components'][component_name]['status'] = 'extracted'
                data['shared_components'][component_name]['file_path'] = file_path
                data['shared_components'][component_name]['extracted_at'] = datetime.now().isoformat()

                # Log extraction
                if 'extraction_log' not in data:
                    data['extraction_log'] = []

                data['extraction_log'].append({
                    'component_name': component_name,
                    'file_path': file_path,
                    'extracted_at': datetime.now().isoformat()
                })

                with open(self.shared_components_db, 'w') as f:
                    json.dump(data, f, indent=2)

                logger.info(f"🔮 Shared component extracted: {component_name} → {file_path}")
                return True

            return False

        except Exception as e:
            logger.error(f"🔮 Error marking component extracted: {e}")
            return False

    # ========================================
    # 🔮 USER QUESTION LEARNING SYSTEM (v1.9.1)
    # ========================================

    def store_user_question(self,
                           question: str,
                           category: str,
                           context: Dict[str, Any],
                           response_summary: Optional[str] = None) -> str:
        """
        🔮 Store a user question with full context for learning

        Args:
            question: The user's question
            category: Question category (frame_export, figma_conversion, etc.)
            context: Mission context (mission_type, user_stage, etc.)
            response_summary: Brief summary of Oracle's response

        Returns:
            question_id: Unique identifier for the stored question
        """
        try:
            with open(self.project_patterns_db, 'r') as f:
                data = json.load(f)

            # Generate unique question ID
            question_id = f"Q{len(data.get('user_learning', {}).get('questions_asked', [])) + 1:04d}"

            # Create question record
            question_record = {
                'id': question_id,
                'question': question,
                'category': category,
                'context': context,
                'asked_at': datetime.now().isoformat(),
                'response_summary': response_summary,
                'was_helpful': None,  # To be updated later
                'follow_ups': []
            }

            # Store question
            if 'user_learning' not in data:
                data['user_learning'] = {'questions_asked': []}

            data['user_learning']['questions_asked'].append(question_record)

            # Update category stats
            if 'question_categories' not in data['user_learning']:
                data['user_learning']['question_categories'] = {}

            if category not in data['user_learning']['question_categories']:
                data['user_learning']['question_categories'][category] = {
                    'count': 0,
                    'avg_satisfaction': 0.0,
                    'common_issues': [],
                    'typical_questions': []
                }

            data['user_learning']['question_categories'][category]['count'] += 1

            # Update analytics
            if 'analytics' not in data['user_learning']:
                data['user_learning']['analytics'] = {}

            data['user_learning']['analytics']['total_questions'] = data['user_learning']['analytics'].get('total_questions', 0) + 1
            data['user_learning']['analytics']['last_updated'] = datetime.now().isoformat()

            with open(self.project_patterns_db, 'w') as f:
                json.dump(data, f, indent=2)

            logger.info(f"🔮 User question stored: {question_id} [{category}]")
            return question_id

        except Exception as e:
            logger.error(f"🔮 Error storing user question: {e}")
            return ""

    def query_similar_questions(self, question: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        🔮 Find similar questions in FAQ database

        Args:
            question: User's current question
            category: Optional category filter

        Returns:
            List of similar questions with their answers
        """
        try:
            with open(self.project_patterns_db, 'r') as f:
                data = json.load(f)

            questions_asked = data.get('user_learning', {}).get('questions_asked', [])

            if not questions_asked:
                return []

            # Simple keyword matching (can be enhanced with NLP)
            question_lower = question.lower()
            keywords = set(question_lower.split())

            similar_questions = []
            for q in questions_asked:
                if category and q.get('category') != category:
                    continue

                q_text = q.get('question', '').lower()
                q_keywords = set(q_text.split())

                # Calculate similarity score based on common keywords
                common_keywords = keywords.intersection(q_keywords)
                if len(common_keywords) >= 2:  # At least 2 common words
                    similarity_score = len(common_keywords) / max(len(keywords), len(q_keywords))
                    similar_questions.append({
                        **q,
                        'similarity_score': similarity_score
                    })

            # Sort by similarity score
            similar_questions.sort(key=lambda x: x.get('similarity_score', 0), reverse=True)

            return similar_questions[:5]  # Return top 5

        except Exception as e:
            logger.error(f"🔮 Error querying similar questions: {e}")
            return []

    def get_question_analytics(self) -> Dict[str, Any]:
        """
        🔮 Get analytics on user questions

        Returns:
            Analytics including most asked categories, common patterns, etc.
        """
        try:
            with open(self.project_patterns_db, 'r') as f:
                data = json.load(f)

            user_learning = data.get('user_learning', {})
            categories = user_learning.get('question_categories', {})
            analytics = user_learning.get('analytics', {})

            # Find most asked category
            most_asked = max(categories.items(), key=lambda x: x[1].get('count', 0)) if categories else (None, {})

            return {
                'total_questions': analytics.get('total_questions', 0),
                'most_asked_category': most_asked[0],
                'most_asked_count': most_asked[1].get('count', 0),
                'categories_breakdown': {
                    cat: stats.get('count', 0)
                    for cat, stats in categories.items()
                },
                'avg_satisfaction': analytics.get('user_satisfaction_score', 0.0),
                'last_updated': analytics.get('last_updated')
            }

        except Exception as e:
            logger.error(f"🔮 Error getting question analytics: {e}")
            return {}

    def track_user_journey(self, user_stage: str, milestone: str) -> bool:
        """
        🔮 Track user's learning journey progression

        Args:
            user_stage: Current stage (beginner, intermediate, advanced)
            milestone: Milestone achieved (completed_first_export, achieved_90plus_accuracy, etc.)

        Returns:
            Success status
        """
        try:
            with open(self.project_patterns_db, 'r') as f:
                data = json.load(f)

            if 'user_learning' not in data:
                data['user_learning'] = {}

            if 'user_journey_log' not in data['user_learning']:
                data['user_learning']['user_journey_log'] = []

            # Log milestone
            data['user_learning']['user_journey_log'].append({
                'user_stage': user_stage,
                'milestone': milestone,
                'achieved_at': datetime.now().isoformat()
            })

            # Update success indicators if milestone matches
            learning_journeys = data['user_learning'].get('learning_journeys', {})
            success_indicators = learning_journeys.get('success_indicators', [])

            if milestone in success_indicators:
                logger.info(f"🔮 User achieved success indicator: {milestone}")

            with open(self.project_patterns_db, 'w') as f:
                json.dump(data, f, indent=2)

            logger.info(f"🔮 User journey tracked: {user_stage} → {milestone}")
            return True

        except Exception as e:
            logger.error(f"🔮 Error tracking user journey: {e}")
            return False

    def identify_knowledge_gaps(self) -> List[Dict[str, Any]]:
        """
        🔮 Identify knowledge gaps based on user questions

        Returns:
            List of identified gaps with severity and suggested improvements
        """
        try:
            with open(self.project_patterns_db, 'r') as f:
                data = json.load(f)

            questions_asked = data.get('user_learning', {}).get('questions_asked', [])

            if not questions_asked:
                return []

            # Analyze question patterns to find gaps
            gaps = []
            category_question_count = {}

            for q in questions_asked:
                category = q.get('category', 'unknown')
                category_question_count[category] = category_question_count.get(category, 0) + 1

            # Categories with high question counts indicate potential gaps
            for category, count in category_question_count.items():
                if count >= 3:  # Threshold for identifying a gap
                    gaps.append({
                        'area': category,
                        'question_count': count,
                        'severity': 'high' if count >= 5 else 'medium',
                        'recommendation': f"Consider improving documentation for {category}",
                        'typical_questions': [
                            q.get('question') for q in questions_asked
                            if q.get('category') == category
                        ][:3]
                    })

            gaps.sort(key=lambda x: x.get('question_count', 0), reverse=True)
            return gaps

        except Exception as e:
            logger.error(f"🔮 Error identifying knowledge gaps: {e}")
            return []

    # ========================================
    # 🔮 SUPER META AGENT - HERO LEARNING SYSTEM (v1.9.1)
    # ========================================

    def track_mission_outcome(self, mission_results: Dict[str, Any]) -> bool:
        """
        🔮 Track complete mission outcome for meta-learning (PHASE 1)

        This is called by Superman after EVERY mission (success or failure) to enable
        Oracle to learn patterns and improve all heroes over time.

        Args:
            mission_results: Complete mission results from Superman

        Returns:
            Success status
        """
        try:
            with open(self.project_patterns_db, 'r') as f:
                data = json.load(f)

            if 'hero_meta_learning' not in data:
                data['hero_meta_learning'] = {
                    'mission_history': [],
                    'hero_performance_trends': {}
                }

            # Extract key mission data
            mission_id = f"M{len(data['hero_meta_learning']['mission_history']) + 1:04d}"

            mission_record = {
                'mission_id': mission_id,
                'timestamp': mission_results.get('timestamp', datetime.now().isoformat()),
                'mission_type': self._detect_mission_type(mission_results),
                'target': mission_results.get('target_url', mission_results.get('file_key', 'unknown')),
                'heroes_deployed': mission_results.get('heroes_deployed', []),
                'overall_score': mission_results.get('justice_league_score', {}).get('overall_score', 0),
                'grade': mission_results.get('justice_league_score', {}).get('grade', 'F'),
                'success': mission_results.get('justice_league_score', {}).get('overall_score', 0) >= 70,
                'hero_reports': {}
            }

            # Extract hero-specific learnings
            hero_reports = mission_results.get('hero_reports', {})
            for hero_name, report in hero_reports.items():
                mission_record['hero_reports'][hero_name] = self._extract_hero_learnings(hero_name, report)

            # Store mission in history
            data['hero_meta_learning']['mission_history'].append(mission_record)

            # Update hero performance trends
            self._update_hero_performance_trends(data, mission_record)

            # Keep only last 100 missions in main file (archive rest)
            if len(data['hero_meta_learning']['mission_history']) > 100:
                # Archive old missions
                archived = data['hero_meta_learning']['mission_history'][:-100]
                data['hero_meta_learning']['mission_history'] = data['hero_meta_learning']['mission_history'][-100:]
                # TODO: Save archived missions to separate file

            with open(self.project_patterns_db, 'w') as f:
                json.dump(data, f, indent=2)

            logger.info(f"🔮 Mission outcome tracked: {mission_id} [{mission_record['mission_type']}] - Success: {mission_record['success']}")

            # Real-time learning: Analyze and generate recommendations immediately
            self._perform_real_time_learning(data, mission_record)

            return True

        except Exception as e:
            logger.error(f"🔮 Error tracking mission outcome: {e}")
            return False

    def start_learning_session(
        self,
        user_request: str,
        user_intent: str,
        mission_type: str = 'unknown'
    ) -> "LearningSession":
        """
        🎓 Start a new learning session for auto-learning

        Creates a LearningSession that tracks the entire user interaction from
        request to completion, enabling Oracle to learn automatically.

        Args:
            user_request: Original user request (exact words)
            user_intent: Parsed intent (figma_conversion, frame_export, website_analysis, etc.)
            mission_type: Type of mission being performed

        Returns:
            LearningSession instance

        Example:
            session = oracle.start_learning_session(
                user_request="Convert Dashboard 10 to React",
                user_intent="figma_conversion",
                mission_type="figma_conversion"
            )
        """
        # Generate unique session ID
        session_id = f"LS{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Create learning session
        session = LearningSession(
            session_id=session_id,
            user_request=user_request,
            user_intent=user_intent,
            mission_type=mission_type
        )

        logger.info(f"🔮 Learning session started: {session_id} [Intent: {user_intent}]")

        return session

    def complete_learning_session(
        self,
        session: "LearningSession",
        results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        🎓 Complete a learning session and generate insights

        Analyzes the complete session, infers user satisfaction, generates
        insights and recommendations, then stores everything for future learning.

        Args:
            session: The LearningSession to complete
            results: Final mission results

        Returns:
            Advisory dictionary with learnings and recommendations

        Example:
            advisory = oracle.complete_learning_session(session, mission_results)
            # Returns: {
            #     'satisfaction': {...},
            #     'what_worked_well': [...],
            #     'what_needs_improvement': [...],
            #     'recommendations': [...]
            # }
        """
        try:
            # Set final results
            session.set_results(results)

            # Import satisfaction analyzer (will create in Phase 1.2)
            from .satisfaction_analyzer import SatisfactionAnalyzer

            # Analyze user satisfaction
            satisfaction_analysis = SatisfactionAnalyzer.analyze_satisfaction(session)
            session.user_satisfaction = satisfaction_analysis
            session.satisfaction_signals = satisfaction_analysis.get('signals', [])

            # Generate insights from session
            insights = self._generate_session_insights(session)
            session.learnings = insights

            # Generate recommendations
            recommendations = self._generate_session_recommendations(session)
            session.recommendations = recommendations

            # Store session in knowledge base
            self._store_learning_session(session)

            # Build advisory for presentation
            advisory = {
                'session_id': session.session_id,
                'satisfaction': satisfaction_analysis,
                'what_worked_well': [i for i in insights if i.get('type') == 'success'],
                'what_needs_improvement': [i for i in insights if i.get('type') == 'improvement'],
                'recommendations': recommendations,
                'learnings': insights
            }

            logger.info(f"🔮 Learning session completed: {session.session_id} "
                       f"[Satisfaction: {satisfaction_analysis.get('assessment', 'unknown')}]")

            return advisory

        except Exception as e:
            logger.error(f"🔮 Error completing learning session: {e}")
            return {}

    def learn_from_operation(
        self,
        hero: str,
        operation: str,
        result: Dict[str, Any],
        session: Optional["LearningSession"] = None
    ):
        """
        🔮 Learn from a single hero operation (auto-invoked by hero hooks)

        This is called automatically by hero operation hooks to enable
        real-time learning from every operation.

        Args:
            hero: Hero name (e.g., "Artemis")
            operation: Operation name (e.g., "generate_component_code_expert")
            result: Operation result
            session: Optional learning session (if part of larger mission)
        """
        try:
            # Quick operation insight
            insight = {
                'timestamp': datetime.now().isoformat(),
                'hero': hero,
                'operation': operation,
                'success': result.get('success', False),
                'score': result.get('score', result.get('accuracy_score', 0))
            }

            # If operation was successful, note the pattern
            if insight['success'] and insight['score'] >= 90:
                logger.debug(f"🔮 High-performance operation: {hero}.{operation} ({insight['score']}%)")

            # If operation failed, analyze why
            elif not insight['success']:
                error_pattern = {
                    'hero': hero,
                    'operation': operation,
                    'error_type': result.get('error', {}).get('type', 'unknown'),
                    'error_message': str(result.get('error', ''))
                }
                logger.debug(f"🔮 Operation failure pattern: {hero}.{operation} - {error_pattern['error_type']}")

        except Exception as e:
            logger.error(f"🔮 Error learning from operation: {e}")

    def _generate_session_insights(self, session: "LearningSession") -> List[Dict[str, Any]]:
        """Generate insights from completed learning session"""
        insights = []

        # Analyze hero performance
        for op in session.hero_operations:
            if op.get('success') and op.get('result', {}).get('score', 0) >= 90:
                insights.append({
                    'type': 'success',
                    'insight': f"{op['hero']} excelled at {op['operation']}",
                    'evidence': f"Score: {op['result'].get('score', 0)}%",
                    'confidence': 0.9
                })

        # Analyze failures
        for error in session.errors_encountered:
            insights.append({
                'type': 'improvement',
                'insight': f"{error['hero']} struggled with {error['operation']}",
                'evidence': f"Error: {error['error']}",
                'confidence': 0.8
            })

        # Satisfaction correlation
        if session.user_satisfaction:
            satisfaction = session.user_satisfaction.get('assessment')
            if satisfaction == 'happy':
                insights.append({
                    'type': 'success',
                    'insight': f"User satisfied with {session.mission_type} approach",
                    'evidence': f"Satisfaction score: {session.user_satisfaction.get('score', 0):.2f}",
                    'confidence': session.user_satisfaction.get('confidence', 0.5)
                })

        return insights

    def _generate_session_recommendations(self, session: "LearningSession") -> List[Dict[str, Any]]:
        """Generate recommendations from session"""
        recommendations = []

        # Recommendation based on performance
        for op in session.hero_operations:
            score = op.get('result', {}).get('score', 0)
            if 60 < score < 80:
                recommendations.append({
                    'type': 'threshold_adjustment',
                    'priority': 'medium',
                    'suggestion': f"Consider adjusting {op['hero']}'s thresholds for {op['operation']}",
                    'rationale': f"Score {score}% indicates potential for optimization"
                })

        # Recommendation based on satisfaction
        if session.user_satisfaction:
            if session.user_satisfaction.get('assessment') == 'unhappy':
                recommendations.append({
                    'type': 'methodology_review',
                    'priority': 'high',
                    'suggestion': f"Review {session.mission_type} methodology",
                    'rationale': "User satisfaction low despite technical success"
                })

        return recommendations

    def _store_learning_session(self, session: "LearningSession"):
        """Store learning session in knowledge base"""
        try:
            with open(self.project_patterns_db, 'r') as f:
                data = json.load(f)

            if 'learning_sessions' not in data:
                data['learning_sessions'] = {}

            if 'satisfaction_patterns' not in data:
                data['satisfaction_patterns'] = {
                    'user_satisfaction_history': [],
                    'satisfaction_thresholds': {}
                }

            # Store session
            data['learning_sessions'][session.session_id] = session.to_dict()

            # Update satisfaction history
            if session.user_satisfaction:
                data['satisfaction_patterns']['user_satisfaction_history'].append({
                    'session_id': session.session_id,
                    'timestamp': session.start_time.isoformat(),
                    'score': session.user_satisfaction.get('score', 0),
                    'assessment': session.user_satisfaction.get('assessment', 'unknown'),
                    'mission_type': session.mission_type
                })

            # Keep only last 50 sessions
            if len(data['learning_sessions']) > 50:
                # Sort by timestamp and keep latest 50
                sorted_sessions = sorted(
                    data['learning_sessions'].items(),
                    key=lambda x: x[1].get('started_at', ''),
                    reverse=True
                )
                data['learning_sessions'] = dict(sorted_sessions[:50])

            with open(self.project_patterns_db, 'w') as f:
                json.dump(data, f, indent=2)

            logger.debug(f"🔮 Learning session stored: {session.session_id}")

        except Exception as e:
            logger.error(f"🔮 Error storing learning session: {e}")

    def _detect_mission_type(self, mission_results: Dict[str, Any]) -> str:
        """Detect mission type from results"""
        if 'file_key' in mission_results or 'figma' in str(mission_results.get('target_url', '')).lower():
            if mission_results.get('frames_exported'):
                return 'frame_export'
            return 'figma_conversion'
        elif 'url' in mission_results or 'target_url' in mission_results:
            return 'website_analysis'
        return 'unknown'

    def _extract_hero_learnings(self, hero_name: str, hero_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        🔮 Extract learnings from a hero's report (PHASE 1)

        Parses hero-specific data to extract performance metrics
        """
        learnings = {
            'hero': hero_name,
            'participated': True,
            'success': False,
            'score': 0,
            'key_metrics': {},
            'issues_found': [],
            'learnings': []
        }

        # Hero-specific extraction logic
        if hero_name.lower() in ['artemis', 'artemis_codesmith']:
            learnings['score'] = hero_report.get('artemis_score', hero_report.get('score', 0))
            learnings['success'] = hero_report.get('success', False)
            learnings['key_metrics'] = {
                'accuracy': hero_report.get('accuracy_score', 0),
                'iterations': hero_report.get('iterations_used', 0)
            }

        elif hero_name.lower() in ['green_arrow', 'green_arrow_visual_validator']:
            learnings['score'] = hero_report.get('accuracy_score', 0)
            learnings['success'] = hero_report.get('accuracy_score', 0) >= 90
            learnings['key_metrics'] = {
                'accuracy': hero_report.get('accuracy_score', 0),
                'status': hero_report.get('status', 'UNKNOWN')
            }

        elif hero_name.lower() == 'batman':
            tests_passed = hero_report.get('tests_passed', 0)
            total_tests = hero_report.get('total_tests', tests_passed + hero_report.get('tests_failed', 0))
            learnings['score'] = (tests_passed / total_tests * 100) if total_tests > 0 else 0
            learnings['success'] = hero_report.get('tests_passed', 0) > 0
            learnings['key_metrics'] = {
                'tests_passed': tests_passed,
                'tests_failed': hero_report.get('tests_failed', 0)
            }

        elif hero_name.lower() == 'hawkman':
            learnings['success'] = hero_report.get('success', False)
            learnings['score'] = 100 if hero_report.get('success') else 0
            learnings['key_metrics'] = {
                'frames_exported': hero_report.get('frames_exported', 0),
                'total_frames': hero_report.get('total_frames', 0)
            }

        # Extract issues/violations
        learnings['issues_found'] = hero_report.get('issues', hero_report.get('violations', []))

        return learnings

    def _update_hero_performance_trends(self, data: Dict[str, Any], mission_record: Dict[str, Any]):
        """Update hero performance trends with new mission data"""
        hero_reports = mission_record.get('hero_reports', {})

        for hero_name, hero_data in hero_reports.items():
            hero_key = hero_name.lower().replace(' ', '_').replace('🎨', '').replace('🏹', '').replace('🦇', '').replace('🦅', '').strip()

            if hero_key not in data['hero_meta_learning']['hero_performance_trends']:
                data['hero_meta_learning']['hero_performance_trends'][hero_key] = {
                    'total_missions': 0,
                    'success_rate': 0.0,
                    'average_accuracy': 0.0,
                    'accuracy_trend_30d': [],
                    'skill_gaps': [],
                    'last_updated': None
                }

            trend = data['hero_meta_learning']['hero_performance_trends'][hero_key]

            # Update counters
            trend['total_missions'] += 1

            # Update success rate
            previous_successes = trend['success_rate'] * (trend['total_missions'] - 1)
            new_successes = previous_successes + (1 if hero_data.get('success') else 0)
            trend['success_rate'] = new_successes / trend['total_missions']

            # Update average accuracy
            if 'score' in hero_data:
                previous_avg = trend['average_accuracy'] * (trend['total_missions'] - 1)
                trend['average_accuracy'] = (previous_avg + hero_data['score']) / trend['total_missions']

            # Track trend (keep last 30 days)
            trend['accuracy_trend_30d'].append({
                'timestamp': mission_record.get('timestamp'),
                'score': hero_data.get('score', 0),
                'success': hero_data.get('success', False)
            })

            # Keep only last 30 data points
            if len(trend['accuracy_trend_30d']) > 30:
                trend['accuracy_trend_30d'] = trend['accuracy_trend_30d'][-30:]

            trend['last_updated'] = datetime.now().isoformat()

    def _perform_real_time_learning(self, data: Dict[str, Any], mission_record: Dict[str, Any]):
        """
        🔮 Perform real-time learning after each mission (PHASE 2 preview)

        Analyzes mission outcome and immediately generates insights
        """
        # Quick pattern detection
        if not mission_record.get('success'):
            # Mission failed - identify why
            failure_pattern = {
                'mission_id': mission_record['mission_id'],
                'mission_type': mission_record['mission_type'],
                'heroes_involved': mission_record['heroes_deployed'],
                'identified_at': datetime.now().isoformat(),
                'pattern': 'mission_failure'
            }

            if 'predictive_insights' not in data['hero_meta_learning']:
                data['hero_meta_learning']['predictive_insights'] = {'failure_patterns': []}

            data['hero_meta_learning']['predictive_insights']['failure_patterns'].append(failure_pattern)

            logger.warning(f"🔮 Mission failure detected: {mission_record['mission_id']} - Oracle is learning from this")

    # ========================================
    # 🔮 PHASE 2: HERO PERFORMANCE ANALYSIS & INTELLIGENCE
    # ========================================

    def analyze_hero_performance_trends(self, hero_name: str) -> Dict[str, Any]:
        """
        🔮 Analyze a hero's performance trends over time (PHASE 2)

        Args:
            hero_name: Name of the hero to analyze

        Returns:
            Performance analysis with trends, skill gaps, and insights
        """
        try:
            with open(self.project_patterns_db, 'r') as f:
                data = json.load(f)

            hero_key = hero_name.lower().replace(' ', '_')
            trends = data.get('hero_meta_learning', {}).get('hero_performance_trends', {}).get(hero_key, {})

            if not trends or trends.get('total_missions', 0) == 0:
                return {'hero': hero_name, 'status': 'insufficient_data', 'missions': 0}

            # Calculate trend direction
            accuracy_trend = trends.get('accuracy_trend_30d', [])
            if len(accuracy_trend) >= 2:
                recent_avg = sum(d['score'] for d in accuracy_trend[-5:]) / min(5, len(accuracy_trend[-5:]))
                older_avg = sum(d['score'] for d in accuracy_trend[:5]) / min(5, len(accuracy_trend[:5]))
                trend_direction = 'improving' if recent_avg > older_avg else 'declining' if recent_avg < older_avg else 'stable'
                trend_change = recent_avg - older_avg
            else:
                trend_direction = 'insufficient_data'
                trend_change = 0

            return {
                'hero': hero_name,
                'total_missions': trends.get('total_missions', 0),
                'success_rate': trends.get('success_rate', 0.0),
                'average_accuracy': trends.get('average_accuracy', 0.0),
                'trend_direction': trend_direction,
                'trend_change': trend_change,
                'last_updated': trends.get('last_updated'),
                'skill_gaps': trends.get('skill_gaps', []),
                'recommendation': self._generate_trend_recommendation(trends, trend_direction)
            }

        except Exception as e:
            logger.error(f"🔮 Error analyzing hero performance trends: {e}")
            return {'hero': hero_name, 'status': 'error', 'error': str(e)}

    def identify_skill_gaps(self, hero_name: str) -> List[Dict[str, Any]]:
        """
        🔮 Identify specific skill gaps for a hero (PHASE 2)

        Analyzes mission history to find scenarios where hero underperforms

        Args:
            hero_name: Name of hero to analyze

        Returns:
            List of identified skill gaps with severity and recommendations
        """
        try:
            with open(self.project_patterns_db, 'r') as f:
                data = json.load(f)

            mission_history = data.get('hero_meta_learning', {}).get('mission_history', [])
            hero_key = hero_name.lower()

            # Analyze missions where this hero participated
            skill_gaps = []
            mission_type_performance = {}

            for mission in mission_history:
                hero_reports = mission.get('hero_reports', {})

                for h_name, h_data in hero_reports.items():
                    if hero_key in h_name.lower():
                        mission_type = mission.get('mission_type', 'unknown')
                        score = h_data.get('score', 0)

                        if mission_type not in mission_type_performance:
                            mission_type_performance[mission_type] = []
                        mission_type_performance[mission_type].append(score)

            # Identify weak areas
            for mission_type, scores in mission_type_performance.items():
                avg_score = sum(scores) / len(scores) if scores else 0
                if avg_score < 80:  # Below 80% is a skill gap
                    skill_gaps.append({
                        'area': mission_type,
                        'average_score': avg_score,
                        'missions_analyzed': len(scores),
                        'severity': 'high' if avg_score < 60 else 'medium',
                        'recommendation': f"Focus training on {mission_type} scenarios"
                    })

            return skill_gaps

        except Exception as e:
            logger.error(f"🔮 Error identifying skill gaps: {e}")
            return []

    def compare_hero_effectiveness(self, mission_type: str) -> Dict[str, Any]:
        """
        🔮 Compare which heroes are most effective for a mission type (PHASE 2)

        Args:
            mission_type: Type of mission (frame_export, figma_conversion, etc.)

        Returns:
            Effectiveness comparison across heroes
        """
        try:
            with open(self.project_patterns_db, 'r') as f:
                data = json.load(f)

            mission_history = data.get('hero_meta_learning', {}).get('mission_history', [])

            hero_performance = {}

            for mission in mission_history:
                if mission.get('mission_type') == mission_type:
                    for hero_name, hero_data in mission.get('hero_reports', {}).items():
                        if hero_name not in hero_performance:
                            hero_performance[hero_name] = []
                        hero_performance[hero_name].append(hero_data.get('score', 0))

            # Calculate averages and rank
            hero_rankings = []
            for hero_name, scores in hero_performance.items():
                avg_score = sum(scores) / len(scores) if scores else 0
                hero_rankings.append({
                    'hero': hero_name,
                    'average_score': avg_score,
                    'missions_completed': len(scores),
                    'effectiveness': 'high' if avg_score >= 90 else 'medium' if avg_score >= 75 else 'low'
                })

            hero_rankings.sort(key=lambda x: x['average_score'], reverse=True)

            return {
                'mission_type': mission_type,
                'hero_rankings': hero_rankings,
                'most_effective': hero_rankings[0] if hero_rankings else None,
                'least_effective': hero_rankings[-1] if hero_rankings else None
            }

        except Exception as e:
            logger.error(f"🔮 Error comparing hero effectiveness: {e}")
            return {}

    def generate_hero_improvement_recommendations(self, hero_name: str) -> List[Dict[str, Any]]:
        """
        🔮 Generate actionable improvement recommendations for a hero (PHASE 2)

        Args:
            hero_name: Name of hero

        Returns:
            List of recommendations with priority and expected impact
        """
        try:
            # Analyze trends and skill gaps
            trends = self.analyze_hero_performance_trends(hero_name)
            skill_gaps = self.identify_skill_gaps(hero_name)

            recommendations = []

            # Recommendation 1: Address declining performance
            if trends.get('trend_direction') == 'declining':
                recommendations.append({
                    'type': 'performance_decline',
                    'priority': 'high',
                    'recommendation': f"Performance declining by {abs(trends.get('trend_change', 0)):.1f}% - review recent changes",
                    'expected_impact': 'Restore performance to previous levels',
                    'action': 'threshold_adjustment'
                })

            # Recommendation 2: Address skill gaps
            for gap in skill_gaps:
                if gap.get('severity') == 'high':
                    recommendations.append({
                        'type': 'skill_gap',
                        'priority': 'high',
                        'area': gap.get('area'),
                        'recommendation': f"Low performance in {gap.get('area')} ({gap.get('average_score'):.1f}%)",
                        'expected_impact': f"Improve {gap.get('area')} accuracy by 15-20%",
                        'action': 'training_scenario'
                    })

            # Recommendation 3: Optimize thresholds if success rate is low
            if trends.get('success_rate', 0) < 0.8:
                recommendations.append({
                    'type': 'threshold_optimization',
                    'priority': 'medium',
                    'recommendation': f"Success rate {trends.get('success_rate', 0):.1%} - consider threshold adjustments",
                    'expected_impact': 'Increase success rate by 10-15%',
                    'action': 'threshold_adjustment'
                })

            return recommendations

        except Exception as e:
            logger.error(f"🔮 Error generating improvement recommendations: {e}")
            return []

    def _generate_trend_recommendation(self, trends: Dict[str, Any], trend_direction: str) -> str:
        """Generate recommendation based on trend"""
        if trend_direction == 'improving':
            return "Performance improving - continue current approach"
        elif trend_direction == 'declining':
            return "⚠️ Performance declining - recommend review and adjustment"
        elif trend_direction == 'stable':
            avg = trends.get('average_accuracy', 0)
            if avg >= 90:
                return "Excellent stable performance"
            elif avg >= 75:
                return "Good performance - opportunity for optimization"
            else:
                return "Stable but below target - training recommended"
        return "Insufficient data for recommendation"

    # ========================================
    # 🔮 PHASE 3: CAPABILITY ENHANCEMENT SYSTEM
    # ========================================

    def get_hero_capabilities(self, hero_name: str) -> Dict[str, Any]:
        """
        🔮 Get hero's current capabilities and Oracle's recommendations (PHASE 3)

        Heroes call this on initialization to load Oracle's learned wisdom

        Args:
            hero_name: Name of hero

        Returns:
            Hero capabilities including thresholds and recommendations
        """
        try:
            hero_capabilities_file = Path('/Users/admin/Documents/claudecode/Projects/aldo-vision/data/hero_capabilities.json')

            if not hero_capabilities_file.exists():
                logger.warning("🔮 Hero capabilities file not found - using defaults")
                return {'hero': hero_name, 'status': 'using_defaults', 'thresholds': {}, 'recommended_techniques': []}

            with open(hero_capabilities_file, 'r') as f:
                data = json.load(f)

            hero_key = hero_name.lower().replace(' ', '_')
            hero_config = data.get('heroes', {}).get(hero_key, {})

            if not hero_config:
                logger.info(f"🔮 No specific config for {hero_name} - using defaults")
                return {'hero': hero_name, 'status': 'using_defaults', 'thresholds': {}, 'recommended_techniques': []}

            # Also get performance trends for context
            trends = self.analyze_hero_performance_trends(hero_name)

            return {
                'hero': hero_name,
                'status': 'loaded',
                'thresholds': hero_config.get('thresholds', {}),
                'recommended_techniques': hero_config.get('recommended_techniques', []),
                'skill_evolution': hero_config.get('skill_evolution', {}),
                'performance_trends': trends,
                'oracle_notes': hero_config.get('oracle_notes', '')
            }

        except Exception as e:
            logger.error(f"🔮 Error loading hero capabilities: {e}")
            return {'hero': hero_name, 'status': 'error', 'error': str(e)}

    def update_hero_capability(self, hero_name: str, capability_type: str, updates: Dict[str, Any]) -> bool:
        """
        🔮 Update hero capability based on learning (PHASE 3)

        Args:
            hero_name: Name of hero
            capability_type: Type of update ('threshold', 'technique', 'skill_evolution')
            updates: Dict of updates to apply

        Returns:
            Success status
        """
        try:
            hero_capabilities_file = Path('/Users/admin/Documents/claudecode/Projects/aldo-vision/data/hero_capabilities.json')

            with open(hero_capabilities_file, 'r') as f:
                data = json.load(f)

            hero_key = hero_name.lower().replace(' ', '_')

            if hero_key not in data.get('heroes', {}):
                logger.warning(f"🔮 Hero {hero_name} not found in capabilities file")
                return False

            hero_config = data['heroes'][hero_key]

            # Apply updates based on type
            if capability_type == 'threshold':
                for threshold_name, threshold_value in updates.items():
                    if threshold_name in hero_config.get('thresholds', {}):
                        hero_config['thresholds'][threshold_name]['value'] = threshold_value
                        hero_config['thresholds'][threshold_name]['adjusted_at'] = datetime.now().isoformat()
                        hero_config['thresholds'][threshold_name]['learned_from'] = 'oracle_meta_learning'

            elif capability_type == 'technique':
                if 'recommended_techniques' not in hero_config:
                    hero_config['recommended_techniques'] = []
                hero_config['recommended_techniques'].append({
                    **updates,
                    'added_at': datetime.now().isoformat()
                })

            elif capability_type == 'skill_evolution':
                if 'skill_evolution' not in hero_config:
                    hero_config['skill_evolution'] = {}
                hero_config['skill_evolution'].update(updates)

            data['last_updated'] = datetime.now().isoformat()

            with open(hero_capabilities_file, 'w') as f:
                json.dump(data, f, indent=2)

            logger.info(f"🔮 Updated {hero_name} {capability_type}: {updates}")
            return True

        except Exception as e:
            logger.error(f"🔮 Error updating hero capability: {e}")
            return False

    # ========================================
    # 🔮 PHASE 4: PREDICTIVE DEPLOYMENT
    # ========================================

    def predict_mission_success(self, mission_context: Dict[str, Any], heroes_list: List[str]) -> Dict[str, Any]:
        """
        🔮 Predict mission success probability (PHASE 4)

        Args:
            mission_context: Mission details (type, complexity, etc.)
            heroes_list: List of heroes being deployed

        Returns:
            Prediction with probability and reasoning
        """
        try:
            with open(self.project_patterns_db, 'r') as f:
                data = json.load(f)

            mission_type = mission_context.get('mission_type', 'unknown')
            mission_history = data.get('hero_meta_learning', {}).get('mission_history', [])

            # Find similar past missions
            similar_missions = [
                m for m in mission_history
                if m.get('mission_type') == mission_type
            ]

            if not similar_missions:
                return {
                    'prediction': 'unknown',
                    'probability': 0.5,
                    'confidence': 'low',
                    'reason': 'No historical data for this mission type'
                }

            # Calculate success rate for this mission type with these heroes
            matching_missions = [
                m for m in similar_missions
                if any(hero in m.get('heroes_deployed', []) for hero in heroes_list)
            ]

            if matching_missions:
                success_count = sum(1 for m in matching_missions if m.get('success', False))
                probability = success_count / len(matching_missions)
            else:
                # Use overall success rate for mission type
                success_count = sum(1 for m in similar_missions if m.get('success', False))
                probability = success_count / len(similar_missions) if similar_missions else 0.5

            prediction = 'success' if probability >= 0.7 else 'uncertain' if probability >= 0.5 else 'failure'
            confidence = 'high' if len(matching_missions) >= 5 else 'medium' if len(matching_missions) >= 2 else 'low'

            return {
                'prediction': prediction,
                'probability': probability,
                'confidence': confidence,
                'based_on_missions': len(matching_missions),
                'reason': f"Based on {len(matching_missions)} similar missions with {probability:.1%} success rate"
            }

        except Exception as e:
            logger.error(f"🔮 Error predicting mission success: {e}")
            return {'prediction': 'error', 'probability': 0.5, 'error': str(e)}

    def suggest_optimal_hero_combination(self, mission_context: Dict[str, Any]) -> List[str]:
        """
        🔮 Suggest optimal hero combination for a mission (PHASE 4)

        Args:
            mission_context: Mission details

        Returns:
            List of recommended heroes
        """
        try:
            mission_type = mission_context.get('mission_type', 'unknown')

            # Get hero effectiveness for this mission type
            effectiveness = self.compare_hero_effectiveness(mission_type)
            rankings = effectiveness.get('hero_rankings', [])

            # Recommend top 3 most effective heroes
            recommended = [h['hero'] for h in rankings[:3] if h.get('effectiveness') in ['high', 'medium']]

            if not recommended:
                # Fallback to default heroes based on mission type
                defaults = {
                    'figma_conversion': ['Artemis', 'Green Arrow', 'Hawkman'],
                    'frame_export': ['Hawkman', 'Oracle'],
                    'website_analysis': ['Batman', 'Green Lantern', 'Wonder Woman']
                }
                recommended = defaults.get(mission_type, ['Artemis', 'Batman'])

            return recommended

        except Exception as e:
            logger.error(f"🔮 Error suggesting hero combination: {e}")
            return []

    # ========================================
    # 🔮 PHASE 5: TRAINING SCENARIO GENERATION
    # ========================================

    def generate_training_scenario(self, hero_name: str, weak_area: str) -> Dict[str, Any]:
        """
        🔮 Generate training scenario to strengthen hero weakness (PHASE 5)

        Args:
            hero_name: Name of hero
            weak_area: Area needing improvement

        Returns:
            Training scenario with objectives and success criteria
        """
        try:
            scenario_id = f"TRAIN-{hero_name[:3].upper()}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

            scenario = {
                'scenario_id': scenario_id,
                'hero': hero_name,
                'target_area': weak_area,
                'difficulty': 'adaptive',
                'objectives': self._generate_training_objectives(hero_name, weak_area),
                'success_criteria': {
                    'min_score': 85,
                    'improvement_target': 15,
                    'consistency_required': True
                },
                'created_at': datetime.now().isoformat(),
                'status': 'active'
            }

            # Store scenario
            with open(self.project_patterns_db, 'r') as f:
                data = json.load(f)

            if 'hero_meta_learning' not in data:
                data['hero_meta_learning'] = {}
            if 'training_scenarios' not in data['hero_meta_learning']:
                data['hero_meta_learning']['training_scenarios'] = {'active_scenarios': [], 'completed_scenarios': []}

            data['hero_meta_learning']['training_scenarios']['active_scenarios'].append(scenario)

            with open(self.project_patterns_db, 'w') as f:
                json.dump(data, f, indent=2)

            logger.info(f"🔮 Generated training scenario {scenario_id} for {hero_name} [{weak_area}]")
            return scenario

        except Exception as e:
            logger.error(f"🔮 Error generating training scenario: {e}")
            return {}

    def _generate_training_objectives(self, hero_name: str, weak_area: str) -> List[str]:
        """Generate specific training objectives"""
        objectives_map = {
            'figma_conversion': [
                "Convert 5 complex dashboard components with 90%+ accuracy",
                "Handle nested component structures correctly",
                "Maintain consistent spacing and layout"
            ],
            'frame_export': [
                "Export 50+ frames with 100% success rate",
                "Handle nested SECTION nodes correctly",
                "Process COMPONENT and COMPONENT_SET types"
            ],
            'visual_validation': [
                "Validate 10 components with 95%+ accuracy",
                "Correctly identify spacing discrepancies within tolerance",
                "Provide actionable fix recommendations"
            ]
        }
        return objectives_map.get(weak_area, [f"Improve performance in {weak_area}"])

    def get_hero_training_plan(self, hero_name: str) -> Dict[str, Any]:
        """
        🔮 Get complete training plan for a hero (PHASE 5)

        Args:
            hero_name: Name of hero

        Returns:
            Training plan with scenarios and priorities
        """
        try:
            # Identify skill gaps
            skill_gaps = self.identify_skill_gaps(hero_name)

            # Generate scenarios for each gap
            training_scenarios = []
            for gap in skill_gaps:
                if gap.get('severity') in ['high', 'medium']:
                    scenario = self.generate_training_scenario(hero_name, gap.get('area'))
                    if scenario:
                        training_scenarios.append(scenario)

            return {
                'hero': hero_name,
                'total_scenarios': len(training_scenarios),
                'scenarios': training_scenarios,
                'priority_order': [s['scenario_id'] for s in sorted(training_scenarios, key=lambda x: x.get('difficulty', ''))]
            }

        except Exception as e:
            logger.error(f"🔮 Error generating training plan: {e}")
            return {}


class LearningSession:
    """
    🎓 LEARNING SESSION - Tracks a complete user interaction for Oracle's auto-learning

    Captures everything from user request to mission completion, enabling Oracle
    to learn patterns, infer satisfaction, and generate insights automatically.

    This is Oracle v2.0's core learning mechanism - every Justice League operation
    creates a learning session.
    """

    def __init__(self, session_id: str, user_request: str, user_intent: str, mission_type: str):
        """
        Initialize a new learning session

        Args:
            session_id: Unique session identifier
            user_request: Original user request (exact words)
            user_intent: Parsed intent (figma_conversion, frame_export, website_analysis, etc.)
            mission_type: Type of mission being performed
        """
        self.session_id = session_id
        self.start_time = datetime.now()
        self.end_time = None

        # User context
        self.user_request = user_request
        self.user_intent = user_intent
        self.expected_outcome = ""  # What user expects to achieve

        # Mission tracking
        self.mission_type = mission_type
        self.hero_operations = []  # List of all hero operations
        self.results = {}  # Final mission results

        # Learning data
        self.user_satisfaction = None  # Inferred satisfaction score
        self.satisfaction_signals = []  # Evidence for satisfaction inference
        self.learnings = []  # Key insights extracted
        self.recommendations = []  # Actionable recommendations

        # Interaction tracking
        self.retry_count = 0
        self.errors_encountered = []
        self.follow_up_questions = []

    def log_operation_start(self, hero: str, operation: str, context: Dict[str, Any]):
        """
        Log the start of a hero operation

        Args:
            hero: Hero name (e.g., "Artemis", "Green Arrow")
            operation: Operation name (e.g., "generate_component_code_expert")
            context: Operation context (parameters, config, etc.)
        """
        operation_record = {
            'hero': hero,
            'operation': operation,
            'started_at': datetime.now().isoformat(),
            'completed_at': None,
            'duration_seconds': None,
            'context': context,
            'result': None,
            'success': None
        }
        self.hero_operations.append(operation_record)

    def log_operation_complete(self, hero: str, operation: str, result: Dict[str, Any]):
        """
        Log the completion of a hero operation

        Args:
            hero: Hero name
            operation: Operation name
            result: Operation result including success status, scores, etc.
        """
        # Find the matching operation record
        for op in reversed(self.hero_operations):
            if op['hero'] == hero and op['operation'] == operation and op['completed_at'] is None:
                op['completed_at'] = datetime.now().isoformat()
                op['result'] = result
                op['success'] = result.get('success', False)

                # Calculate duration
                started = datetime.fromisoformat(op['started_at'])
                completed = datetime.fromisoformat(op['completed_at'])
                op['duration_seconds'] = (completed - started).total_seconds()

                # Track errors
                if not op['success'] and 'error' in result:
                    self.errors_encountered.append({
                        'hero': hero,
                        'operation': operation,
                        'error': result['error']
                    })
                break

    def log_retry(self):
        """Log that user retried the operation"""
        self.retry_count += 1

    def log_follow_up_question(self, question: str):
        """Log user's follow-up question"""
        self.follow_up_questions.append(question)

    def set_results(self, results: Dict[str, Any]):
        """Set final mission results"""
        self.results = results
        self.end_time = datetime.now()

    def get_duration_seconds(self) -> float:
        """Get total session duration in seconds"""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return (datetime.now() - self.start_time).total_seconds()

    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary for storage"""
        return {
            'session_id': self.session_id,
            'started_at': self.start_time.isoformat(),
            'completed_at': self.end_time.isoformat() if self.end_time else None,
            'duration_seconds': self.get_duration_seconds(),
            'user_request': self.user_request,
            'user_intent': self.user_intent,
            'expected_outcome': self.expected_outcome,
            'mission_type': self.mission_type,
            'operations': self.hero_operations,
            'results': self.results,
            'satisfaction': self.user_satisfaction,
            'satisfaction_signals': self.satisfaction_signals,
            'learnings': self.learnings,
            'recommendations': self.recommendations,
            'retry_count': self.retry_count,
            'errors_encountered': self.errors_encountered,
            'follow_up_questions': self.follow_up_questions
        }


# Main entry point - Oracle's Mission Interface
def oracle_analyze_system() -> Dict[str, Any]:
    """
    🔮 Oracle analyzes the entire Justice League system

    Returns:
        Complete system analysis and recommendations
    """
    oracle = OracleMeta()
    return oracle.oracle_report()
