# Java Virtual Threads, Blocking I/O & Concurrency Limits

## Mental model
Virtual thread, Java `Thread` API'sini koruyan fakat OS thread'i yaşamı boyunca sahiplenmeyen hafif bir thread'dir. JDK scheduler çok sayıda virtual thread'i daha az carrier/platform thread üzerinde M:N çalıştırır. Blocking JDK I/O sırasında virtual thread çoğunlukla unmount olur ve carrier başka işi çalıştırabilir.

```text
request/task -> virtual thread --mount--> carrier -> CPU
                         | blocking I/O
                         +--unmount--> carrier freed
```

Concurrency parallelism değildir. Virtual threads I/O-heavy concurrency'de thread-per-request modelini ölçekleyebilir; CPU-bound işi core sayısının ötesinde hızlandırmaz. Virtual thread ucuz diye DB connection, downstream QPS veya memory limitsiz değildir; semaphore, bulkhead, rate limit ve backpressure hâlâ gerekir.

## Interview checkpoints
- Platform vs virtual thread ve M:N scheduling.
- Neden virtual threads pool'lanmamalı?
- 100k virtual thread ile 50 DB connection arasındaki capacity ilişkisi.
- Pinning, observability ve migration riskleri.
- Reactive model ile virtual-thread modelinin trade-off'ları.

## Production failure modes
Downstream capacity'yi limitsiz açmak, CPU-bound workload'u concurrency ile hızlandırmaya çalışmak, thread-local maliyetini küçümsemek, uzun pinning/native bölgelerini ölçmemek ve bottleneck'i DB pool'da bırakıp runtime benchmark'ını yanlış yorumlamak.

## Alıştırma / proje
10.000 concurrent request ve 50 DB connection için queueing modelini çiz. Ardından fixed platform-thread pool ve virtual-thread-per-task sürümlerini throughput, p99, DB pool wait, CPU ve carrier davranışıyla karşılaştıran `virtual-thread-load-lab` oluştur.

## Kaynak
- https://openjdk.org/jeps/444
