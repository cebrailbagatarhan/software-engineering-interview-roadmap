# Linux cgroups v2 ve Resource Isolation

## Neden var?
Aynı Linux host üzerindeki workload'lar CPU, memory ve IO gibi sonlu kaynaklar için yarışır. cgroup süreçleri hiyerarşik gruplara ayırır ve bu kaynakların accounting/control politikasını uygular. cgroup v2 unified hierarchy kullanır.

## Mental model
```text
host
└─ root cgroup
   ├─ latency-critical API
   └─ batch workers

controller policy + contention -> resource distribution
```

## CPU
`cpu.weight` relative paylaşımı, `cpu.max` absolute bandwidth sınırını ifade eder. CPU quota aşırı sıkıysa workload çalışmaya devam etse bile throttling tail latency'yi bozabilir.

## Memory
- `memory.current`: mevcut kullanım.
- `memory.high`: hard OOM sınırı olmadan reclaim/throttling baskısı.
- `memory.max`: hard usage limit; reclaim yeterli değilse cgroup OOM davranışı oluşabilir.

## Container bağlantısı
Container tek başına kernel primitive değildir. Runtime; namespace, cgroup, filesystem/capability ve diğer kernel mekanizmalarını bir araya getirir. Namespace “neyi görebilirim?”, cgroup ise kabaca “ne kadar kaynak tüketebilirim?” sorusuna cevap verir.

## Interview prompts
- weight ve quota farkı nedir?
- memory.high neden memory.max'ten ayrı?
- CPU throttling p99'u nasıl bozar?
- noisy-neighbor nasıl teşhis edilir?

## Production trade-off
Resource policy kapasite planlamasının parçasıdır. Limitleri körlemesine küçültmek utilization'ı artırabilir fakat latency ve restart riskini büyütür. Kritik servislerde saturation sinyalleri, pressure ve throttling metrikleri ortalama utilization kadar önemlidir.

## Kaynak
Linux Kernel — Control Group v2: https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html
