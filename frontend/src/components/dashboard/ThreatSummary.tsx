import { Card } from '../ui/Card'

export function ThreatSummary() {
  return (
    <Card className="p-5">
      <div className="text-base font-semibold text-slate-100">Сводка по угрозам</div>
      <p className="mt-3 text-sm leading-relaxed text-slate-300">
        Используйте анализаторы для оценки payload и сетевых потоков. Результаты вероятностные, поэтому их нужно комбинировать
        с логированием, политиками безопасности и ручной проверкой.
      </p>
    </Card>
  )
}
