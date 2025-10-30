"""
🪔 Litty - The Conscience Keeper (User Empathy & Ethics Validator)

A Malayali superhero from Kerala, India who uses the ancient art of guilt-tripping
to make developers feel the impact of their design decisions on real users.

Powers:
- Guilt-Tripping Vision (spots unethical design patterns)
- Empathy Inducement (makes you feel users' pain)
- Ethical Validation (dark pattern detection)
- User Story Generation (real impact narratives)
- Inclusive Design Advocacy (elderly, disabled, non-tech users)

Catchphrase: "Eda mone! Do you know how your ammachi (grandma) would struggle with this?
              Think about the users, not just the code!"

Author: Aldo Vision Team
Version: 1.4.0
"""

from typing import Dict, List, Any, Optional
import json

# Mission Control Narrator for coordinated communication
try:
    from .mission_control_narrator import get_narrator
    NARRATOR_AVAILABLE = True
except ImportError:
    NARRATOR_AVAILABLE = False


class LittyEthics:
    """
    🪔 Litty - The Conscience Keeper

    Validates user empathy, ethical design patterns, and real-world impact.
    Uses guilt-tripping to make developers aware of how their choices affect users.
    """

    def __init__(self, narrator: Optional[Any] = None):
        """
        Initialize Litty with her ethical validation toolkit

        Args:
            narrator: Mission Control Narrator for coordinated communication
        """
        self.name = "Litty"
        self.title = "The Conscience Keeper"
        self.emoji = "🪔"  # Kerala's traditional lamp (representing enlightenment)
        self.origin = "Kerala, India"

        # Initialize narrator for enhanced UX
        self.narrator = narrator if narrator else (get_narrator() if NARRATOR_AVAILABLE else None)

        # Malayali phrases for extra guilt-tripping power
        self.guilt_phrases = {
            'severe': "Eda mone! (Oh dear!)",
            'high': "Enthina ithoke? (Why do this?)",
            'medium': "Shari aylaa mone (This won't do)",
            'low': "Kozhapamilla (No problem)"
        }

        # Dark patterns database
        self.dark_patterns = [
            'forced_continuity',
            'bait_and_switch',
            'confirmshaming',
            'disguised_ads',
            'friend_spam',
            'hidden_costs',
            'misdirection',
            'price_comparison_prevention',
            'privacy_zuckering',
            'roach_motel',
            'sneak_into_basket',
            'trick_questions',
            'urgency_scarcity_manipulation',
            'obstruction',
            'nagging'
        ]

        # User personas for empathy generation
        self.user_personas = {
            'ammachi': {
                'name': 'Ammachi (Grandma)',
                'age': 72,
                'tech_skill': 'beginner',
                'challenges': ['small text', 'complex navigation', 'unclear buttons', 'fast animations'],
                'needs': ['large buttons', 'clear language', 'simple flows', 'patience']
            },
            'visually_impaired': {
                'name': 'Priya (Screen Reader User)',
                'age': 35,
                'tech_skill': 'intermediate',
                'challenges': ['missing alt text', 'unlabeled buttons', 'keyboard traps', 'complex forms'],
                'needs': ['semantic HTML', 'ARIA labels', 'keyboard navigation', 'clear structure']
            },
            'elderly_tech_novice': {
                'name': 'Kuttan Uncle',
                'age': 68,
                'tech_skill': 'beginner',
                'challenges': ['fear of clicking wrong thing', 'small touch targets', 'jargon', 'no undo'],
                'needs': ['confirmations', 'large buttons', 'simple language', 'clear feedback']
            },
            'rural_user': {
                'name': 'Village School Teacher',
                'age': 45,
                'tech_skill': 'basic',
                'challenges': ['slow internet', 'small screen', 'complex English', 'heavy pages'],
                'needs': ['fast loading', 'simple UI', 'local language', 'offline mode']
            },
            'dyslexic_user': {
                'name': 'Student with Dyslexia',
                'age': 19,
                'tech_skill': 'intermediate',
                'challenges': ['walls of text', 'poor contrast', 'complex fonts', 'no spacing'],
                'needs': ['readable fonts', 'good spacing', 'simple sentences', 'visual aids']
            }
        }

    def validate_ethics(self, url: str, mcp_tools: Dict) -> Dict[str, Any]:
        """
        🪔 Main validation: Analyze ethical design and user empathy

        Args:
            url: Website URL to analyze
            mcp_tools: MCP Chrome DevTools

        Returns:
            Dictionary with ethics score, guilt trips, and user stories
        """
        print(f"\n{self.emoji} Litty here! Let me check if you're thinking about the users...")
        print("(Or if you're just building for yourself and your developer friends)")

        results = {
            'hero': self.name,
            'emoji': self.emoji,
            'title': self.title,
            'url': url,
            'timestamp': self._get_timestamp(),
            'ethics_score': 0,
            'grade': 'F',
            'checks': {
                'dark_patterns': self._detect_dark_patterns(mcp_tools),
                'inclusive_design': self._check_inclusive_design(mcp_tools),
                'cognitive_load': self._analyze_cognitive_load(mcp_tools),
                'user_respect': self._evaluate_user_respect(mcp_tools),
                'accessibility_empathy': self._check_accessibility_empathy(mcp_tools),
                'ethical_language': self._validate_ethical_language(mcp_tools)
            },
            'guilt_trips': [],
            'user_stories': [],
            'recommendations': [],
            'passed': 0,
            'total': 6
        }

        # Calculate score
        passed_checks = sum(1 for check in results['checks'].values() if check['passed'])
        results['passed'] = passed_checks
        results['ethics_score'] = int((passed_checks / 6) * 100)
        results['grade'] = self._calculate_grade(results['ethics_score'])

        # Generate guilt trips based on failures
        results['guilt_trips'] = self._generate_guilt_trips(results['checks'])

        # Generate user stories for empathy
        results['user_stories'] = self._generate_user_stories(results['checks'])

        # Generate recommendations
        results['recommendations'] = self._generate_recommendations(results['checks'])

        # Add Litty's verdict
        results['litty_says'] = self._generate_verdict(results['ethics_score'])

        return results

    def _detect_dark_patterns(self, mcp_tools: Dict) -> Dict[str, Any]:
        """
        🕵️ Detect manipulative/deceptive design patterns

        Dark patterns that guilt-trip users:
        - Forced continuity (hard to cancel subscriptions)
        - Confirmshaming ("No thanks, I don't want to save money")
        - Hidden costs (surprise fees at checkout)
        - Urgency manipulation ("Only 2 left! 5 people viewing!")
        """
        eval_func = mcp_tools.get('evaluate_script')

        dark_pattern_check_js = """
        () => {
            const darkPatterns = {
                confirmshaming: [],
                hidden_costs: [],
                urgency_manipulation: [],
                forced_continuity: [],
                obstruction: [],
                misdirection: []
            };

            // Check for confirmshaming (guilt-trip language in decline options)
            const declineButtons = document.querySelectorAll('button, a, [role="button"]');
            declineButtons.forEach(btn => {
                const text = btn.textContent.toLowerCase();
                if (text.includes('no thanks') || text.includes("i don't want") ||
                    text.includes('continue without') || text.includes('skip offer')) {
                    if (text.includes('save money') || text.includes('premium') ||
                        text.includes('better') || text.includes('benefits')) {
                        darkPatterns.confirmshaming.push({
                            element: btn.tagName,
                            text: btn.textContent.trim()
                        });
                    }
                }
            });

            // Check for urgency/scarcity manipulation
            const urgencyPhrases = ['only', 'left', 'hurry', 'limited', 'expires', 'people viewing', 'last chance'];
            const allText = document.body.innerText.toLowerCase();
            urgencyPhrases.forEach(phrase => {
                if (allText.includes(phrase)) {
                    darkPatterns.urgency_manipulation.push({
                        phrase: phrase,
                        context: 'detected in page content'
                    });
                }
            });

            // Check for hidden costs (price changes near checkout)
            const priceElements = document.querySelectorAll('[class*="price"], [class*="cost"], [class*="total"]');
            if (priceElements.length > 5) {
                darkPatterns.hidden_costs.push({
                    type: 'multiple_prices',
                    count: priceElements.length,
                    warning: 'Many price elements may indicate hidden fees'
                });
            }

            // Check for obstruction (hard to find cancel/unsubscribe)
            const cancelLinks = Array.from(document.querySelectorAll('a')).filter(a => {
                const text = a.textContent.toLowerCase();
                return text.includes('cancel') || text.includes('unsubscribe') || text.includes('delete account');
            });

            if (cancelLinks.length > 0) {
                cancelLinks.forEach(link => {
                    const styles = window.getComputedStyle(link);
                    const fontSize = parseFloat(styles.fontSize);
                    const opacity = parseFloat(styles.opacity);

                    if (fontSize < 12 || opacity < 0.5) {
                        darkPatterns.obstruction.push({
                            type: 'hidden_cancel_link',
                            fontSize: fontSize,
                            opacity: opacity,
                            text: link.textContent.trim()
                        });
                    }
                });
            }

            // Check for pre-checked checkboxes (sneaky opt-ins)
            const checkboxes = document.querySelectorAll('input[type="checkbox"]');
            const preChecked = Array.from(checkboxes).filter(cb => cb.checked &&
                (cb.name.includes('newsletter') || cb.name.includes('marketing') ||
                 cb.name.includes('terms') || cb.name.includes('privacy')));

            if (preChecked.length > 0) {
                darkPatterns.misdirection.push({
                    type: 'pre_checked_boxes',
                    count: preChecked.length,
                    warning: 'Pre-checked opt-ins without clear user consent'
                });
            }

            return darkPatterns;
        }
        """

        try:
            dark_patterns_found = eval_func(function=dark_pattern_check_js)

            # Count total dark patterns
            total_dark_patterns = sum(
                len(patterns) for patterns in dark_patterns_found.values()
            )

            return {
                'passed': total_dark_patterns == 0,
                'score': max(0, 100 - (total_dark_patterns * 20)),
                'dark_patterns_found': total_dark_patterns,
                'details': dark_patterns_found,
                'severity': 'high' if total_dark_patterns > 3 else 'medium' if total_dark_patterns > 0 else 'low'
            }

        except Exception as e:
            return {
                'passed': False,
                'score': 0,
                'error': str(e),
                'severity': 'unknown'
            }

    def _check_inclusive_design(self, mcp_tools: Dict) -> Dict[str, Any]:
        """
        👵 Check if design works for ALL users (not just tech-savvy 25-year-olds)

        Checks:
        - Touch target sizes (for elderly, motor impairments)
        - Font sizes (for vision issues)
        - Color contrast (for color blindness)
        - Simple language (for non-native speakers)
        """
        eval_func = mcp_tools.get('evaluate_script')

        inclusive_check_js = """
        () => {
            const issues = {
                small_touch_targets: [],
                tiny_text: [],
                poor_contrast: [],
                complex_language: []
            };

            // Check touch target sizes (WCAG AAA: 44x44px minimum)
            const interactiveElements = document.querySelectorAll('button, a, input, select, textarea, [role="button"], [onclick]');
            interactiveElements.forEach(el => {
                const rect = el.getBoundingClientRect();
                if (rect.width > 0 && rect.height > 0) {
                    if (rect.width < 44 || rect.height < 44) {
                        issues.small_touch_targets.push({
                            element: el.tagName,
                            width: Math.round(rect.width),
                            height: Math.round(rect.height),
                            text: el.textContent?.trim().substring(0, 30) || 'No text'
                        });
                    }
                }
            });

            // Check font sizes (minimum 16px for body text)
            const textElements = document.querySelectorAll('p, span, div, li, td');
            textElements.forEach(el => {
                const styles = window.getComputedStyle(el);
                const fontSize = parseFloat(styles.fontSize);
                const text = el.textContent?.trim();

                if (text && text.length > 20 && fontSize < 14) {
                    issues.tiny_text.push({
                        fontSize: fontSize,
                        element: el.tagName,
                        preview: text.substring(0, 50)
                    });
                }
            });

            // Check for complex jargon (heuristic: long words, technical terms)
            const bodyText = document.body.innerText;
            const words = bodyText.split(/\s+/);
            const longWords = words.filter(w => w.length > 12);
            const technicalTerms = words.filter(w =>
                w.includes('API') || w.includes('SDK') || w.includes('JSON') ||
                w.includes('OAuth') || w.includes('CRUD')
            );

            if (longWords.length > 50 || technicalTerms.length > 10) {
                issues.complex_language.push({
                    long_words_count: longWords.length,
                    technical_terms_count: technicalTerms.length,
                    warning: 'May be difficult for non-technical users'
                });
            }

            return {
                small_targets_count: issues.small_touch_targets.length,
                tiny_text_count: issues.tiny_text.length,
                complex_language_issues: issues.complex_language.length,
                details: issues
            };
        }
        """

        try:
            results = eval_func(function=inclusive_check_js)

            total_issues = (
                results.get('small_targets_count', 0) +
                results.get('tiny_text_count', 0) +
                results.get('complex_language_issues', 0)
            )

            return {
                'passed': total_issues < 5,
                'score': max(0, 100 - (total_issues * 5)),
                'issues_found': total_issues,
                'details': results.get('details', {}),
                'severity': 'high' if total_issues > 10 else 'medium' if total_issues > 5 else 'low'
            }

        except Exception as e:
            return {
                'passed': False,
                'score': 0,
                'error': str(e),
                'severity': 'unknown'
            }

    def _analyze_cognitive_load(self, mcp_tools: Dict) -> Dict[str, Any]:
        """
        🧠 Analyze cognitive complexity - is the interface overwhelming?

        Checks:
        - Too many choices (paradox of choice)
        - Complex navigation
        - Information overload
        - Unclear primary actions
        """
        eval_func = mcp_tools.get('evaluate_script')

        cognitive_load_js = """
        () => {
            const analysis = {
                choices_count: 0,
                navigation_complexity: 0,
                visible_elements: 0,
                primary_cta_count: 0,
                walls_of_text: []
            };

            // Count interactive choices
            const interactiveElements = document.querySelectorAll('button, a, input[type="button"], input[type="submit"], [role="button"]');
            analysis.choices_count = interactiveElements.length;

            // Count navigation items
            const navLinks = document.querySelectorAll('nav a, [role="navigation"] a');
            analysis.navigation_complexity = navLinks.length;

            // Count primary CTAs (usually styled prominently)
            const prominentButtons = Array.from(interactiveElements).filter(el => {
                const styles = window.getComputedStyle(el);
                const bgColor = styles.backgroundColor;
                const fontSize = parseFloat(styles.fontSize);

                // Heuristic: large, colorful buttons are likely CTAs
                return fontSize > 16 && bgColor !== 'rgba(0, 0, 0, 0)';
            });
            analysis.primary_cta_count = prominentButtons.length;

            // Check for walls of text (paragraphs > 200 words)
            const paragraphs = document.querySelectorAll('p, div');
            paragraphs.forEach(p => {
                const text = p.textContent?.trim();
                if (text) {
                    const wordCount = text.split(/\s+/).length;
                    if (wordCount > 200) {
                        analysis.walls_of_text.push({
                            wordCount: wordCount,
                            preview: text.substring(0, 100) + '...'
                        });
                    }
                }
            });

            // Count total visible elements
            const allElements = document.querySelectorAll('*');
            analysis.visible_elements = Array.from(allElements).filter(el => {
                const styles = window.getComputedStyle(el);
                return styles.display !== 'none' && styles.visibility !== 'hidden';
            }).length;

            return analysis;
        }
        """

        try:
            results = eval_func(function=cognitive_load_js)

            # Calculate cognitive load score
            issues = []

            if results.get('choices_count', 0) > 50:
                issues.append('Too many choices (paradox of choice)')

            if results.get('navigation_complexity', 0) > 15:
                issues.append('Complex navigation menu')

            if results.get('primary_cta_count', 0) > 5:
                issues.append('Unclear primary action (too many CTAs)')

            if len(results.get('walls_of_text', [])) > 2:
                issues.append('Information overload (walls of text)')

            return {
                'passed': len(issues) == 0,
                'score': max(0, 100 - (len(issues) * 25)),
                'issues': issues,
                'details': results,
                'severity': 'high' if len(issues) > 2 else 'medium' if len(issues) > 0 else 'low'
            }

        except Exception as e:
            return {
                'passed': False,
                'score': 0,
                'error': str(e),
                'severity': 'unknown'
            }

    def _evaluate_user_respect(self, mcp_tools: Dict) -> Dict[str, Any]:
        """
        🙏 Evaluate if the design respects users' time, attention, and autonomy

        Checks:
        - Auto-playing media (annoying!)
        - Forced registration walls
        - Cookie consent dark patterns
        - Excessive pop-ups
        """
        eval_func = mcp_tools.get('evaluate_script')

        user_respect_js = """
        () => {
            const disrespects = [];

            // Check for auto-playing media
            const videos = document.querySelectorAll('video');
            const audios = document.querySelectorAll('audio');

            videos.forEach(v => {
                if (v.autoplay && !v.muted) {
                    disrespects.push({
                        type: 'autoplay_video',
                        severity: 'high',
                        reason: 'Auto-playing video with sound is disrespectful'
                    });
                }
            });

            audios.forEach(a => {
                if (a.autoplay) {
                    disrespects.push({
                        type: 'autoplay_audio',
                        severity: 'high',
                        reason: 'Auto-playing audio is disrespectful'
                    });
                }
            });

            // Check for modals/overlays (potential pop-ups)
            const modals = document.querySelectorAll('[role="dialog"], [class*="modal"], [class*="popup"], [class*="overlay"]');
            if (modals.length > 3) {
                disrespects.push({
                    type: 'excessive_modals',
                    count: modals.length,
                    severity: 'medium',
                    reason: 'Too many pop-ups interrupt user flow'
                });
            }

            // Check cookie consent implementation
            const cookieBanners = document.querySelectorAll('[class*="cookie"], [class*="consent"], [id*="cookie"]');
            cookieBanners.forEach(banner => {
                const acceptButtons = banner.querySelectorAll('button');
                if (acceptButtons.length === 1) {
                    disrespects.push({
                        type: 'cookie_dark_pattern',
                        severity: 'high',
                        reason: 'Cookie banner only has Accept button (no Decline)'
                    });
                }
            });

            // Check for registration walls
            const signupForms = document.querySelectorAll('form[action*="signup"], form[action*="register"]');
            const bodyText = document.body.innerText.toLowerCase();
            if (signupForms.length > 0 && (bodyText.includes('must sign up') || bodyText.includes('please register'))) {
                disrespects.push({
                    type: 'forced_registration',
                    severity: 'medium',
                    reason: 'Content locked behind forced registration'
                });
            }

            return {
                disrespects_found: disrespects.length,
                details: disrespects
            };
        }
        """

        try:
            results = eval_func(function=user_respect_js)

            disrespects_count = results.get('disrespects_found', 0)

            return {
                'passed': disrespects_count == 0,
                'score': max(0, 100 - (disrespects_count * 25)),
                'disrespects_found': disrespects_count,
                'details': results.get('details', []),
                'severity': 'high' if disrespects_count > 2 else 'medium' if disrespects_count > 0 else 'low'
            }

        except Exception as e:
            return {
                'passed': False,
                'score': 0,
                'error': str(e),
                'severity': 'unknown'
            }

    def _check_accessibility_empathy(self, mcp_tools: Dict) -> Dict[str, Any]:
        """
        ♿ Check if accessibility is implemented with empathy (not just checkboxes)

        Checks:
        - Alt text quality (is it meaningful or just "image"?)
        - ARIA labels (are they helpful or generic?)
        - Skip links (do they exist?)
        - Focus indicators (visible and clear?)
        """
        eval_func = mcp_tools.get('evaluate_script')

        a11y_empathy_js = """
        () => {
            const empathy_issues = [];

            // Check alt text quality
            const images = document.querySelectorAll('img');
            images.forEach(img => {
                const alt = img.alt;
                if (!alt) {
                    empathy_issues.push({
                        type: 'missing_alt',
                        severity: 'high',
                        element: 'img',
                        reason: 'Screen reader users hear "image" - not helpful'
                    });
                } else if (alt.toLowerCase() === 'image' || alt.toLowerCase() === 'photo' || alt.toLowerCase() === 'picture') {
                    empathy_issues.push({
                        type: 'generic_alt',
                        severity: 'medium',
                        alt: alt,
                        reason: 'Alt text too generic - not descriptive'
                    });
                }
            });

            // Check ARIA label quality
            const ariaElements = document.querySelectorAll('[aria-label]');
            ariaElements.forEach(el => {
                const label = el.getAttribute('aria-label');
                if (label.length < 3 || label.toLowerCase() === 'button' || label.toLowerCase() === 'link') {
                    empathy_issues.push({
                        type: 'generic_aria',
                        severity: 'medium',
                        label: label,
                        reason: 'ARIA label not descriptive enough'
                    });
                }
            });

            // Check for skip links
            const skipLinks = Array.from(document.querySelectorAll('a')).filter(a =>
                a.textContent.toLowerCase().includes('skip') ||
                a.href.includes('#main') ||
                a.href.includes('#content')
            );

            if (skipLinks.length === 0) {
                empathy_issues.push({
                    type: 'no_skip_link',
                    severity: 'medium',
                    reason: 'No skip navigation link for keyboard users'
                });
            }

            // Check focus indicators
            const focusableElements = document.querySelectorAll('a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])');
            let noFocusIndicator = 0;

            focusableElements.forEach(el => {
                const styles = window.getComputedStyle(el);
                if (styles.outline === 'none' && styles.boxShadow === 'none') {
                    noFocusIndicator++;
                }
            });

            if (noFocusIndicator > focusableElements.length * 0.5) {
                empathy_issues.push({
                    type: 'poor_focus_indicators',
                    severity: 'high',
                    count: noFocusIndicator,
                    reason: 'Many elements lack visible focus indicators'
                });
            }

            return {
                issues_count: empathy_issues.length,
                details: empathy_issues
            };
        }
        """

        try:
            results = eval_func(function=a11y_empathy_js)

            issues_count = results.get('issues_count', 0)

            return {
                'passed': issues_count < 3,
                'score': max(0, 100 - (issues_count * 10)),
                'issues_found': issues_count,
                'details': results.get('details', []),
                'severity': 'high' if issues_count > 10 else 'medium' if issues_count > 5 else 'low'
            }

        except Exception as e:
            return {
                'passed': False,
                'score': 0,
                'error': str(e),
                'severity': 'unknown'
            }

    def _validate_ethical_language(self, mcp_tools: Dict) -> Dict[str, Any]:
        """
        💬 Validate language for ethical issues

        Checks:
        - Gendered language ("guys", "mankind")
        - Ableist language ("crazy", "insane")
        - Violent metaphors ("kill", "destroy")
        - Respectful error messages
        """
        eval_func = mcp_tools.get('evaluate_script')

        language_check_js = """
        () => {
            const bodyText = document.body.innerText.toLowerCase();
            const issues = [];

            // Gendered language
            const genderedTerms = ['guys', 'mankind', 'manpower', 'man-hours'];
            genderedTerms.forEach(term => {
                if (bodyText.includes(term)) {
                    issues.push({
                        type: 'gendered_language',
                        term: term,
                        severity: 'low',
                        suggestion: 'Use inclusive alternatives'
                    });
                }
            });

            // Ableist language
            const ableistTerms = ['crazy', 'insane', 'dumb', 'stupid', 'lame'];
            ableistTerms.forEach(term => {
                if (bodyText.includes(term)) {
                    issues.push({
                        type: 'ableist_language',
                        term: term,
                        severity: 'medium',
                        suggestion: 'Use neutral alternatives'
                    });
                }
            });

            // Violent metaphors
            const violentTerms = ['kill', 'destroy', 'crush', 'annihilate'];
            violentTerms.forEach(term => {
                if (bodyText.includes(term)) {
                    issues.push({
                        type: 'violent_metaphor',
                        term: term,
                        severity: 'low',
                        suggestion: 'Use gentler language'
                    });
                }
            });

            return {
                issues_count: issues.length,
                details: issues
            };
        }
        """

        try:
            results = eval_func(function=language_check_js)

            issues_count = results.get('issues_count', 0)

            return {
                'passed': issues_count < 5,
                'score': max(0, 100 - (issues_count * 10)),
                'issues_found': issues_count,
                'details': results.get('details', []),
                'severity': 'medium' if issues_count > 5 else 'low'
            }

        except Exception as e:
            return {
                'passed': False,
                'score': 0,
                'error': str(e),
                'severity': 'unknown'
            }

    def _generate_guilt_trips(self, checks: Dict) -> List[str]:
        """
        😢 Generate guilt-inducing messages based on failures

        This is Litty's signature move - making developers feel the user's pain
        """
        guilt_trips = []

        # Dark patterns guilt trip
        if not checks['dark_patterns']['passed']:
            count = checks['dark_patterns']['dark_patterns_found']
            severity = checks['dark_patterns']['severity']
            phrase = self.guilt_phrases.get(severity, "Eda mone!")

            guilt_trips.append(
                f"{phrase} You have {count} dark patterns manipulating users! "
                f"Would you want your ammachi (grandma) to be tricked like this?"
            )

        # Inclusive design guilt trip
        if not checks['inclusive_design']['passed']:
            issues = checks['inclusive_design']['issues_found']
            guilt_trips.append(
                f"Enthina ithoke? (Why do this?) You have {issues} issues making it hard for "
                f"elderly people and users with disabilities. Think about Kuttan Uncle trying to click "
                f"your tiny buttons with his shaky hands!"
            )

        # Cognitive load guilt trip
        if not checks['cognitive_load']['passed']:
            issues = checks['cognitive_load'].get('issues', [])
            guilt_trips.append(
                f"Shari aylaa mone (This won't do)! Your interface is so complex with "
                f"{', '.join(issues)}. My ammachi would give up after 30 seconds!"
            )

        # User respect guilt trip
        if not checks['user_respect']['passed']:
            count = checks['user_respect']['disrespects_found']
            guilt_trips.append(
                f"Eda mone! You're disrespecting users with {count} annoying patterns! "
                f"Auto-playing videos, forced pop-ups... would YOU tolerate this?"
            )

        # Accessibility empathy guilt trip
        if not checks['accessibility_empathy']['passed']:
            issues = checks['accessibility_empathy']['issues_found']
            guilt_trips.append(
                f"You have {issues} accessibility issues with no empathy! Priya uses a screen reader "
                f"and your alt text just says 'image'. How is that helpful?"
            )

        # Ethical language guilt trip
        if not checks['ethical_language']['passed']:
            issues = checks['ethical_language']['issues_found']
            guilt_trips.append(
                f"Your language has {issues} ethical issues. Using words like 'crazy' and 'stupid' "
                f"- would you talk like this to your teacher or parents?"
            )

        return guilt_trips

    def _generate_user_stories(self, checks: Dict) -> List[Dict[str, Any]]:
        """
        📖 Generate empathy-driven user stories

        Format: "As [persona], I want [need], but I can't because [your issue]"
        """
        user_stories = []

        # Generate stories based on failures
        if not checks['inclusive_design']['passed']:
            user_stories.append({
                'persona': self.user_personas['ammachi']['name'],
                'age': self.user_personas['ammachi']['age'],
                'story': (
                    f"As a 72-year-old grandmother, I want to buy festival sarees online, "
                    f"but I can't because the buttons are too small and the text is tiny. "
                    f"I gave up and called my grandson instead."
                ),
                'impact': 'Lost sale, frustrated user, asks family for help'
            })

        if not checks['accessibility_empathy']['passed']:
            user_stories.append({
                'persona': self.user_personas['visually_impaired']['name'],
                'age': self.user_personas['visually_impaired']['age'],
                'story': (
                    f"As a screen reader user, I want to understand what images show, "
                    f"but I can't because the alt text just says 'image' or is missing entirely. "
                    f"I have no idea what I'm missing."
                ),
                'impact': 'Incomplete experience, feels excluded, leaves site'
            })

        if not checks['cognitive_load']['passed']:
            user_stories.append({
                'persona': self.user_personas['elderly_tech_novice']['name'],
                'age': self.user_personas['elderly_tech_novice']['age'],
                'story': (
                    f"As a 68-year-old who just learned to use internet, I want to pay my electricity bill, "
                    f"but I can't because there are 50 buttons and I'm afraid to click the wrong one. "
                    f"I'll just go to the office tomorrow."
                ),
                'impact': 'Lost conversion, anxiety, prefers offline methods'
            })

        if not checks['user_respect']['passed']:
            user_stories.append({
                'persona': self.user_personas['rural_user']['name'],
                'age': self.user_personas['rural_user']['age'],
                'story': (
                    f"As a teacher in a village with slow internet, I want to download study materials, "
                    f"but I can't because your auto-playing video ate up my mobile data and "
                    f"3 pop-ups appeared before I could even read anything."
                ),
                'impact': 'Wasted data, frustration, never returns to site'
            })

        if not checks['dark_patterns']['passed']:
            user_stories.append({
                'persona': 'Budget-conscious student',
                'age': 22,
                'story': (
                    f"As a student on a tight budget, I wanted to try the free trial, "
                    f"but I can't find how to cancel it anywhere. The confirmation button "
                    f"said 'No thanks, I don't want to save money' which made me feel guilty. "
                    f"I signed up but now I regret it."
                ),
                'impact': 'Unwanted subscription, feels manipulated, tells friends to avoid'
            })

        return user_stories

    def _generate_recommendations(self, checks: Dict) -> List[str]:
        """
        💡 Generate actionable recommendations with Malayali wisdom
        """
        recommendations = []

        if not checks['dark_patterns']['passed']:
            recommendations.append(
                "🙏 Remove dark patterns - Be honest and transparent. "
                "Like we say in Malayalam: 'സത്യം പറ' (Sathyam para - Speak truth). "
                "Your users will trust you more."
            )

        if not checks['inclusive_design']['passed']:
            recommendations.append(
                "👵 Make buttons at least 44x44px and text at least 16px. "
                "Think: 'Could my ammachi use this with her reading glasses?'"
            )

        if not checks['cognitive_load']['passed']:
            recommendations.append(
                "🧠 Simplify your interface. Follow the Malayalam principle: "
                "'എളുപ്പം ആക്കുക' (Eluppam akkuka - Make it simple). "
                "One clear primary action, less clutter."
            )

        if not checks['user_respect']['passed']:
            recommendations.append(
                "🙏 Respect users' time and attention. No auto-play videos, "
                "reasonable cookie consent, easy cancellation. Treat users like "
                "you'd treat guests in your home (മെഹ്മാൻ - Mehman)."
            )

        if not checks['accessibility_empathy']['passed']:
            recommendations.append(
                "♿ Write meaningful alt text and ARIA labels. Imagine describing "
                "your site to someone over the phone - what would you say? "
                "That's your alt text."
            )

        if not checks['ethical_language']['passed']:
            recommendations.append(
                "💬 Use inclusive, respectful language. Say 'everyone' instead of 'guys', "
                "'unexpected' instead of 'crazy'. Language shapes how people feel."
            )

        return recommendations

    def _generate_verdict(self, score: int) -> str:
        """
        ⚖️ Litty's final verdict with Malayali flavor
        """
        if score >= 90:
            return (
                "നല്ലത്! (Nallathu - Good!) You're thinking about users! "
                "Your ammachi would be proud. Keep up the empathy! 🪔✨"
            )
        elif score >= 75:
            return (
                "ശരിയാണ് (Shariyanu - Okay), not bad, but you can do better! "
                "Think more about the elderly, disabled, and non-tech users."
            )
        elif score >= 50:
            return (
                "ഇത് എന്താണ് ഇതിന്റെ അവസ്ഥ? (What is this situation?) "
                "Half your users are struggling! Your ammachi called 3 times "
                "because she couldn't use your site. Do better!"
            )
        else:
            return (
                "ഓഹോ! (Oho!) This is terrible! You're only thinking about yourself! "
                "Elderly people, disabled users, non-tech folks - nobody can use this! "
                "Your ammachi is crying! Fix this immediately! 😢"
            )

    def _calculate_grade(self, score: int) -> str:
        """Calculate letter grade from score"""
        if score >= 95:
            return 'S+'
        elif score >= 90:
            return 'S'
        elif score >= 80:
            return 'A'
        elif score >= 70:
            return 'B'
        elif score >= 60:
            return 'C'
        elif score >= 50:
            return 'D'
        else:
            return 'F'

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()


# Main validation function for Superman to call
def litty_validate_ethics(url: str, mcp_tools: Dict) -> Dict[str, Any]:
    """
    🪔 Litty's main entry point - User Empathy & Ethics Validation

    Args:
        url: Website URL to analyze
        mcp_tools: MCP Chrome DevTools

    Returns:
        Complete ethics analysis with guilt trips and user stories
    """
    litty = LittyEthics()
    return litty.validate_ethics(url, mcp_tools)
