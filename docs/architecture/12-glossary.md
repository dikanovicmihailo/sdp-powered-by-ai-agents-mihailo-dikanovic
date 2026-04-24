# 12. Glossary

| Term | Definition |
|------|-----------|
| **Plateau** | The rectangular grid on Mars within which rovers operate. Defined by its upper-right corner `(width, height)`; the lower-left corner is always `(0, 0)`. |
| **Rover** | An autonomous vehicle deployed on the plateau. Holds a position `(x, y)` and a heading. Processes commands one at a time. |
| **Position** | A coordinate pair `(x, y)` on the plateau grid. `x` increases eastward; `y` increases northward. |
| **Heading** | The cardinal direction a rover is facing: `N` (North), `E` (East), `S` (South), or `W` (West). |
| **Command** | A single instruction sent to a rover. Valid values: `L` (turn left 90°), `R` (turn right 90°), `M` (move one step forward in the current heading direction). |
| **Command String** | A sequence of commands for a single rover, e.g. `LMLMLMLMM`. |
| **Turn Left (L)** | Rotate the rover 90° counter-clockwise without moving. `N → W → S → E → N`. |
| **Turn Right (R)** | Rotate the rover 90° clockwise without moving. `N → E → S → W → N`. |
| **Move Forward (M)** | Advance the rover one grid step in its current heading direction. Ignored if the move would leave the plateau. |
| **Safe-Stop** | The behaviour where a rover ignores a move command that would take it outside the plateau (or into an obstacle), remaining at its current position. |
| **Obstacle** | *(Optional extension)* A cell on the plateau that a rover cannot enter. Triggers a safe-stop before the blocked cell. |
| **Mission** | The complete execution of all command strings for all rovers on a given plateau. |
| **Operator** | The human (or system) that provides the plateau definition, rover starting positions, and command strings. |
| **InputParser** | The adapter component responsible for converting raw stdin text into domain objects (`Plateau`, `Rover`, `Command` list). |
| **OutputFormatter** | The adapter component responsible for converting final `Rover` state into the `x y HEADING` output string. |
| **MissionController** | The application-layer component that orchestrates a mission — iterating over rovers and applying their command sequences. |
| **Hexagonal Architecture** | An architectural style (also called Ports & Adapters) that isolates the domain from I/O by placing all external concerns in adapter classes. |
| **ADR** | Architecture Decision Record — a short document capturing a significant design decision, its context, and its consequences. |
| **arc42** | A lightweight, pragmatic template for software architecture documentation with 12 standardised chapters. |
| **C4 Model** | A hierarchical diagramming approach (Context → Container → Component → Code) for visualising software architecture. |
| **PlantUML** | A text-based diagramming tool used to author C4 diagrams in this project. |
