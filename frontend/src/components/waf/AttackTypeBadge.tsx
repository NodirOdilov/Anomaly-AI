import { Badge } from '../ui/Badge'

export function AttackTypeBadge({ type }: { type: string }) {
  const t = type.toLowerCase()
  if (t === 'benign') return <Badge tone="good">benign</Badge>
  if (t.includes('sql')) return <Badge tone="bad">sql_injection</Badge>
  if (t.includes('xss')) return <Badge tone="bad">xss</Badge>
  if (t.includes('path')) return <Badge tone="bad">path_traversal</Badge>
  if (t.includes('command')) return <Badge tone="bad">command_injection</Badge>
  return <Badge tone="info">{type}</Badge>
}
