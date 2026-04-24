# 01. Introduction and Goals

## What is the Mars Rover Kata?

The Mars Rover Kata is a classic software design exercise. A rover is deployed onto a rectangular plateau on Mars. An operator sends it a sequence of commands — turn left (`L`), turn right (`R`), or move forward (`M`). The rover must navigate the grid, maintain its position and orientation, and never leave the plateau. An optional extension adds obstacle detection.

The kata is small enough to implement in an afternoon, but rich enough to practice clean architecture, domain modelling, and test-driven development.

---

## Functional Requirements

| ID   | Requirement |
|------|-------------|
| FR-1 | The system accepts a plateau size defined by its upper-right corner coordinates (e.g. `5 5`); the lower-left corner is always `0 0` |
| FR-2 | The system accepts one or more rovers, each with an initial position `(x, y)` and a cardinal heading (`N`, `E`, `S`, `W`) |
| FR-3 | Each rover receives a command string composed of: `L` (turn left 90°), `R` (turn right 90°), `M` (move one step forward) |
| FR-4 | Rovers are processed sequentially — a rover completes all its commands before the next one starts |
| FR-5 | The system reports the final position and heading of every rover |
| FR-6 | A rover must not move outside the plateau boundaries |
| FR-7 | *(Optional)* The system detects obstacles on the plateau; a rover stops before hitting one and reports its last safe position |

---

## Quality Goals

| Priority | Quality Goal | Scenario |
|----------|-------------|----------|
| 1 | **Correctness** | Given any valid input, the system always produces the correct final positions |
| 2 | **Safety** | A rover never moves to an invalid position (out of bounds or occupied by an obstacle) |
| 3 | **Testability** | All domain rules are exercisable through unit tests with no I/O setup required |
| 4 | **Extensibility** | New command types or movement strategies can be added without modifying existing domain logic |
| 5 | **Readability** | The code structure reflects the domain language — `Rover`, `Plateau`, `Heading`, `Command` |

---

## Stakeholders

| Stakeholder | Interest |
|-------------|----------|
| **Operator** | Issue commands and receive accurate final rover positions |
| **Developer** | A clean, well-structured codebase that is easy to extend and test |
| **Course Student** | Understand how arc42 and C4 apply to a real (if small) system |
