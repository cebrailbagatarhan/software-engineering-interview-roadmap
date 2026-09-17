# Long-Running Agent Harnesses, Tool Boundaries & Durable Execution

## Neden önemli?
Production agent sistemi tek model çağrısı değildir. Reasoning, context, tool execution, çalışma ortamı, ara durum, retry/timeout, subagent koordinasyonu ve observability bir harness içinde yönetilir.

## Mental model
```text
request -> control plane -> planner/model
              |-> state/checkpoints
              |-> subagents
              +-> tool gateway -> side effects
                         |
                   result ledger
                         |
                   retry / resume
```

Control plane state transition'ları yönetir; execution plane dosya, kod ve API gibi yan etkili araçları çalıştırır. Crash recovery için durable checkpoint, idempotent tool call, explicit side-effect ledger ve resumable state machine gerekir.

## Güncel production bağlantısı
OpenAI 10 Eylül 2026'da Agents API'yi public beta olarak duyurdu; uzun süreli işler için context/tool/subagent koordinasyonu, managed environments ve intermediate-result persistence gereksinimini öne çıkardı. Tasarım sorusu ürün isminden bağımsızdır: saatler sonra crash eden iş güvenli biçimde nereden ve hangi side-effect bilgisiyle devam eder?

## Mülakat soruları
- Harness ile model sorumluluğu nasıl ayrılır?
- Tool call neden sıradan function call değildir?
- Retry'da duplicate side effect nasıl önlenir?
- Checkpoint hangi state'i içermelidir?
- Timeout/cancellation/partial result nasıl modellenir?
- Subagent fan-out'ta budget ve backpressure nasıl uygulanır?
- Build-vs-buy hangi güvenlik ve ekonomi risklerini değiştirir?

## Seviyeye göre derinlik
Junior/Mid: model, tool, state. Senior: idempotency, checkpoint, timeout, observability. Staff: orchestration, isolation, concurrency budget, recovery. Principal/CTO: platform boundary, cost, auditability ve portability.

## Mini alıştırma
`research → code change → test → deploy request` state machine'i çiz. Deploy timeout sonrası retry öncesi hangi ledger kaydının kontrol edileceğini belirt.

## Proje
`durable-agent-runner`: Postgres/SQLite state store, idempotency key, checkpoint, tool-result ledger, cancellation ve crash-after-side-effect fault injection.

## Failure modes / trade-off
Prompt'u durable state sanmak; side effect sonrası geç checkpoint; sınırsız fan-out; tool permission'ını modele bırakmak; retry storm; stale context; approval bypass. Production'da completion, resume success, duplicate side effect, tool error, compute budget, wall-clock latency ve approval violations izlenir.

## Kaynaklar
- https://openai.com/index/introducing-the-agents-api/
- https://platform.openai.com/docs/guides/agents
