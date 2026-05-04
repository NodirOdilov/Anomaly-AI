import { Textarea } from '../ui/Textarea'

export function PayloadInput({
  value,
  onChange,
}: {
  value: string
  onChange: (v: string) => void
}) {
  return (
    <div>
      <div className="mb-2 text-sm font-semibold tracking-wide text-slate-200">Payload</div>
      <Textarea value={value} onChange={(e) => onChange(e.target.value)} placeholder="Вставьте query string или фрагмент body…" />
    </div>
  )
}
