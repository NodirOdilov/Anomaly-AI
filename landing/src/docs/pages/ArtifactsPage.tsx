import { DocCallout, DocH1, DocH2, DocLead, DocLi, DocPre, DocUl } from '../components/DocTypography'

export function ArtifactsPage() {
  return (
    <article className="pb-16">
      <DocH1>Артефакты обучения и версионирование</DocH1>
      <DocLead>
        Артефакт сериализуется средствами <span className="font-mono text-slate-200">joblib</span> и представляет собой
        ассоциативный массив (Python <span className="font-mono text-slate-200">dict</span>) с обязательными ключами,
        перечисленными ниже. Такой формат обеспечивает совместимость с практикой MLOps «модель + метаданные» и упрощает
        аудит.
      </DocLead>

      <DocH2 id="schema">Логическая схема</DocH2>
      <DocPre>{`{
  "project": "Anomaly AI",
  "model": <sklearn Pipeline или estimator>,
  "preprocessor": <объект или null>,
  "features": [...],           // для табличного модуля: порядок имён признаков
  "labels": { "<класс>": <индекс>, ... },
  "model_type": "waf_payload_detector" | "network_anomaly_detector",
  "version": "semver",
  "created_at": "<ISO-8601 UTC>",
  "metrics": {
    "accuracy": float,
    "precision": float,
    "recall": float,
    "f1": float,
    "false_positive_rate": float,
    "false_negative_rate": float
  }
}`}</DocPre>

      <DocH2 id="validation">Проверки при загрузке</DocH2>
      <DocUl>
        <DocLi>Наличие файла по конфигурируемому пути.</DocLi>
        <DocLi>Наличие обязательных ключей и ненулевая строка версии.</DocLi>
        <DocLi>Соответствие поля <span className="font-mono text-slate-200">model_type</span> ожидаемому модулю.</DocLi>
        <DocLi>Ненулевой указатель на обученный объект модели.</DocLi>
      </DocUl>

      <DocCallout title="Научная трассируемость">
        Для публикаций рекомендуется сохранять рядом с артефактом отчёт о данных (data card), журнал эксперимента и
        контрольную сумму файла; платформа предоставляет базовые отчёты Markdown в каталоге{' '}
        <span className="font-mono text-slate-200">backend/reports/</span>, которые следует расширять при промышленной
        эксплуатации.
      </DocCallout>
    </article>
  )
}
