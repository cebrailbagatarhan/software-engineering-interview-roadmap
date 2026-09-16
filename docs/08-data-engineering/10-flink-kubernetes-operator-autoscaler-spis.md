# Flink Kubernetes Operator Autoscaler SPIs & Safe Control Loops

## Neden önemli?
Flink Kubernetes Operator 1.16.0 autoscaler'a custom evaluator, scaling executor ve alignment mode için pluggable SPI'lar ekledi. Extension point'leri production'da güvenle kullanmak için autoscaling'i bir feedback-control sistemi olarak modellemek gerekir.

## Mental model
```text
metrics -> evaluator -> desired parallelism -> alignment -> executor
   ^                                                   |
   +---- lag / utilization / backpressure <- workload-+
```

Evaluator karar politikasını, executor kararı uygulama mekanizmasını, alignment ise ilişkili operator'ların parallelism uyumunu belirler. Lag, busy time, backpressure ve checkpoint maliyeti birlikte değerlendirilmelidir.

## Interview katmanları
- Junior: parallelism, throughput, lag.
- Mid: metric -> desired state -> scaling.
- Senior: hysteresis, cooldown, checkpoint/rescale maliyeti, oscillation.
- Staff: custom extension governance, canary, blast radius ve fleet capacity.
- Principal/CTO: throughput SLO, cloud cost, platform standardization ve operational complexity.

## Failure modes ve trade-off
Tek metriğe göre scale etmek, cooldown kullanmamak, rescale/checkpoint maliyetini yok saymak ve custom executor'a sınırsız yetki vermek unstable control loop yaratabilir. Operator upgrade'lerinde default davranış değişiklikleri ayrıca regression test edilmelidir.

## Production checklist
Lag ve busy/backpressured time; checkpoint duration/failure; rescale frequency; desired/actual parallelism; recovery time; compute-minute ve cost/request benzeri unit economics birlikte izlenmelidir.

## Mini proje
Synthetic Kafka workload altında default ve custom evaluator'ı karşılaştır. 5x traffic burst'te lag recovery time, rescale count, checkpoint duration ve compute-minute ölç.

## Kaynaklar
- https://flink.apache.org/2026/09/15/apache-flink-kubernetes-operator-1.16.0-release-announcement/
- https://flink.apache.org/2026/06/25/apache-flink-2.3.0-release-announcement/