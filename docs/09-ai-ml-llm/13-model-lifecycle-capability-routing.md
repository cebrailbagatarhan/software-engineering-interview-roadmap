# LLM Model Lifecycle, Retirement Risk ve Capability Routing

## Problem
Production LLM uygulamasını doğrudan tek model ID'sine bağlamak lifecycle, pricing ve capability değişikliklerini uygulama incident'ına dönüştürür. Daha dayanıklı abstraction bir capability contract + model registry + routing policy'dir.

## Mental model
```text
request -> capability policy -> model router -> model
                 ^                 |
                 |                 v
             eval gates <--- cost/latency/quality

registry: active -> deprecated -> retired
```

## Capability contract
Task; gerekli reasoning/coding/tool capability, quality floor, latency SLO, context ihtiyacı ve cost ceiling ile tanımlanır. Router aktif inventory'den uygun modeli seçer. Model retirement olduğunda mapping merkezi olarak değiştirilebilir; shadow traffic ve eval gates ile migration doğrulanır.

14 Eylül 2026 tarihli OpenAI release note'u GPT-5.5'in ChatGPT, ChatGPT Work ve Codex'te 14 Ekim 2026'da retire edileceğini duyurdu. GPT-5.6 ailesindeki Sol/Terra/Luna katmanları quality-cost-latency routing için güncel bir lifecycle örneğidir.

## Mülakat derinliği
Junior model/cost/latency; Mid routing/fallback; Senior eval, shadow traffic ve rollback; Staff capability registry/policy engine; CTO vendor strategy, lifecycle governance ve unit economics tartışmalıdır.

## Failure modes
- Hard-coded model IDs
- Eval'siz fallback
- Yalnız token fiyatına optimizasyon
- Retirement exposure inventory'si olmaması
- Tool/context/cache capability farklarını yok saymak

## Production bağlantısı
Task success/eval score, p95 latency, cost/task, fallback rate, model-version distribution, deprecated-model traffic ve retirement deadline exposure izlenmelidir.

## Kaynaklar
- https://openai.com/products/release-notes/
- https://openai.com/index/gpt-5-6/
- https://platform.openai.com/docs/guides/evals
