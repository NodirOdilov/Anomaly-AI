# Диаграммы

Исходники Mermaid (`.mmd`) и отрендеренные файлы (`.svg`, `.png`) для README и документации.

| Файл | Где используется |
| ---- | ---------------- |
| `architecture-overview` | Корневой `README.md` |
| `architecture-full` | `README.md` (блок details) |
| `architecture-layers` | `ARCHITECTURE.md` |
| `predict-flow` | `ARCHITECTURE.md` |
| `data-model` | `ARCHITECTURE.md` |
| `mega-plan-stack` | `MEGA_PLAN.md` |

Пересборка всех диаграмм:

```bash
node scripts/render-diagrams.mjs
```

Или: `make diagrams`
