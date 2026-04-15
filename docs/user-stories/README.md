# User Story Inventory — Mars Rover Kata

Pareto-prioritized: the first 5 stories (~50% of total) deliver ~80% of the working system value.

---

## Story Map

| ID | File | Title | Layer | Priority | Status |
|----|------|-------|-------|----------|--------|
| STORY-001 | [plateau.md](plateau.md) | Define the plateau | Domain | 🔴 Core | ⬜ Todo |
| STORY-002 | [deploy-rover.md](deploy-rover.md) | Deploy a rover | Domain | 🔴 Core | ⬜ Todo |
| STORY-003 | [navigate-rover.md](navigate-rover.md) | Navigate a rover | Domain | 🔴 Core | ⬜ Todo |
| STORY-004 | [report-positions.md](report-positions.md) | Report final positions | Adapter | 🔴 Core | ⬜ Todo |
| STORY-005 | [boundary-safe-stop.md](boundary-safe-stop.md) | Boundary safe-stop | Domain | 🔴 Core | ⬜ Todo |
| STORY-006 | [multi-rover-mission.md](multi-rover-mission.md) | Multi-rover mission | Application | 🟡 Secondary | ⬜ Todo |
| STORY-007 | [cli-input.md](cli-input.md) | CLI pipe input | Adapter | 🟡 Secondary | ⬜ Todo |
| STORY-008 | [input-validation.md](input-validation.md) | Input validation & errors | Adapter | 🟡 Secondary | ⬜ Todo |
| STORY-009 | [obstacle-detection.md](obstacle-detection.md) | Obstacle detection | Domain | 🟢 Optional | ⬜ Todo |
| STORY-010 | [extensible-commands.md](extensible-commands.md) | Extensible command types | Domain | 🟢 Optional | ⬜ Todo |

---

## Pareto Split

```
🔴 Core (STORY-001 → 005)   ████████████████████  80% of system value
🟡 Secondary (006 → 008)    ████░░░░░░░░░░░░░░░░  15% of system value
🟢 Optional  (009 → 010)    ██░░░░░░░░░░░░░░░░░░   5% of system value
```

---

## Progress Tracker

- [ ] STORY-001 Define the plateau
- [ ] STORY-002 Deploy a rover
- [ ] STORY-003 Navigate a rover
- [ ] STORY-004 Report final positions
- [ ] STORY-005 Boundary safe-stop
- [ ] STORY-006 Multi-rover mission
- [ ] STORY-007 CLI pipe input
- [ ] STORY-008 Input validation & errors
- [ ] STORY-009 Obstacle detection
- [ ] STORY-010 Extensible command types
