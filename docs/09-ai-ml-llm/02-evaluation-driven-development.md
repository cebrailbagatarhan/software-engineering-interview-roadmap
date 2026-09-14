# LLM Evaluation-Driven Development ve Regression Gates

## Neden eval?
LLM sisteminde manuel birkaç örneğin iyi görünmesi release kriteri değildir. Versioned eval set gerçek kullanım, edge case ve kritik failure mode'ları temsil etmeli; prompt, model, retrieval veya tool değişikliği aynı regression suite üzerinde karşılaştırılmalıdır.

```text
production examples -> versioned eval set -> candidate
        ^                       |              |
        |                       +--- evaluate -+
        |                              |
        +---- online feedback <- deploy/gate
```

## Ölçüm katmanları
Tek aggregate score yerine task/language/risk slice'ları izle. Correctness yanında latency ve cost'u da release kararına kat. RAG'de retrieval failure ile generation failure'ı ayır. Deterministic correctness mümkünse programmatic assertion kullan; model grader kullanıldığında rubric ve calibration örnekleri versionlanmalıdır.

## Offline + online
Offline eval hızlı regression gate sağlar. Online telemetry gerçek distribution drift'i, yeni edge case'leri ve kullanıcı davranışını gösterir. Production failure'lar eval corpus'a geri beslenmelidir.

## Mülakat derinliği
Senior aday dataset, metric ve reproducibility konuşur. Staff evaluator governance, per-slice thresholds ve quality-cost-latency trade-off tasarlar. Principal risk tier'larına göre şirket çapında release standardı kurar.

## Failure modes
Synthetic-only set, eval overfitting, data leakage, unstable judge, tek skor, cost/latency'yi yok saymak ve production'dan yeni case toplamamak.

## Habitat bağlantısı
Storage copilot veya policy assistant için backend seçimi, migration planı ve destructive action önerileri deterministic policy checks ile doğrulanabilir; doğal dil kalitesi model grader'a bırakılırken güvenlik/correctness invariants kodla gate edilir.

## Kaynaklar
- OpenAI — Evaluation best practices: https://platform.openai.com/docs/guides/evaluation-best-practices
- OpenAI — Evals: https://platform.openai.com/docs/guides/evals
