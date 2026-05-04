import type { HealthResponse } from '../types/common'
import type { NetworkCsvResponse, NetworkRowResult } from '../types/network'
import type { ModelStatusItem, ModelsStatusResponse, ModuleMetrics, ReportsSummaryResponse } from '../types/reports'
import type { WafPredictResult } from '../types/waf'

const WAF_ATTACKS = ['sql_injection', 'xss', 'path_traversal', 'command_injection', 'generic_injection'] as const
const NETWORK_LABELS = ['BENIGN', 'HTTP_ATTACK', 'UDP_ATTACK'] as const

function previewVersion(): string {
  const d = new Date()
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `1.0.0-preview.${y}${m}${day}`
}

function hashString(input: string): number {
  let h = 2166136261
  for (let i = 0; i < input.length; i += 1) {
    h ^= input.charCodeAt(i)
    h = Math.imul(h, 16777619)
  }
  return h >>> 0
}

function createRng(seedInput: string): () => number {
  let t = hashString(seedInput) + 0x6d2b79f5
  return () => {
    t = Math.imul(t ^ (t >>> 15), t | 1)
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61)
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}

function rand(rng: () => number, min: number, max: number): number {
  return rng() * (max - min) + min
}

function round3(v: number): number {
  return Math.round(v * 1000) / 1000
}

function pickBySeed<T>(items: readonly T[], seed: number): T {
  return items[seed % items.length]
}

function randomMetrics(model: string, seedKey: string): ModuleMetrics {
  const rng = createRng(seedKey)
  const accuracy = rand(rng, 0.82, 0.97)
  const precision = rand(rng, 0.8, 0.96)
  const recall = rand(rng, 0.78, 0.95)
  const f1 = (2 * precision * recall) / (precision + recall)
  const falsePositiveRate = rand(rng, 0.01, 0.12)
  const falseNegativeRate = rand(rng, 0.02, 0.14)

  return {
    model,
    accuracy: round3(accuracy),
    precision: round3(precision),
    recall: round3(recall),
    f1: round3(f1),
    false_positive_rate: round3(falsePositiveRate),
    false_negative_rate: round3(falseNegativeRate),
    notes: 'Презентационный режим: метрики сгенерированы из synthetic telemetry.',
  }
}

function recommendationFor(attackType: string): string {
  if (attackType === 'sql_injection') return 'Заблокируйте запрос и проверьте логи приложения.'
  if (attackType === 'xss') return 'Заблокируйте запрос или выполните sanitization выходных данных.'
  if (attackType === 'path_traversal') return 'Отклоните path-ввод и проверьте логику доступа к файлам.'
  if (attackType === 'command_injection') return 'Немедленно заблокируйте запрос и изолируйте источник.'
  return 'Передайте инцидент на ручной анализ.'
}

function inferAttackType(payload: string, seed: number): string {
  const p = payload.toLowerCase()
  if (/(union|select| or |--|drop )/.test(p)) return 'sql_injection'
  if (/(<script|javascript:|onerror=|onload=)/.test(p)) return 'xss'
  if (/(\.\.\/|\.\.\\|\/etc\/passwd|%2e%2e%2f)/.test(p)) return 'path_traversal'
  if (/(;\s*(ls|cat|rm|curl|wget)|\|\s*sh|\$\()/.test(p)) return 'command_injection'
  return pickBySeed(WAF_ATTACKS, seed)
}

export function buildDemoWafResult(payload: string): WafPredictResult {
  const cleanPayload = payload.trim() || "id=1' OR '1'='1"
  const seed = hashString(cleanPayload)
  const rng = createRng(`waf:${cleanPayload}`)
  const seededAttack = inferAttackType(cleanPayload, seed)
  const explicitPattern = seededAttack !== 'generic_injection'
  const benignLike = /^[a-z0-9_\-=&%./? ]+$/i.test(cleanPayload)
  const score = rng()
  const isAttack = explicitPattern || (!benignLike && score > 0.5) || (benignLike && score > 0.9)
  const attackType = isAttack ? seededAttack : 'benign'
  const confidence = round3(
    isAttack
      ? explicitPattern
        ? rand(rng, 0.86, 0.99)
        : rand(rng, 0.72, 0.91)
      : rand(rng, 0.74, 0.93),
  )

  return {
    payload: cleanPayload,
    is_attack: isAttack,
    attack_type: attackType,
    confidence,
    severity: isAttack ? (confidence > 0.88 ? 'high' : 'medium') : 'none',
    recommendation: isAttack ? recommendationFor(attackType) : 'Разрешить с обычным мониторингом.',
    model_version: previewVersion(),
  }
}

export function buildDemoNetworkCsvResponse(seedText = 'network-default'): NetworkCsvResponse {
  const rng = createRng(`network:${seedText}`)
  const total = Math.floor(rand(rng, 18, 64))
  const results: NetworkRowResult[] = []

  for (let i = 0; i < total; i += 1) {
    const r = rng()
    const label = r < 0.68 ? 'BENIGN' : r < 0.86 ? 'HTTP_ATTACK' : 'UDP_ATTACK'
    const confidence = round3(label === 'BENIGN' ? rand(rng, 0.62, 0.96) : rand(rng, 0.7, 0.99))
    results.push({ row: i + 1, prediction: label, confidence })
  }

  const benign = results.filter((x) => x.prediction === 'BENIGN').length
  const suspicious = total - benign
  const counts = Object.fromEntries(NETWORK_LABELS.map((k) => [k, 0])) as Record<string, number>
  for (const row of results) counts[row.prediction] = (counts[row.prediction] ?? 0) + 1
  const topPrediction = Object.entries(counts).sort((a, b) => b[1] - a[1])[0]?.[0] ?? 'BENIGN'

  return {
    total_flows: total,
    benign,
    suspicious,
    top_prediction: topPrediction,
    results,
  }
}

export function buildDemoReportsSummary(): ReportsSummaryResponse {
  return {
    network_anomaly: randomMetrics('RandomForestClassifier (release candidate)', 'reports-network'),
    waf_payload: randomMetrics('TfidfVectorizer + LogisticRegression (release candidate)', 'reports-waf'),
  }
}

function loadedStatus(modelType: string, path: string): ModelStatusItem {
  return {
    loaded: true,
    version: previewVersion(),
    model_type: modelType,
    path,
    message: 'Preview fallback: synthetic status stream active.',
  }
}

export function buildDemoModelsStatus(): ModelsStatusResponse {
  return {
    network_anomaly: loadedStatus('network_anomaly_detector', '/models/network_anomaly_model.joblib'),
    waf_payload: loadedStatus('waf_payload_detector', '/models/waf_payload_model.joblib'),
  }
}

export function buildDemoHealth(): HealthResponse {
  return {
    status: 'ok',
    service: 'Anomaly AI',
    version: previewVersion(),
    backend: 'FastAPI',
  }
}
