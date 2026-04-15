# User Story Inventory — Mars Rover Kata

Pareto-prioritized: the first 5 stories (~50% of total) deliver ~80% of the working system value.

---

## Story Map

| ID | File | Title | Layer | Priority | Status |
|----|------|-------|-------|----------|--------|
| PLATEAU-STORY-001 | [plateau.md](plateau.md) | Define the plateau | Domain | 🔴 Core | ⬜ Todo |
| ROVER-STORY-001 | [deploy-rover.md](deploy-rover.md) | Deploy a rover | Domain | 🔴 Core | ⬜ Todo |
| NAV-STORY-001 | [navigate-rover.md](navigate-rover.md) | Navigate a rover | Domain | 🔴 Core | ⬜ Todo |
| CLI-STORY-002 | [report-positions.md](report-positions.md) | Report final positions | Adapter | 🔴 Core | ⬜ Todo |
| NAV-STORY-002 | [boundary-safe-stop.md](boundary-safe-stop.md) | Boundary safe-stop | Domain | 🔴 Core | ⬜ Todo |
| MISSION-STORY-001 | [multi-rover-mission.md](multi-rover-mission.md) | Multi-rover mission | Application | 🟡 Secondary | ⬜ Todo |
| CLI-STORY-001 | [cli-input.md](cli-input.md) | CLI pipe input | Adapter | 🟡 Secondary | ⬜ Todo |
| CLI-STORY-003 | [input-validation.md](input-validation.md) | Input validation & errors | Adapter | 🟡 Secondary | ⬜ Todo |
| NAV-STORY-003 | [obstacle-detection.md](obstacle-detection.md) | Obstacle detection | Domain | 🟢 Optional | ⬜ Todo |
| NAV-STORY-004 | [extensible-commands.md](extensible-commands.md) | Extensible command types | Domain | 🟢 Optional | ⬜ Todo |

---

## Pareto Split

```
🔴 Core (PLATEAU-STORY-001 → NAV-STORY-002)   ████████████████████  80% of system value
🟡 Secondary (MISSION-STORY-001 → CLI-STORY-003)    ████░░░░░░░░░░░░░░░░  15% of system value
🟢 Optional  (NAV-STORY-003 → NAV-STORY-004)    ██░░░░░░░░░░░░░░░░░░   5% of system value
```

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

- [ ] PLATEAU-STORY-001 Define the plateau
- [ ] ROVER-STORY-001 Deploy a rover
- [ ] NAV-STORY-001 Navigate a rover
- [ ] CLI-STORY-002 Report final positions
- [ ] NAV-STORY-002 Boundary safe-stop
- [ ] MISSION-STORY-001 Multi-rover mission
- [ ] CLI-STORY-001 CLI pipe input
- [ ] CLI-STORY-003 Input validation & errors
- [ ] NAV-STORY-003 Obstacle detection
- [ ] NAV-STORY-004 Extensible command types

---

## Architecture References

All stories link to specific sections in the [architecture documentation](../architecture/):

- **Building Blocks**: [05-building-blocks.md](../architecture/05-building-blocks.md) — Component responsibilities
- **Solution Strategy**: [04-solution-strategy.md](../architecture/04-solution-strategy.md) — Hexagonal architecture, Command pattern
- **Functional Requirements**: [01-introduction.md](../architecture/01-introduction.md) — FR-1 through FR-7
- **Quality Requirements**: [10-quality-requirements.md](../architecture/10-quality-requirements.md) — QS-1 through QS-6
- **Constraints**: [02-constraints.md](../architecture/02-constraints.md) — DC-1 through DC-6, TC-1 through TC-3
- **Risks & Technical Debt**: [11-risks-and-technical-debts.md](../architecture/11-risks-and-technical-debts.md) — R-1 through R-3, TD-1 through TD-4
