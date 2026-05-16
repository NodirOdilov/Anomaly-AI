# Diagrams

Mermaid sources (`.mmd`) and rendered assets (`.svg`, `.png`) for README and docs.

| File | Used in |
| ---- | ------- |
| `architecture-overview` | Root `README.md` |
| `architecture-full` | `README.md` (details) |
| `architecture-layers` | `ARCHITECTURE.md` |
| `predict-flow` | `ARCHITECTURE.md` |
| `data-model` | `ARCHITECTURE.md` |
| `mega-plan-stack` | `MEGA_PLAN.md` |

Regenerate all:

```bash
node scripts/render-diagrams.mjs
```
