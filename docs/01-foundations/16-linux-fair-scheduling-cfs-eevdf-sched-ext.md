# Linux Fair Scheduling — CFS, EEVDF, CPU Isolation ve sched_ext

## Mental model
```text
runnable tasks -> fairness accounting -> eligible? -> virtual deadline -> CPU
                       vruntime / lag                         |
                                                   preempt/sleep/wakeup

sched_ext: workload -> BPF scheduling policy -> dispatch queue -> CPU
                            | error/stall
                            +-------------> default scheduling
```

## Konu anlatımı
Scheduler fairness, latency, throughput, locality ve isolation arasında politika uygular. CFS ideal multitasking CPU'yu `vruntime` ile yaklaşıklar. Güncel Linux scheduler dokümantasyonunda CFS'in EEVDF'ye yer açtığı belirtilir. EEVDF task'ın adil CPU payına göre lag hesaplar; lag >= 0 olan eligible task'lar arasından virtual deadline'ı en erken olanı seçer. Bu, latency-sensitive task'ların kısa requested slice'larını fairness modeli içinde ifade etmeyi sağlar.

`sched_ext`, BPF programlarıyla scheduling policy tanımlamaya izin verir. Kernel dokümantasyonuna göre BPF scheduler error üretirse veya runnable task stall olursa default scheduling davranışı geri yüklenebilir; bu özellik programmable scheduler rollout'unda önemli bir safety boundary'dir.

## İçeride ne oluyor?
- Runnable task CPU adayıdır; sleeping/blocked task değildir.
- CFS `vruntime` ile ideal fair CPU'daki ilerlemeyi yaklaşıklar; nice/weight CPU payını etkiler.
- EEVDF lag ile fairness debt/credit'i, virtual deadline ile seçim önceliğini temsil eder.
- Preemption responsiveness karşılığında context-switch/cache/TLB maliyeti yaratır.
- CPU affinity ve cpuset placement'ı sınırlar; locality ile load balancing arasında trade-off oluşturur.
- Container CPU throttling, host run-queue contention ve steal time ayrı failure kaynaklarıdır.
- `sched_ext` arbitrary BPF policy'lerine izin verir; starvation detection, fallback ve blast-radius kontrolü production tasarımının parçasıdır.

## Mülakat soruları
1. Runnable ile running farkı nedir?
2. Context switch neden bedava değildir?
3. CFS `vruntime` neyi yaklaşıklar?
4. EEVDF'de lag, eligibility ve virtual deadline ilişkisi nedir?
5. CPU affinity hangi durumda tail latency'yi iyileştirir veya kötüleştirir?
6. Kubernetes pod CPU throttling ile host scheduler contention nasıl ayrılır?
7. Staff: programmable scheduler rollout'unda starvation ve fallback nasıl yönetilir?
8. Principal: multi-tenant fleet'te fairness, latency SLO ve utilization nasıl dengelenir?

## Beklenen cevap seviyesi
- **Mid:** process state, run queue, preemption, priority, context switch.
- **Senior:** vruntime, lag/deadline, locality, affinity ve cgroup throttling.
- **Staff:** NUMA/topology, isolation, sched_ext rollout/fallback ve observability.
- **Principal:** workload classes, fleet economics, tenancy ve policy governance.

## Mini alıştırma
A ve B CPU-bound; C her 5 ms'de uyanıp 500 µs CPU istiyor. Fairness ile C'nin responsiveness hedefi arasındaki gerilimi çiz; kısa slice, dedicated CPU ve custom scheduler seçeneklerini karşılaştır.

## Proje fikri
`scheduler-policy-lab`: CPU-bound ve bursty workload'larda context switches, migrations, throttled time ve p99 latency ölç. Affinity/cpuset varyantlarını karşılaştır; uygun test hostunda `sched_ext` örnek scheduler'ı ile fallback davranışını doğrula.

## Failure modes / production bağlantısı
CPU utilization ile runnable pressure'ı eşitlemek, load average'ı doğrudan saturation sanmak, affinity'yi evrensel optimizasyon kabul etmek ve programmable scheduler'da starvation/fallback test etmemek yaygın hatalardır. Production'da utilization, runnable pressure, throttled time, context switches, migrations, steal time ve p95/p99 latency birlikte okunmalıdır.

## Kaynaklar
- Linux Kernel — Scheduler: https://www.kernel.org/doc/html/latest/scheduler/
- Linux Kernel — CFS: https://www.kernel.org/doc/html/latest/scheduler/sched-design-CFS.html
- Linux Kernel — EEVDF: https://www.kernel.org/doc/html/latest/scheduler/sched-eevdf.html
- Linux Kernel — sched_ext: https://www.kernel.org/doc/html/latest/scheduler/sched-ext.html
- Linux Kernel — CPUsets: https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v1/cpusets.html
