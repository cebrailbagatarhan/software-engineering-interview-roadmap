# Prompt Caching, Prefix Architecture & Inference Economics

## Temel fikir
Uzun ve tekrarlanan instructions, tool schemas ve shared context her request'te yeniden prefill edildiğinde inference latency ve compute maliyeti büyür. Prompt caching aynı prefix için daha önce yapılan prompt-processing computation'ını reuse etmeyi hedefler. Response cache değildir ve correctness mekanizması olarak kullanılmamalıdır.

## Mental model
```text
[stable policy][tools][shared context] | [request-specific delta]
<------------- reusable prefix ------>   variable suffix
```

Exact/shared prefix'i başta stabil tutmak, volatile metadata'yı sona taşımak cache reuse olasılığını artırır. Tool definitions ve diğer input parçalarının değişmesi de prefix identity'yi bozabilir.

## 2026 production bağlantısı
OpenAI'nin 13 Ağustos 2026 GPT-5.6 builder guidance'ı model ailesinde prompt-cache TTL'nin en az 30 dakikaya uzatıldığını, deterministic cache breakpoints ve `prompt_cache_key` kullanımını anlatıyor. Tasarım yalnız hit rate'i değil cached/uncached input, latency, quality ve tenant isolation'ı birlikte optimize etmelidir.

## Mülakat ayrımları
- Prompt cache != semantic/response cache.
- Exact prefix reuse prompt ordering'i architecture concern yapar.
- Dynamic timestamp veya tenant-specific field'i prompt başına koymak downstream reuse'u bozabilir.
- High hit rate tek başına düşük end-to-end latency garantisi değildir.
- Multi-tenant sistemde cost optimization isolation/correctness sınırlarını ihlal etmemelidir.

## Production metrikleri
`cached_tokens` ratio, uncached input tokens, TTFT/end-to-end latency, cost/request, quality eval, cache-key cardinality ve model-routing sonucu birlikte izlenir.

## Kaynaklar
- https://openai.com/index/builders-guide-to-gpt-5-6/
- https://openai.com/index/api-prompt-caching/
- https://openai.com/index/unrolling-the-codex-agent-loop/
- https://developers.openai.com/api/docs/guides/prompt-caching
