import { DocH1, DocH2, DocH3, DocLead, DocLi, DocP, DocPre, DocUl } from '../components/DocTypography'

export function ApiReferencePage() {
  return (
    <article className="pb-16">
      <DocH1>Справочник HTTP API</DocH1>
      <DocLead>
        Интерфейс реализован на FastAPI и следует стилю REST. Ниже приведены маршруты версии{' '}
        <span className="font-mono text-slate-200">v1</span>; тело запросов и ответов — JSON с кодировкой UTF-8, если не
        указано иное.
      </DocLead>

      <DocH2 id="health">Служебные методы</DocH2>
      <DocH3>GET /health</DocH3>
      <DocP>Возвращает статус процесса, имя сервиса, версию backend и идентификатор стека (FastAPI).</DocP>
      <DocPre>{`{
  "status": "ok",
  "service": "Anomaly AI",
  "version": "1.0.0",
  "backend": "FastAPI"
}`}</DocPre>

      <DocH3>GET /api/v1/info</DocH3>
      <DocP>Метаданные продукта: краткое описание, перечень модулей, режим «defensive-security».</DocP>

      <DocH3>GET /api/v1/models/status</DocH3>
      <DocP>
        Диагностическая информация о наличии и валидности артефактов WAF и сетевого модуля на диске сервера приложений.
      </DocP>

      <DocH2 id="waf-api">Модуль WAF</DocH2>
      <DocH3>POST /api/v1/waf/predict</DocH3>
      <DocP>Тело запроса:</DocP>
      <DocPre>{`{ "payload": "<строка UTF-8>" }`}</DocPre>
      <DocP>
        Ответ содержит бинарный или мультиклассовый вердикт, нормализованную метку, оценку уверенности (максимум softmax),
        уровень серьёзности, рекомендацию для оператора и версию модели.
      </DocP>

      <DocH3>POST /api/v1/waf/batch-predict</DocH3>
      <DocP>
        Пакетная оценка массива строк; ответ включает агрегированное число атак и список результатов по элементам. Формат
        оптимизирован для сценариев пакетной обработки журналов при соблюдении политик хранения данных.
      </DocP>

      <DocH2 id="net-api">Сетевой модуль</DocH2>
      <DocH3>POST /api/v1/network/predict</DocH3>
      <DocP>
        JSON-объект с ключами, совпадающими с обучающим вектором признаков (без столбца метки). Сервер валидирует
        наличие обязательных полей относительно загруженного артефакта.
      </DocP>

      <DocH3>POST /api/v1/network/upload-csv</DocH3>
      <DocP>
        Загрузка CSV (<span className="font-mono text-slate-200">multipart/form-data</span>, поле файла{' '}
        <span className="font-mono text-slate-200">file</span>). Кодировка UTF-8. Опциональный столбец метки игнорируется
        при инференсе, но может присутствовать для сверки в исследовательских сценариях.
      </DocP>

      <DocH2 id="reports">Отчётность</DocH2>
      <DocH3>GET /api/v1/reports/summary</DocH3>
      <DocP>
        Возвращает блоки метрик по обоим модулям. Нулевые значения на «чистой» установке отражают отсутствие обученного
        артефакта и являются ожидаемым поведением, а не сбоем API.
      </DocP>

      <DocH2 id="errors">Коды ошибок</DocH2>
      <DocP>Прикладные исключения сериализуются в JSON-объект единого вида:</DocP>
      <DocPre>{`{ "error": "<код>", "message": "<человекочитаемое пояснение>" }`}</DocPre>
      <DocUl>
        <DocLi>
          <span className="font-mono text-slate-200">InvalidInput</span> — некорректные или неполные входные данные.
        </DocLi>
        <DocLi>
          <span className="font-mono text-slate-200">ModelNotFound</span> — отсутствует файл артефакта на сервере.
        </DocLi>
        <DocLi>
          <span className="font-mono text-slate-200">ModelArtifactError</span> — повреждённый или несовместимый артефакт.
        </DocLi>
      </DocUl>
    </article>
  )
}
