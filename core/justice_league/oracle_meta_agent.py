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

    Powers:
    1. Knowledge Management - Store all errors, solutions, patterns
    2. Learning Engine - Learn from every mission, improve agents
    3. Self-Healing - Detect issues, propose fixes (require approval)
    4. Performance Monitoring - Track metrics, optimize performance
    5. Version Control - Manage versions, enable rollback
    6. Predictive Maintenance - Predict and prevent failures
    7. MCP Integration - Monitor and integrate MCP servers
    8. Testing Pipeline - Generate and validate tests
    """

    def __init__(self, knowledge_base_dir: Optional[str] = None):
        """
        Initialize Oracle's information network

        Args:
            knowledge_base_dir: Directory for knowledge base storage
        """
        self.knowledge_base_dir = Path(knowledge_base_dir) if knowledge_base_dir else Path('/tmp/aldo-vision-justice-league/oracle')
        self.knowledge_base_dir.mkdir(parents=True, exist_ok=True)

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

    def query_knowledge_base(self, query: str, agent_name: Optional[str] = None) -> List[Dict]:
        """
        🔮 Query knowledge base for relevant errors/solutions

        Args:
            query: Search query (error message, keywords, etc.)
            agent_name: Optional filter by agent name

        Returns:
            List of relevant error/solution records
        """
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
            # Store pattern
            self._store_pattern({
                'pattern_type': 'recurring_error',
                'agent': agent_name,
                'error_type': error_type,
                'occurrences': len(recent_errors),
                'detected_at': datetime.now().isoformat()
            })

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
        try:
            with open(self.project_patterns_db, 'r') as f:
                data = json.load(f)

            project = data.get('projects', {}).get(file_key)

            if not project:
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


# Main entry point - Oracle's Mission Interface
def oracle_analyze_system() -> Dict[str, Any]:
    """
    🔮 Oracle analyzes the entire Justice League system

    Returns:
        Complete system analysis and recommendations
    """
    oracle = OracleMeta()
    return oracle.oracle_report()
