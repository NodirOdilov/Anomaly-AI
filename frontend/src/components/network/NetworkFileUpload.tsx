import { FileUpload } from '../ui/FileUpload'

export function NetworkFileUpload({
  onFile,
}: {
  onFile: (f: File | null) => void
}) {
  return (
    <FileUpload
      accept=".csv,text/csv"
      hint="CSV должен содержать те же числовые feature columns, что и при обучении (см. Документацию). Колонка Label опциональна."
      onChange={(e) => onFile(e.target.files?.[0] ?? null)}
    />
  )
}
