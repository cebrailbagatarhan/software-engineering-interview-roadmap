# Linux PSI, Resource Pressure & Load Shedding

## Konu anlatımı
Linux Pressure Stall Information (PSI), CPU, memory ve I/O contention nedeniyle workload'ların ilerleyemediği zamanı ölçer. Utilization kapasitenin ne kadar kullanıldığını, PSI ise scarcity'nin işe ne kadar stall olarak yansıdığını anlatır.

`/proc/pressure/cpu`, `memory` ve `io` dosyalarında `some` ve `full` sinyalleri, avg10/avg60/avg300 trendleri ve total stall time bulunur. `some` en az bir task'ın stalled olduğu süreyi; `full` bütün non-idle task'ların aynı anda ilerleyemediği ağır pressure durumunu gösterir. cgroup v2 aynı sinyalleri workload bazında sunabilir.

## Mental model
```text
utilization -> capacity consumption
pressure    -> lost progress / stall

traffic -> workload -> CPU|memory|IO -> PSI -> shed/scale/debug
```

## İçeride ne oluyor?
Kernel stall sürelerini aggregate eder ve threshold trigger'larıyla `poll/epoll` tabanlı userspace reaksiyonunu destekler. PSI, queue depth ve latency ile birlikte yorumlandığında noisy neighbor, memory thrashing veya I/O saturation gibi sorunları utilization'dan daha erken ayırabilir.

## Mülakat soruları
- CPU utilization ile CPU pressure farkı nedir?
- `some` ve `full` neyi ölçer?
- Memory usage yüksek ama PSI düşükse ne düşünürsün?
- cgroup PSI neden önemlidir?
- PSI autoscaling/load shedding'e nasıl bağlanır?

## Beklenen cevap seviyesi
Mid: utilization/stall ayrımı. Senior: some/full, windows, cgroup ve SLO korelasyonu. Staff: hysteresis, load shedding ve noisy-neighbor policy. Principal/CTO: reliability headroom ile utilization economics.

## Mini alıştırma
CPU %55, memory %92, memory `some avg10=18`, `full avg10=6`, p99 4x. Üç hipotez ve mitigation sırası yaz.

## Proje fikri
`psi-slo-guard`: PSI + latency korelasyonu ve hysteresis tabanlı low-priority shedding.

## Production bağlantısı
PSI tek başına karar mekanizması değildir. PSI, queue depth, p99 latency, OOM/reclaim, CPU steal ve shed rate birlikte izlenir; threshold'larda hysteresis kullanılarak oscillation azaltılır.

## Kaynaklar
- https://docs.kernel.org/accounting/psi.html
- https://docs.kernel.org/admin-guide/cgroup-v2.html
