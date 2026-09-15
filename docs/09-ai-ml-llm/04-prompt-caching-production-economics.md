# Prompt Caching, Prefix Stability & Production Economics

Uzun ve tekrar eden instruction/tool/schema/context prefix'leri LLM isteklerinde input processing maliyetini büyütür. Prompt caching ortak prefix hesaplamasını yeniden kullanarak latency ve input maliyetini azaltabilir. Stable/reusable içeriği başa, request-specific içeriği sona koymak cache reuse açısından temel tasarım desenidir.

## Mental model
```text
[stable shared prefix][dynamic request tail]
          |
       cache hit
       /      \
 latency/cost  task semantics unchanged
```

Cache correctness katmanı değildir. Prompt/tool schema değişiklikleri reuse oranını düşürebilir. Production'da cached tokens, uncached input, p50/p95 latency, cost/request ve hit ratio birlikte izlenmelidir.

2026 GPT-5.6 builder rehberi prompt-cache TTL'nin model ailesinde en az 30 dakikaya uzatıldığını, deterministic breakpoints ve uygun cache key kullanımının hit rate/latency'ye yardımcı olabildiğini belirtir. Model/API ayrıntıları değişebileceği için canlı dokümantasyon esas alınmalıdır.

## Mülakat odağı
- Prompt cache vs semantic/RAG cache.
- Prefix stability.
- Cache hit'in correctness'ten ayrılması.
- Tool schema ve prompt-layout etkisi.
- Multi-tenant privacy/cache-key sınırları.
- Model migration sırasında economics revalidation.

## Production
Cache hit telemetry olmadan optimizasyon yapma. Hit oranını artırmak için stale business context'i sabitleme. Tenant isolation, versioning ve rollout ölçümlerini maliyet/latency ile birlikte değerlendir.

## Kaynaklar
- https://platform.openai.com/docs/guides/prompt-caching
- https://openai.com/index/builders-guide-to-gpt-5-6/
