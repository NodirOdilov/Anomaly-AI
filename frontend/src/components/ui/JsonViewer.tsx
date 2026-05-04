export function JsonViewer({ value }: { value: unknown }) {
  const text = JSON.stringify(value, null, 2)
  return (
    <pre className="max-h-80 overflow-auto rounded-xl border border-slate-800 bg-slate-950 p-4 text-xs leading-relaxed text-slate-200">
      {text}
    </pre>
  )
}
