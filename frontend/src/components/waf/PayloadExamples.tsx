import { Button } from '../ui/Button'

const examples = [
  { label: 'Обычный запрос', value: 'q=books&sort=price' },
  { label: 'Пример SQLi', value: "id=1' OR '1'='1" },
  { label: 'Пример XSS', value: '<script>alert(1)</script>' },
  { label: 'Пример Path Traversal', value: '../../etc/passwd' },
] as const

export function PayloadExamples({ onPick }: { onPick: (s: string) => void }) {
  return (
    <div className="flex flex-wrap gap-2.5">
      {examples.map((e) => (
        <Button key={e.label} type="button" variant="ghost" className="text-xs" onClick={() => onPick(e.value)}>
          {e.label}
        </Button>
      ))}
    </div>
  )
}
