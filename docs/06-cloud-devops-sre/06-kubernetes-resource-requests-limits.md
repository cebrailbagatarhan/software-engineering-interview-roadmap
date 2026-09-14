# Kubernetes Resource Requests, Limits ve Runtime Failure Modes

## Mental model
Request scheduler'ın placement ve contention kararına girdi sağlar. Limit runtime tüketim sınırıdır. CPU ve memory aynı şekilde uygulanmaz.

```text
request -> scheduler placement / CPU contention weight
CPU limit -> cgroup throttling
memory limit -> cgroup boundary -> pressure -> OOM kill
```

Kubernetes resmi dokümantasyonuna göre CPU limit kernel tarafından throttling ile uygulanır; memory limit aşımı ise memory pressure tespit edildiğinde OOM kill ile sonuçlanabilir. Request değerleri scheduling'de kullanılır ve workload uygun kaynak varsa request'in üstünde tüketebilir.

## Rightsizing
Ortalama kullanım tek başına yeterli değildir. p95/p99, burst, startup, sidecar, GC ve autoscaler davranışını ölç. Çok yüksek request utilization'ı düşürür; çok düşük request contention/eviction riskini büyütebilir. Agresif CPU limit latency'yi throttling ile bozabilir.

## Mülakat soruları
- Request ve limit farkı nedir?
- CPU limit neden kill yerine throttling üretir?
- Memory OOM ile node-pressure eviction farkı nedir?
- HPA CPU utilization neden request kalitesinden etkilenir?
- Multi-tenant cluster'da quota ve fairness nasıl kurulur?

## Production bağlantısı
Rightsizing'i latency, throttled seconds, RSS/working set, OOM restart ve scheduler pending time ile birlikte değerlendir. Capacity planning'i yalnız maliyet optimizasyonu değil reliability kontrolü olarak gör.

## Habitat bağlantısı
Farklı storage backend adapter'ları farklı CPU/memory profillerine sahip olabilir. Tek bir request/limit şablonu yerine workload class ve backend davranışına göre profile kullanmak noisy-neighbor riskini azaltır.

## Kaynaklar
- Kubernetes — Resource Management: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
- Kubernetes — Resource Quotas: https://kubernetes.io/docs/concepts/policy/resource-quotas/
