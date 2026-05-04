import { Card } from '../components/ui/Card'

export function DocumentationPage() {
  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-2xl font-semibold leading-tight text-slate-50 sm:text-3xl">Документация</h1>
        <p className="max-w-4xl text-sm leading-relaxed text-slate-300">Краткая ориентация для защитников, ревьюеров и интервьюеров.</p>
      </div>

      <Card className="space-y-4 p-5 text-sm leading-relaxed text-slate-200">
        <div className="text-base font-semibold text-slate-50">Что такое Anomaly AI?</div>
        <p>
          Anomaly AI — защитная платформа кибербезопасности, использующая Machine Learning для обнаружения аномалий сетевого
          трафика и вредоносных web-payload, таких как SQL injection, XSS, path traversal и попытки обхода WAF. В систему
          входят FastAPI backend, ML-сервисы детектирования, CLI-инструменты, деплой через Docker и React-панель для
          интерактивного анализа.
        </p>

        <div className="text-base font-semibold text-slate-50">Обнаружение WAF-угроз</div>
        <p>
          Payload векторизуются символьными n-gram (TF‑IDF) и классифицируются линейной моделью. Rule-based подсказки помогают
          маркировать очевидные паттерны, когда модель неуверенна — только для защитной классификации.
        </p>

        <div className="text-base font-semibold text-slate-50">Обнаружение сетевых аномалий</div>
        <p>
          Числовые признаки потоков очищаются (NaN/inf), масштабируются и классифицируются pipeline на RandomForest. Артефакты
          сохраняют порядок признаков, чтобы обучение и inference оставались согласованными.
        </p>

        <div className="text-base font-semibold text-slate-50">Использование API</div>
        <p>
          Базовый URL задаётся через <code className="text-sky-300">VITE_API_BASE_URL</code>. Ключевые маршруты: <code className="text-sky-300">/health</code>,{' '}
          <code className="text-sky-300">/api/v1/waf/predict</code> и <code className="text-sky-300">/api/v1/network/upload-csv</code>. Полные
          примеры смотрите в <code className="text-sky-300">docs/API.md</code>.
        </p>

        <div className="text-base font-semibold text-slate-50">Предупреждение по безопасности</div>
        <p>
          Только защитное применение. Не направляйте toolkit на системы, которыми вы не владеете или не имеете разрешения на
          тестирование. Строки payload — это недоверенные данные: используйте их как вход для классификаторов, а не как команды
          к исполнению.
        </p>
      </Card>
    </div>
  )
}
