# Justice League Mission Debate Protocol

## 🎯 Core Principle

**Every Justice League mission MUST include full team debate before execution.**

User preference learned: 2025-10-31
User quote: *"yes, make it happen for every mission"*

## 📋 Debate Requirements

### Who Participates

1. **Oracle** (always) - Provides capability analysis and historical data
2. **Relevant heroes** for the mission type - Present positions and evidence
3. **Superman** (always) - Makes final decision based on team input

### Sequential Thinking Limits

- **Heroes**: 3-7 steps each when presenting positions
- **Oracle**: 3-5 steps during capability analysis
- **Superman**: 5-7 steps when making final decision

### Conversation Style

**✅ SHOW**: Full live dialogue with back-and-forth exchanges
**❌ AVOID**: Summaries like "My agents fighting with each other"

## 🎬 Mission Flow (11 Steps)

1. **Superman announces mission** to team
2. **Oracle queries** hero capability database
3. **Oracle provides** capability analysis with context
4. **Relevant heroes present** positions with sequential thinking
5. **Heroes question** each other's proposals
6. **Heroes provide** evidence and benchmarks
7. **Oracle asks** mission-critical question to reframe debate
8. **Superman analyzes** all input with sequential thinking
9. **Superman makes** informed decision
10. **Team confirms** consensus
11. **Selected hero executes** mission

## 📊 Output Format

### ✅ Correct Format (Live Conversation)

```
🦸 Superman: "Team, we have a mission: Export Figma file to PNG. Who's best for this?"

🔮 Oracle: [Scanning] Querying Justice League capability database...
🔮 Oracle: [Analysis] Found 3 heroes with Figma export capabilities
🔮 Oracle: [Context] Quicksilver: 3x faster, Hawkman: 100% reliable

🦅 Hawkman: [Position] I can handle this mission reliably.
🦅 Hawkman: [Sequential Thinking - Step 1] I've exported 177+ frames successfully
🦅 Hawkman: [Sequential Thinking - Step 2] My sequential approach prevents API rate limiting
🦅 Hawkman: [Evidence] K-12 export: 177 frames, 20 minutes, 0 failures

💨 Quicksilver: [Position] I'm optimized for exactly this type of mission.
💨 Quicksilver: [Sequential Thinking - Step 1] Parallel processing: 8 concurrent workers
💨 Quicksilver: [Sequential Thinking - Step 2] Batch API reduces calls by 85%
💨 Quicksilver: [Evidence] Today's benchmark: 484/484 frames, 4m 50s, 100% success

🎯 Green Arrow: [Question to Quicksilver] What about error handling at 8x speed?

💨 Quicksilver: [Response] Each worker operates independently with retry logic
💨 Quicksilver: [Evidence] 0 failures out of 484 frames this morning

🦇 Batman: [Investigation] Checking production readiness...
🦇 Batman: [Validation] ✅ Autonomous error recovery verified

🔮 Oracle: ⚡ MISSION-CRITICAL QUESTION:
🔮 Oracle: "What's more valuable: saving 15 minutes, or ensuring 100% reliability?"
🔮 Oracle: [Analysis] Both have 100% success rates historically

⚡ Flash: [Performance Analysis] Quicksilver is 4x faster per-frame
⚡ Flash: ✅ Performance winner: Quicksilver

🦸 Superman: [Analyzing Team Input] Let me analyze all perspectives...
🦸 Superman: [Sequential Thinking - Step 1] Hawkman: Reliable, slower (20 min)
🦸 Superman: [Sequential Thinking - Step 2] Quicksilver: Reliable, fast (5 min)
🦸 Superman: [Sequential Thinking - Step 3] Batman validated error handling ✅
🦸 Superman: [Sequential Thinking - Step 4] Oracle: both 100% success rates
🦸 Superman: [Sequential Thinking - Step 5] Flash: 4x speed advantage verified
🦸 Superman: [Decision Logic] Speed + Reliability = Quicksilver

🦸 Superman: ✅ DECISION: Quicksilver leads this mission

Team Status: ✅ Unanimous agreement

💨 Quicksilver: "Ready for high-speed operations: 8 concurrent workers deployed!"
```

### ❌ Incorrect Format (Summaries)

```
My agents fighting with each other

Superman's orders, investigated independently, debated with each other,
and reached a better solution together!

Key Highlights:
- Batman investigated independently and found 3 CRITICAL violations
- Artemis confirmed the evidence
- Oracle asked the mission-critical question
- Superman made the right call: Build with accessibility NOW
```

**Why is the summary bad?**
- User doesn't see HOW the decision was made
- No sequential thinking visible
- No back-and-forth questioning
- No evidence presentation
- Missing the engaging superhero banter
- Loses transparency of the process

## 🎯 Mission Type → Hero Mapping

### Figma Frame Export

**Recommended**: Quicksilver, Hawkman
**Default**: Quicksilver
**Fallback**: Hawkman
**Decision factors**:
- Speed requirement (Quicksilver: 3x faster)
- Reliability (Both: 100%)
- Frame count (Large: Quicksilver, Small: Either)

### Figma-to-Code

**Recommended**: Artemis
**Supporting**: Vision Analyst, Green Arrow, Oracle
**Decision factors**:
- Component complexity (Simple: Artemis alone, Complex: Add Vision Analyst)
- Accuracy requirement (>95%: Image-to-HTML, 70-85%: Figma API)
- Time constraint (<30 min: Figma API, 60-90 min: Image-to-HTML)

### Accessibility Testing

**Recommended**: Batman, Wonder Woman
**Decision factors**:
- WCAG level (AA: Wonder Woman, Investigation: Batman)
- Critical violations (Batman detects, Wonder Woman validates)

### Performance Testing

**Recommended**: Flash
**Supporting**: Aquaman
**Decision factors**:
- Type (Speed: Flash, Network: Aquaman)

### Visual Validation

**Recommended**: Green Arrow, Green Lantern
**Decision factors**:
- Type (WYSIWYG: Green Arrow, Regression: Green Lantern)

### Responsive Design

**Recommended**: Plastic Man
**Decision factors**:
- Breakpoint-first approach increases success 23%

## 💡 Benefits of Mission Debates

1. **Better decisions** through collaboration
2. **Multiple perspectives** prevent blind spots
3. **Evidence-based** mission planning
4. **Transparent reasoning** process visible to user
5. **Team learns** from each debate
6. **User sees HOW** decisions are made, not just WHAT

## 📚 Related Documentation

- `/data/justice_league_hero_capabilities.json` - Hero capability registry
- `/data/oracle_project_patterns.json` - Oracle user preferences
- `/knowledge_base/NARRATOR_STYLE_GUIDE.md` - Narrator personality styles
- `/test_inter_agent_debate.py` - Debate system test examples

## 🚀 Implementation Status

- ✅ Hero capability registry created
- ✅ Oracle preference stored
- ✅ Narrator debate methods implemented
- ✅ Test suite validates debate flow
- 🔄 Superman coordinator integration (in progress)
- ⏳ All mission types debate workflow (pending)

## 🔮 Oracle's Learning

**Preference ID**: `mission_debates`
**Priority**: HIGH
**Applies to**: All Justice League missions
**Learned from**: User session 2025-10-31

Oracle will automatically:
- Query capability database when missions announced
- Provide historical performance data
- Ask mission-critical questions
- Track debate outcomes for future learning
