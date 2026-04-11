# 07. Deployment View

## Topology

The Mars Rover Control System is a **single-process CLI application**. There is no network, no database, and no containerisation required.

```
┌─────────────────────────────────────┐
│  Developer / Operator Machine       │
│                                     │
│  Python 3.12 runtime                │
│  ┌─────────────────────────────┐    │
│  │  mars_rover (Python pkg)    │    │
│  │  python -m mars_rover       │    │
│  └─────────────────────────────┘    │
│                                     │
│  stdin ──▶  process  ──▶  stdout    │
└─────────────────────────────────────┘
```

## Running the Application

```bash
# Pipe an input file
python -m mars_rover < input.txt

# Interactive (type input manually, Ctrl-D to finish)
python -m mars_rover
```

## Input / Output Example

**Input**
```
5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM
```

**Output**
```
1 3 N
5 1 E
```

## Development Setup

```bash
# Install dependencies (dev extras)
pip install -e ".[dev]"

# Run tests
pytest

# Run linters
ruff check .
black --check .
```
