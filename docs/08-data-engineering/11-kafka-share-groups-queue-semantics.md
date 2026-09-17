# Kafka Share Groups: Queue Semantics, Backpressure & Idempotency

## Problem
Klasik Kafka consumer group partition ownership'i üzerinden ölçeklenir. Work-queue workload'larında ise record-level acquisition, acknowledgement, redelivery ve uzun processing süresini yönetmek gerekir. Kafka Share Groups bu kullanım için queue-benzeri tüketim semantiği sunar.

```text
partitioned log -> share coordinator -> C1/C2/C3
                                      |   |   |
                                     ACK RENEW timeout
                                              |
                                           redelivery
```

## Mental model
Log **verinin kalıcılığıdır**; acquisition ise **geçici work ownership**. Bir record acquired olabilir ama bu source-of-truth'tan silindiği anlamına gelmez. Başarılı processing acknowledgement ile tamamlanır; timeout/failure yeniden teslim yaratabilir. Bu yüzden side-effect'ler idempotent tasarlanmalıdır.

## Production-ready Share Groups
Kafka 4.2 release announcement Share Groups/Kafka Queues özelliğini production-ready olarak duyurur. `RENEW` acknowledgement uzun processing için ownership süresini uzatır; adaptive batching coordinator verimliliğini, lag ve quantity metrikleri ise operability'yi geliştirir.

## Interview invariants
- Delivery semantiğini side-effect semantiğiyle karıştırma.
- Acknowledgement side-effect'in güvenli commit noktasından sonra gelmelidir.
- Redelivery duplicate execution demektir; idempotency/dedup gerekir.
- Poison message için bounded retry ve terminal handling gerekir.
- Consumer concurrency downstream DB/API capacity'sinden bağımsız büyütülemez.
- Backpressure yalnız lag değildir; in-flight work ve processing latency de izlenir.

## Seviye beklentisi
Junior topic/partition/consumer/ack kavramlarını; Mid ownership ve redelivery'yi; Senior idempotency, timeout, poison-message ve backpressure'ı; Staff coordinator scaling, quotas ve multi-tenant isolation'ı; Principal/CTO platform consolidation ile operasyon maliyetini tartışabilmelidir.

## Production metrikleri
Acquired/in-flight record, redelivery rate, acknowledgement outcome, processing p95/p99, coordinator load, downstream saturation ve end-to-end message age.

## Kaynaklar
- https://kafka.apache.org/blog/2026/01/14/apache-kafka-4.2.0-release-announcement/
- https://kafka.apache.org/community/downloads/
