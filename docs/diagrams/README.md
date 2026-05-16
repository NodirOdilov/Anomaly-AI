# Диаграммы архитектуры

> Исходники Mermaid (`.mmd`) и отрендеренные SVG/PNG для README и документации.

| Параметр | Значение |
|----------|----------|
| Каталог | `docs/diagrams/` |
| Конфиг рендера | `mermaid-config.json` |
| Скрипт сборки | `scripts/render-diagrams.mjs` |

## Каталог артефактов

| Базовое имя | Форматы | Используется в |
|-------------|---------|----------------|
| `architecture-overview` | `.mmd`, `.svg`, `.png` | [`README.md`](../README.md) |
| `architecture-full` | `.mmd`, `.svg`, `.png` | README (блок details) |
| `architecture-layers` | `.mmd`, `.svg` | [`ARCHITECTURE.md`](../ARCHITECTURE.md) |
| `predict-flow` | `.mmd`, `.svg` | ARCHITECTURE.md |
| `data-model` | `.mmd`, `.svg` | ARCHITECTURE.md |
| `mega-plan-stack` | `.mmd`, `.svg` | [`MEGA_PLAN.md`](../MEGA_PLAN.md) |

---

## Пересборка

Из корня репозитория:

```bash
node scripts/render-diagrams.mjs
```

или:

```bash
make diagrams
```

Требования: Node.js 20+, пакет `@mermaid-js/mermaid-cli` (подтягивается через `npx`).

---

## Правки диаграммы

1. Отредактируйте соответствующий файл `.mmd`.
2. Запустите пересборку (см. выше).
3. Закоммитьте `.mmd` и сгенерированные `.svg` / `.png`.

---

## См. также

- [`ARCHITECTURE.md`](../ARCHITECTURE.md)
- [`README.md`](../README.md#архитектура)
