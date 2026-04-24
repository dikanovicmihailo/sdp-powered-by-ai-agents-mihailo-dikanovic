# User Story Inventory — Mars Rover Kata

## Prioritization Note

This backlog uses **value-weighted prioritization**, not a strict Pareto 80/20 split.

The 5 Core stories represent 50% of the story count but deliver ~80% of the working system value. In a 10-story kata this is expected: the domain is small enough that there is no long tail of low-value stories to cut. Every story here earns its place. The 80/20 rule describes the *value ratio*, not the *story count ratio* — and that ratio holds.

If this were a 50-story backlog, the Core tier would contain ~10 stories (20%). At 10 stories, 5 is the honest answer.

---

## Story Map

| ID | File | Title | Layer | Priority | Status |
|----|------|-------|-------|----------|--------|
| PLATEAU-STORY-001 | [plateau.md](plateau.md) | Define the plateau | Domain | 🔴 Core | ✅ Implemented |
| ROVER-STORY-001 | [deploy-rover.md](deploy-rover.md) | Deploy a rover | Domain | 🔴 Core | ✅ Implemented |
| NAV-STORY-001 | [navigate-rover.md](navigate-rover.md) | Navigate a rover | Domain | 🔴 Core | ✅ Implemented |
| CLI-STORY-002 | [report-positions.md](report-positions.md) | Report final positions | Adapter | 🔴 Core | ✅ Implemented |
| NAV-STORY-002 | [boundary-safe-stop.md](boundary-safe-stop.md) | Boundary safe-stop | Domain | 🔴 Core | ✅ Implemented |
| MISSION-STORY-001 | [multi-rover-mission.md](multi-rover-mission.md) | Multi-rover mission | Application | 🟡 Secondary | ✅ Implemented |
| CLI-STORY-001 | [cli-input.md](cli-input.md) | CLI pipe input | Adapter | 🟡 Secondary | ✅ Implemented |
| CLI-STORY-003 | [input-validation.md](input-validation.md) | Input validation & errors | Adapter | 🟡 Secondary | ✅ Implemented |
| NAV-STORY-003 | [obstacle-detection.md](obstacle-detection.md) | Obstacle detection | Domain | 🟢 Optional | ✅ Implemented |
| NAV-STORY-004 | [extensible-commands.md](extensible-commands.md) | Extensible command types | Domain | 🟢 Optional | ✅ Implemented |

---

## Pareto Split

The value distribution holds even though the story count split is 50/30/20, not 80/20:

| Tier | Stories | Story count | Value delivered |
|------|---------|-------------|-----------------|
| 🔴 Core | PLATEAU-STORY-001 → NAV-STORY-002 | 5 (50%) | ~80% |
| 🟡 Secondary | MISSION-STORY-001 → CLI-STORY-003 | 3 (30%) | ~15% |
| 🟢 Optional | NAV-STORY-003 → NAV-STORY-004 | 2 (20%) | ~5% |

The story count column and the value column measure different things. 50% of stories deliver 80% of the value — that asymmetry is the point. A strict 80/20 rule applied to story count would mean 2 Core stories, which would exclude `Navigate a rover` and `Report final positions`. That's wrong for a 10-story kata with no filler.

---

## Domain Breakdown

### PLATEAU Domain
- **PLATEAU-STORY-001** — Define the plateau (Core)

### ROVER Domain
- **ROVER-STORY-001** — Deploy a rover (Core)

### NAV Domain (Navigation/Commands)
- **NAV-STORY-001** — Navigate a rover (Core)
- **NAV-STORY-002** — Boundary safe-stop (Core)
- **NAV-STORY-003** — Obstacle detection (Optional)
- **NAV-STORY-004** — Extensible command types (Optional)

### MISSION Domain (Application Layer)
- **MISSION-STORY-001** — Multi-rover mission (Secondary)

### CLI Domain (Adapter Layer)
- **CLI-STORY-001** — CLI pipe input (Secondary)
- **CLI-STORY-002** — Report final positions (Core)
- **CLI-STORY-003** — Input validation & errors (Secondary)

---

## Story Bundle Structure

Each story follows the **Original + FE + BE + INFRA** decomposition:

- **Original Story**: `{DOMAIN}-STORY-{N}` — User-facing feature description
- **Frontend Sub-Story**: `{DOMAIN}-FE-{N}.{X}` — UI/interface concerns
- **Backend Sub-Story**: `{DOMAIN}-BE-{N}.{X}` — Domain logic and business rules
- **Infrastructure Sub-Story**: `{DOMAIN}-INFRA-{N}.{X}` — Deployment, persistence, external services

All scenarios use **GIVEN-WHEN-THEN** format with unique scenario IDs: `{STORY-ID}-S{N}`

---

## Progress Tracker

 - [x] PLATEAU-STORY-001 Define the plateau
 - [x] ROVER-STORY-001 Deploy a rover
 - [x] NAV-STORY-001 Navigate a rover
 - [x] CLI-STORY-002 Report final positions
 - [x] NAV-STORY-002 Boundary safe-stop
 - [x] MISSION-STORY-001 Multi-rover mission
 - [x] CLI-STORY-001 CLI pipe input
 - [x] CLI-STORY-003 Input validation & errors
 - [x] NAV-STORY-003 Obstacle detection
 - [x] NAV-STORY-004 Extensible command types

---

## Architecture References

All stories link to specific sections in the [architecture documentation](../architecture/):

- **Building Blocks**: [05-building-blocks.md](../architecture/05-building-blocks.md) — Component responsibilities
- **Solution Strategy**: [04-solution-strategy.md](../architecture/04-solution-strategy.md) — Hexagonal architecture, Command pattern
- **Functional Requirements**: [01-introduction.md](../architecture/01-introduction.md) — FR-1 through FR-7
- **Quality Requirements**: [10-quality-requirements.md](../architecture/10-quality-requirements.md) — QS-1 through QS-6
- **Constraints**: [02-constraints.md](../architecture/02-constraints.md) — DC-1 through DC-6, TC-1 through TC-3
- **Risks & Technical Debt**: [11-risks-and-technical-debts.md](../architecture/11-risks-and-technical-debts.md) — R-1 through R-3, TD-1 through TD-4
