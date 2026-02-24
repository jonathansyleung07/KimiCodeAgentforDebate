# Multi-Agent Debate System

A configurable multi-agent debate system where multiple LLM agents debate on social topics. Agents conduct research, exchange arguments, and engage in structured debates across multiple rounds.

## Features

- 🤖 **Multi-Agent Debate**: Configure multiple AI agents with different models and perspectives
- 📚 **Research Phase**: Agents conduct independent research before debating
- 📝 **Structured Debates**: Multi-round debates with configurable word counts
- 🗂️ **Organized Output**: Research and speeches saved in structured folders
- 🔧 **Configurable**: All settings defined in `OBJECTIVE.md`
- 🌐 **OpenRouter Integration**: Support for multiple LLM providers via OpenRouter

## Quick Start

### 1. Clone/Navigate to the Project Directory

```bash
cd /path/to/debate-system
```

### 2. Create Conda Environment

```bash
# Create environment with Python 3.12
conda create -n debate python=3.12 -y

# Activate environment
conda activate debate
```

### 3. Install Dependencies

```bash
pip install openai python-dotenv pyyaml
```

Or using a requirements file:

```bash
pip install -r requirements.txt
```

### 4. Configure API Credentials

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual OpenRouter API key
# Get your API key from: https://openrouter.ai/keys
```

Edit `.env`:
```
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
OPENROUTER_API_URL=https://openrouter.ai/api/v1
```

### 5. Configure the Debate

Edit `OBJECTIVE.md` to customize:
- Debate topic
- Number of debaters
- LLM models to use
- Number of rounds
- Words per speech
- Research rounds

### 6. Run the Debate

```bash
# Run the main debate orchestrator
python debate.py
```

## Project Structure

```
.
├── OBJECTIVE.md          # Debate configuration and parameters
├── README.md             # This file
├── .env                  # API credentials (gitignored)
├── .env.example          # Example environment file
├── .gitignore            # Git ignore rules
├── debate.py             # Main debate orchestrator
├── requirements.txt      # Python dependencies
├── agents/
│   ├── __init__.py
│   └── debater.py        # Debater agent class
├── utils/
│   ├── __init__.py
│   └── parser.py         # OBJECTIVE.md parser
├── memory/               # Research materials (created at runtime)
│   ├── peter/
│   ├── paul/
│   └── mary/
└── speeches/             # Debate speeches (created at runtime)
    ├── round_1/
    ├── round_2/
    └── round_3/
```

## Configuration (OBJECTIVE.md)

The `OBJECTIVE.md` file defines all aspects of the debate:

| Section | Description |
|---------|-------------|
| Debate Topic | The central question being debated |
| Debaters | Agent configurations (model, language, stance) |
| Debate Parameters | Rounds, word counts, research rounds |
| Agent Behavior Rules | How agents conduct research and debate |
| Output Format | Structure of research and speech files |

## Supported Models (via OpenRouter)

Popular models available on OpenRouter:
- `openai/gpt-4o`
- `openai/gpt-4o-mini`
- `anthropic/claude-3.5-sonnet`
- `anthropic/claude-3-opus`
- `google/gemini-pro`
- `google/gemini-flash`
- `meta-llama/llama-3.1-70b-instruct`
- `mistralai/mistral-large`

See [OpenRouter models](https://openrouter.ai/models) for the full list.

## Example Debate Flow

1. **Research Phase**
   - Each agent conducts 2 rounds of research
   - Research saved to `memory/{alias}/research_round_{n}.md`

2. **Debate Phase - Round 1**
   - Peter speaks first (loads his research)
   - Paul responds (loads Peter's speech + his research)
   - Mary responds (loads Peter's and Paul's speeches + her research)

3. **Debate Phase - Round 2**
   - Speaking order rotates
   - Each agent addresses previous arguments

4. **Debate Phase - Round 3**
   - Final round of arguments
   - Agents summarize their positions

## Customization

### Changing the Topic

Edit `OBJECTIVE.md`:
```markdown
## Debate Topic
Your custom debate topic here?
```

### Adding More Debaters

Add a new debater section in `OBJECTIVE.md`:
```markdown
#### Debater 4: Alice
- **Alias**: Alice
- **Model**: mistralai/mistral-large
- **Language**: English
- **Role**: Your role description
- **Stance**: Your stance description
```

### Changing Models

Simply update the model name in `OBJECTIVE.md`. Ensure the model is available on OpenRouter.

## Troubleshooting

### API Key Issues
```
Error: 401 Unauthorized
```
- Check your `OPENROUTER_API_KEY` in `.env`
- Verify the key is active at https://openrouter.ai/keys

### Model Not Found
```
Error: 404 Model not found
```
- Verify the model name in `OBJECTIVE.md`
- Check available models at https://openrouter.ai/models

### Rate Limits
```
Error: 429 Too Many Requests
```
- OpenRouter has rate limits based on your tier
- Add delays between requests in `debate.py`

## License

MIT License - Feel free to use and modify for your own debates.

## Contributing

This is a learning project for `kimi-cli`. Contributions and improvements are welcome!
