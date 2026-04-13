# 10. Quality Requirements

## Quality Tree

```
Quality
├── Correctness
│   ├── Accurate position tracking
│   └── Correct heading rotation (L/R)
├── Safety
│   ├── Boundary enforcement
│   └── Obstacle avoidance (optional)
├── Testability
│   ├── Domain testable without I/O
│   └── Adapters testable with plain strings
├── Extensibility
│   ├── New command types
│   └── New movement strategies
└── Readability
    ├── Domain language in code
    └── Single responsibility per class
```

---

## Quality Scenarios

| ID   | Quality Goal | Stimulus | Response | Measure |
|------|-------------|----------|----------|---------|
| QS-1 | **Correctness** | Operator sends `1 2 N` + `LMLMLMLMM` | System outputs `1 3 N` | Output matches expected result exactly |
| QS-2 | **Correctness** | Operator sends `3 3 E` + `MMRMMRMRRM` | System outputs `5 1 E` | Output matches expected result exactly |
| QS-3 | **Safety** | Rover at `(0, 0, S)` receives command `M` | Rover stays at `(0, 0, S)` | Position unchanged; no exception raised |
| QS-4 | **Safety** | Rover at `(5, 5, N)` on a `5 5` plateau receives `M` | Rover stays at `(5, 5, N)` | Position unchanged; no exception raised |
| QS-5 | **Testability** | Developer writes a unit test for `MoveForward` | Test instantiates `Plateau`, `Rover`, `MoveForward` directly | Test runs in < 1 ms with no mocking or file I/O |
| QS-6 | **Extensibility** | Developer adds a new `U-Turn` command (`U`) | New `UTurn` class added; `InputParser` mapping updated | Zero changes to `Rover`, `Plateau`, `Heading`, or `MissionController` |
| QS-7 | **Readability** | New developer reads `domain/rover.py` | Class names, method names, and variable names match the kata vocabulary | Code review passes without terminology questions |
