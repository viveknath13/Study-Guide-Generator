# Study Guide Generator

A small multi-agent pipeline that turns any topic into a beginner-friendly study guide. It runs locally using [Ollama](https://ollama.com) and [LangChain](https://python.langchain.com), so no API keys or cloud services are needed.

## How It Works

Four agents run in sequence, each making one LLM call with its own system prompt:

| # | Agent | Input | Output |
|---|-------|-------|--------|
| 1 | `planner_agent` | Topic | An outline with 3 short study sections |
| 2 | `teacher_agent` | Topic + outline | Short beginner-friendly notes |
| 3 | `quiz_agent` | Topic + notes | 3 short review questions |
| 4 | `conclusion_agent` | Topic + notes | 3 short concluding takeaways |

```
Topic ──► Planner ──► Teacher ──► Quiz
                          │
                          └─────► Conclusion
```

The final study guide combines the **outline**, **review questions**, and **conclusion** into one Markdown-formatted output.

Each agent logs how long it took, so you can see where time is spent.

## Requirements

- Python 3.9+
- [Ollama](https://ollama.com/download) installed and running
- The `qwen3:8b` model pulled locally
- The `langchain-ollama` package

## Setup

1. **Install Ollama** from https://ollama.com/download

2. **Pull the model:**
   ```bash
   ollama pull qwen3:8b
   ```

3. **Install the Python dependency:**
   ```bash
   pip install langchain-ollama
   ```

## Usage

Make sure Ollama is running, then start the script (replace `study_guide.py` with your file name):

```bash
python study_guide.py
```

Enter a topic when prompted:

```
Warming the model...
Model is ready for you....

Enter the study Topic: Photosynthesis
calling agent planer_agent...
finished planer_agent in 8.2s
calling agent teacher_agent...
finished teacher_agent in 12.5s
...
```

The finished study guide is printed to the terminal.

## Example Output

```markdown
##Study Guide: Photosynthesis

## Outline
1. What is photosynthesis?
2. The light-dependent reactions
3. The Calvin cycle

## Review Question
1. ...
2. ...
3. ...

##Conculsion
1. ...
2. ...
3. ...
```

## Configuration

| Setting | Where | Default |
|---------|-------|---------|
| Model | `MODEL = ChatOllama(model=...)` | `qwen3:8b` |
| Temperature | `MODEL = ChatOllama(temperature=...)` | `0` (deterministic) |
| Agent behavior | System prompt string in each agent function | See code |

To use a different model, pull it with `ollama pull <model>` and change the `model` argument.

## Project Structure

```
.
├── study_guide.py   # The full pipeline (agents + CLI entry point)
└── README.md
```

### Key Functions

- `ask(system, user)` runs a single LLM call and strips any `<think>...</think>` reasoning blocks that Qwen3 emits.
- `run_agent(name, system, user)` wraps `ask()` and logs timing.
- `build_study_guide(topic)` runs every agent in order and assembles the final output.

## Notes

- The model is "warmed up" with a dummy call at startup so the first real agent call isn't slowed by model loading.
- The teacher's notes are used as input for the quiz and conclusion agents, but they are not included in the final printed guide. To include them, add a `## Notes` section to the return value of `build_study_guide`.
- Temperature is set to `0`, so the same topic will produce nearly identical output each run.

## Troubleshooting

- **Connection error:** Make sure Ollama is running (`ollama serve`).
- **Model not found:** Run `ollama pull qwen3:8b`.
- **Slow responses:** Try a smaller model, or run Ollama on a machine with a GPU.

