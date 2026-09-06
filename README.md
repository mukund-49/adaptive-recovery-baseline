# Adaptive Recovery Policy Selection - Baseline

This repository contains the runnable baseline for the CSE 598 Agentic AI capstone proposal.

The baseline is a tool utilizing LLM agent implemented in Python using the Groq API and the `openai/gpt-oss-20b` model. The agent operates in a controlled movie-information(just an example, this has nothing to do with the actual topic in hand) workspace and can list, read, and search files to complete a natural-language task.

## Dependencies

- Python 3
- `groq`
- `python-dotenv`

Install the required packages with:

```bash
pip install -r requirements.txt
```

## Setup

### 1. Create and activate a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the Groq API key

A Groq API key is required to run the baseline.

Create a `.env` file in the root directory:

```text
GROQ_API_KEY=your_api_key_here
```

## Running the Baseline

Run:

```bash
python agent.py
```

The natural language task to be executed is specified at the bottom of `agent.py`.

## Input

The controlled input files used by the agent are located in:

```text
workspace/
```

The workspace contains movie information such as actors, directors, movies, ratings, upcoming movies, and awards.

## Output

The agent prints its tool calls, observations, and final answer to the terminal.

A JSON record of each run is also saved automatically in:

```text
results/
```


Example results are also attached under the 'examples/' , there is a successful trajectory and an unsuccessul trajectory stored in json format of the task "According to the available files, find the benchmark rating of Robert Pattinson's upcoming Batman movie."
