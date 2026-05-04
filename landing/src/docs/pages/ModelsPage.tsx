import { DocCallout, DocH1, DocH2, DocH3, DocLead, DocLi, DocP, DocUl } from '../components/DocTypography'

export function ModelsPage() {
  return (
    <article className="pb-16">
      <DocH1>Архитектура моделей в продукте</DocH1>
      <DocLead>
        Реализация следует принципу «конвейер как единый объект»: векторизация/масштабирование и обучаемый классификатор
        сериализуются совместно, чтобы исключить рассогласование предобработки между обучением и инференсом.
      </DocLead>

      <DocH2 id="waf-pipeline">Конвейер WAF-модуля</DocH2>
      <DocP>Состав:</DocP>
      <DocUl>
        <DocLi>
          <strong>TfidfVectorizer</strong> с <span className="font-mono text-slate-200">analyzer=&quot;char&quot;</span> и
          диапазоном n-грамм из конфигурации (<span className="font-mono text-slate-200">configs/waf_payload.yaml</span>
          ).
        </DocLi>
        <DocLi>
          <strong>LogisticRegression</strong> с балансировкой классов через веса <span className="font-mono text-slate-200">class_weight=&quot;balanced&quot;</span>{' '}
          (оценка обратной частоты класса на обучающей выборке внутри реализации scikit-learn).
        </DocLi>
      </DocUl>
      <DocCallout title="Научная интерпретация балансировки">
        Взвешивание классов эквивалентно изменению функции потерь и приводит к компромиссу между полнотой по редким
        классам и точностью по доминирующим. Эффект следует количественно фиксировать на валидации, а не постулировать
        априори.
      </DocCallout>

      <DocH2 id="net-pipeline">Конвейер сетевого модуля</DocH2>
      <DocP>Состав:</DocP>
      <DocUl>
        <DocLi>
          <strong>MinMaxScaler</strong> — масштабирование признаков по обучающей выборке; параметры сохраняются в объекте
          scaler внутри сериализованного конвейера.
        </DocLi>
        <DocLi>
          <strong>RandomForestClassifier</strong> с параметром{' '}
          <span className="font-mono text-slate-200">class_weight=&quot;balanced&quot;</span> и числом деревьев из YAML.
        </DocLi>
      </DocUl>

      <DocH3>Обработка отсутствующих и некорректных значений</DocH3>
      <DocP>
        На этапе подготовки табличных данных выполняется замена бесконечностей и пропусков конечными значениями по
        правилам модуля подготовки; данное упрощение подходит для базового контура, но в исследовательской постановке требует
        обоснования (MNAR/MCAR/MAR) и сравнения с более информативными методами вменения.
      </DocP>

      <DocH2 id="inference">Инференс и постобработка</DocH2>
      <DocP>
        Для каждого запроса возвращаются метка с максимальной апостериорной вероятностью (argmax по softmax-выходу или
        аналогу для логрега) и скаляр уверенности, равный максимальной вероятности по классам. Дополнительно применяется
        правило-основанный слой для уточнения метки при низкой уверенности; данный слой должен быть явно указан в
        приложениях к научному отчёту, если сравниваются чистые вероятностные модели и гибридная система.
      </DocP>
    </article>
  )
}
