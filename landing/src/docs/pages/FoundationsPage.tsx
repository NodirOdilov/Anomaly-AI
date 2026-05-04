import {
  DocCallout,
  DocH1,
  DocH2,
  DocH3,
  DocLead,
  DocLi,
  DocMath,
  DocP,
  DocUl,
} from '../components/DocTypography'

export function FoundationsPage() {
  return (
    <article className="pb-16">
      <DocH1>Математические основы</DocH1>
      <DocLead>
        Ниже формализованы две независимые задачи обучения с учителем, реализованные в платформе. Обозначения согласованы
        с принятой в машинном обучении нотации (Hastie, Tibshirani, Friedman; James et al.).
      </DocLead>

      <DocH2 id="notation">Обозначения</DocH2>
      <DocUl>
        <DocLi>
          <strong>Корпус текстовых payload’ов:</strong> пусть имеется выборка пар{' '}
          <span className="font-mono text-slate-200">(sᵢ, yᵢ)</span>, где{' '}
          <span className="font-mono text-slate-200">sᵢ ∈ Σ*</span> — строка над конечным алфавитом символов запроса,{' '}
          <span className="font-mono text-slate-200">yᵢ ∈ 𝒴_waf</span> — конечное множество меток (включая benign и
          классы атак).
        </DocLi>
        <DocLi>
          <strong>Матрица сетевых признаков:</strong>{' '}
          <span className="font-mono text-slate-200">X ∈ ℝⁿˣᵈ</span>, строка{' '}
          <span className="font-mono text-slate-200">xᵢ</span> описывает <span className="font-mono text-slate-200">i</span>
          -й поток; метки <span className="font-mono text-slate-200">yᵢ ∈ 𝒴_net</span>.
        </DocLi>
      </DocUl>

      <DocH2 id="tfidf">Векторизация payload’ов: TF–IDF по символьным n-граммам</DocH2>
      <DocP>
        Для устойчивого представления коротких и сильно структурированных строк (делимитеры, экранирование, смешение
        регистров) применяется <strong>символьный анализатор</strong>: признаки соответствуют n-граммам символов при
        заданных <span className="font-mono text-slate-200">n ∈ [n_min, n_max]</span>. Вес признака{' '}
        <span className="font-mono text-slate-200">j</span> для документа <span className="font-mono text-slate-200">i</span>
        :
      </DocP>
      <DocMath>
        {`TF-IDF(i, j) = f_{i,j} · log((N + 1) / (df_j + 1))`}
      </DocMath>
      <DocP>
        где <span className="font-mono text-slate-200">f<sub>i,j</sub></span> — частота (или нормированная частота)
        n-граммы <span className="font-mono text-slate-200">j</span> в строке <span className="font-mono text-slate-200">i</span>,{' '}
        <span className="font-mono text-slate-200">df_j</span> — число документов, содержащих n-грамму,{' '}
        <span className="font-mono text-slate-200">N</span> — число документов в обучающей выборке. Конкретная схема
        нормализации и сглаживания соответствует реализации{' '}
        <span className="font-mono text-slate-200">sklearn.feature_extraction.text.TfidfVectorizer</span> в версии
        библиотеки, зафиксированной в <span className="font-mono text-slate-200">requirements.txt</span> backend.
      </DocP>
      <DocCallout title="Интерпретация для практики">
        Символьные n-граммы устойчивы к дроблению ключевых лексем и частично к простейшим обфускациям, однако не
        гарантируют инвариантность к полиморфным атакам и состязательным возмущениям в пространстве ввода.
      </DocCallout>

      <DocH2 id="logreg">Многоклассовая логистическая регрессия (модуль WAF)</DocH2>
      <DocP>
        После отображения TF–IDF вектор <span className="font-mono text-slate-200">φ(s) ∈ ℝᵖ</span> подаётся в
        многоклассовую логистическую модель. Для класса <span className="font-mono text-slate-200">k</span>:
      </DocP>
      <DocMath>
        {`P(y = k | s) = exp(θ_k^T φ(s) + b_k) / Σ_j exp(θ_j^T φ(s) + b_j)`}
      </DocMath>
      <DocP>
        Оценка параметров выполняется максимизацией штрафованного лог-правдоподобия (L2-регуляризация через параметр{' '}
        <span className="font-mono text-slate-200">C</span> в терминологии scikit-learn). Оптимизатор по умолчанию в
        конфигурации — saga; при малых выборках возможна повышенная дисперсия оценок и неидеальная калибровка
        вероятностей — см. раздел «Методология оценки».
      </DocP>

      <DocH2 id="scale-forest">Числовые потоки: масштабирование и случайный лес</DocH2>
      <DocP>
        Каждый признак потока приводится к отрезку [0, 1] посредством минимаксного преобразования, параметры которого
        оцениваются на обучающей выборке и сохраняются в составе конвейера. Это линейное преобразование устраняет различие
        масштабов физических величин; для древесных моделей оно не является строго необходимым, но обеспечивает
        согласованность с последующими экспериментами и потенциальными линейными базовыми моделями.
      </DocP>
      <DocP>
        Классификатор — ансамбль решающих деревьев (Random Forest). Для бэггинг-оценки дисперсии в литературе
        приводятся OOB-оценки; в текущей реализации продукта основной отчёт строится по отложенной/кросс-валидационной
        схеме, заданной в скриптах обучения.
      </DocP>

      <DocH3>Постобработка меток (эвристическое уточнение)</DocH3>
      <DocP>
        Независимо от вероятностной модели применяется слой правил сопоставления регулярных выражений для снижения
        неопределённости в прикладных сценариях. Данный слой <strong>не является вероятностной моделью</strong> и
        не подлежит интерпретации как оценка апостериорной вероятности; его следует документировать отдельно в отчётах о
        воспроизводимости.
      </DocP>
    </article>
  )
}
