# Multi-Agent Debate Configuration

## Debate Topic
How to solve the potential problem of mass unemployment in the post-AI era?

## Debate Configuration

### Topic Details
- **Topic**: How to solve the potential problem of mass unemployment in the post-AI era?
- **Description**: A structured debate exploring solutions, policies, and societal adaptations needed to address workforce displacement caused by artificial intelligence advancement.

### Debaters (3 Agents)

#### Debater 1: Peter
- **Alias**: Peter
- **Model**: openai/gpt-4o
- **Language**: English
- **Role**: Technology Optimist - believes AI will create new opportunities and economic growth
- **Stance**: Pro-active adaptation, emphasis on education and reskilling

#### Debater 2: Paul
- **Alias**: Paul
- **Model**: anthropic/claude-3.5-sonnet
- **Language**: English
- **Role**: Policy Advocate - focuses on government intervention and social safety nets
- **Stance**: Universal Basic Income (UBI) and strong regulatory frameworks

#### Debater 3: Mary
- **Alias**: Mary
- **Model**: google/gemini-pro
- **Language**: English
- **Role**: Social Critic - emphasizes human value beyond work and societal restructuring
- **Stance**: Post-work society, community-based economics, redefining human purpose

### Debate Parameters

- **Number of Rounds**: 3
- **Words per Speech**: 1000 words (approximately)
- **Research Rounds**: 2 rounds of research before debate begins

### Directory Structure

```
./
├── memory/
│   ├── peter/          # Peter's research and reference materials
│   ├── paul/           # Paul's research and reference materials
│   └── mary/           # Mary's research and reference materials
├── speeches/
│   ├── round_1/
│   │   ├── speaker_1_peter.md
│   │   ├── speaker_2_paul.md
│   │   └── speaker_3_mary.md
│   ├── round_2/
│   │   ├── speaker_1_peter.md
│   │   ├── speaker_2_paul.md
│   │   └── speaker_3_mary.md
│   └── round_3/
│       ├── speaker_1_peter.md
│       ├── speaker_2_paul.md
│       └── speaker_3_mary.md
├── OBJECTIVE.md        # This configuration file
└── .env                # API credentials (not in git)
```

### Agent Behavior Rules

#### Research Phase
1. Each agent conducts 2 rounds of independent research
2. Research materials saved to respective `memory/{alias}/` folder
3. Research should include:
   - Academic perspectives on AI and employment
   - Historical precedents of technological displacement
   - Economic theories and policy proposals
   - Real-world case studies and pilot programs
4. Format: Human-readable markdown with clear organization

#### Debate Phase
1. Speaking order: Peter → Paul → Mary (rotates each round)
2. Before each speech, agent reads:
   - All previous speeches from other debaters
   - Own memory/reference folder
3. Speech requirements:
   - Address previous arguments
   - Support with research from memory
   - Advance own position while acknowledging valid points
   - Approximately 1000 words per speech
4. Save speeches to `speeches/round_{n}/speaker_{m}_{alias}.md`

### Output Format

#### Research Files (`memory/{alias}/research_round_{n}.md`)
```markdown
# Research Round {n} - {Topic}

## Key Findings
...

## Sources & References
...

## Arguments to Use
...

## Counter-arguments to Prepare
...
```

#### Speech Files (`speeches/round_{n}/speaker_{m}_{alias}.md`)
```markdown
# Round {n}, Speaker {m} - {Alias}

## Speech

[Content approximately 1000 words]

## Key Points Summary
- Point 1
- Point 2
- Point 3
```

### API Configuration
- **API Provider**: OpenRouter
- **Required Environment Variables**:
  - `OPENROUTER_API_KEY` - Your OpenRouter API key
  - `OPENROUTER_API_URL` - https://openrouter.ai/api/v1
  - `YOUR_SITE_URL` - (Optional) For OpenRouter rankings
  - `YOUR_SITE_NAME` - (Optional) For OpenRouter rankings

### Success Criteria
- All research materials are comprehensive and well-organized
- Each debate round contains 3 speeches with substantive arguments
- Debates demonstrate engagement with opponents' points
- Final outputs are human-readable and educational
