# Python Runtime Upgrades: GC Rollback & Production Memory Regressions

## Konu anlatımı
Runtime internals uygulamanın görünmez dependency'sidir. Python 3.14.0–3.14.4 ile gelen incremental garbage collector, production ortamlarından gelen ciddi memory-pressure raporları nedeniyle Python 3.14.5'te önceki generational GC yaklaşımına geri döndürüldü. Bu örnek runtime upgrade'lerinin yalnız correctness değil resource envelope açısından da test edilmesi gerektiğini gösterir.

## Mental model
```text
workload -> allocations -> GC policy -> reclaim / pauses -> RSS + CPU + tail latency -> container/OOM boundary
```

GC memory leak ile aynı değildir. Reachable/live set, allocator fragmentation, delayed reclamation ve runtime policy RSS'i etkileyebilir. Canary'de p50/p99 latency, RSS/working set, CPU, throughput, OOM ve GC telemetry eski runtime ile karşılaştırılmalıdır.

## Mülakat derinliği
Junior: allocation/reachability/GC. Mid: generations, pause, RSS. Senior: workload benchmark, memory limit, canary ve rollback. Staff: fleet rollout waves ve compatibility. CTO/EM: support lifecycle, upgrade velocity ve incident economics.

## Failure modes
Microbenchmark'ı production sanmak; average RSS ile yetinmek; container limit altında test etmemek; kısa canary; rollback artifact'i saklamamak.

## Alıştırma / proje
İki runtime'ı allocation-heavy workload altında aynı container limit ile çalıştır. RSS p95, OOM, CPU, throughput ve p99 latency için promotion gate üret.

## Kaynaklar
- https://www.python.org/downloads/release/python-3145/
- https://www.python.org/downloads/release/python-3147/
- https://peps.python.org/pep-0745/
