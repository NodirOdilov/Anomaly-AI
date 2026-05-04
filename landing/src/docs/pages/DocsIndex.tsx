import { Link } from 'react-router-dom'
import {
  DocCallout,
  DocH1,
  DocH2,
  DocH3,
  DocLead,
  DocLi,
  DocP,
  DocUl,
} from '../components/DocTypography'

export function DocsIndex() {
  return (
    <article className="pb-16">
      <DocH1>Научно-техническая документация Anomaly AI</DocH1>
      <DocLead>
        Настоящий комплект документов предназначен для исследователей, инженеров по данным и специалистов по
        прикладной безопасности, которым требуется строгая постановка задачи, прозрачная методология и явные границы
        применимости системы. Изложение ориентировано на воспроизводимость и статистическую корректность формулировок.
      </DocLead>

      <DocCallout title="Область применения документа">
        Описывается реализация в составе монорепозитория Anomaly AI (FastAPI + scikit-learn + артефакты joblib + консоль
        React). Все утверждения о качестве моделей следует относить к конкретной версии артефакта и корпуса обучения;
        контрольные выборки в репозитории не претендуют на репрезентативность реального трафика.
      </DocCallout>

      <DocH2 id="audience">Целевая аудитория и предполагаемая подготовка</DocH2>
      <DocP>
        Документация рассчитана на читателя, владеющего основами теории вероятностей, линейной алгебры, классического
        машинного обучения (обучение с учителем, оценка обобщающей способности) и базовыми принципами сетевой
        безопасности. Предполагается знакомство с терминологией REST API и форматами JSON/CSV.
      </DocP>

      <DocH2 id="scope">Предмет и границы системы</DocH2>
      <DocP>
        Anomaly AI решает две взаимодополняющие задачи <strong>классификации с учителем</strong>:
      </DocP>
      <DocUl>
        <DocLi>
          <strong>Детектирование вредоносных веб-payload’ов</strong> — отображение строки (последовательности символов)
          в конечное множество семантических меток атак и класса «допустимо» (benign).
        </DocLi>
        <DocLi>
          <strong>Классификация сетевых потоков</strong> — отображение вектора числовых признаков, извлечённых из
          агрегированного описания потока, в конечное множество меток (в базовой конфигурации: BENIGN,
          HTTP_ATTACK, UDP_ATTACK).
        </DocLi>
      </DocUl>
      <DocP>
        Система <strong>не</strong> выполняет активное тестирование на проникновение, не генерирует эксплойты и не
        осуществляет несанкционированное сканирование. Назначение — анализ данных, на обработку которых у оператора есть
        правовые основания.
      </DocP>

      <DocH2 id="structure">Структура документации</DocH2>
      <DocP>Навигация слева (на широких экранах) отражает логический порядок чтения:</DocP>
      <DocUl>
        <DocLi>
          <Link className="text-cyan-300 underline-offset-2 hover:underline" to="/docs/foundations">
            Математические основы
          </Link>{' '}
          — постановка задач, обозначения, ключевые преобразования признаков.
        </DocLi>
        <DocLi>
          <Link className="text-cyan-300 underline-offset-2 hover:underline" to="/docs/methodology">
            Методология оценки
          </Link>{' '}
          — протоколы разбиения данных, метрики, статистические оговорки.
        </DocLi>
        <DocLi>
          <Link className="text-cyan-300 underline-offset-2 hover:underline" to="/docs/models">
            Архитектура моделей
          </Link>{' '}
          — конвейеры, гиперпараметры, постобработка меток.
        </DocLi>
        <DocLi>
          <Link className="text-cyan-300 underline-offset-2 hover:underline" to="/docs/datasets">
            Данные и протоколы
          </Link>{' '}
          — схемы признаков, этика разметки, утечки информации.
        </DocLi>
        <DocLi>
          <Link className="text-cyan-300 underline-offset-2 hover:underline" to="/docs/api">
            Справочник API
          </Link>{' '}
          — контракты HTTP-интерфейса.
        </DocLi>
        <DocLi>
          <Link className="text-cyan-300 underline-offset-2 hover:underline" to="/docs/artifacts">
            Артефакты и версии
          </Link>{' '}
          — состав сериализованного объекта и проверки целостности.
        </DocLi>
        <DocLi>
          <Link className="text-cyan-300 underline-offset-2 hover:underline" to="/docs/limitations">
            Ограничения и этика
          </Link>{' '}
          — обобщение, дрейф, устойчивость к состязательным воздействиям.
        </DocLi>
        <DocLi>
          <Link className="text-cyan-300 underline-offset-2 hover:underline" to="/docs/references">
            Литература
          </Link>{' '}
          — первичные методические источники.
        </DocLi>
      </DocUl>

      <DocH3>Версионирование</DocH3>
      <DocP>
        Версия программного комплекса и версия модели различаются. Версия API и веб-интерфейса приводится в ответе{' '}
        <code className="rounded bg-slate-900 px-1.5 py-0.5 font-mono text-cyan-200">GET /health</code>; версия модели
        содержится в поле <code className="rounded bg-slate-900 px-1.5 py-0.5 font-mono text-cyan-200">version</code>{' '}
        артефакта joblib и должна цитироваться в научных отчётах наряду с хэшем датасета и параметрами обучения.
      </DocP>
    </article>
  )
}
