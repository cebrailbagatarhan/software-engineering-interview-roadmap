# Flink Kubernetes Operator Autoscaling, Alignment & Control Loops

## Neden önemli?
Stateful streaming autoscaling, stateless HTTP replica scaling'den daha karmaşıktır: parallelism değişimi state repartitioning, checkpoint/recovery, source/sink kapasitesi ve backpressure ile birlikte değerlendirilir.

Apache Flink Kubernetes Operator 1.16.0 (15 Eylül 2026), autoscaler için custom evaluator, scaling executor ve alignment mode SPI'ları; yeni parallelism-alignment davranışı ve Kubernetes-native `ResourceRequirements` desteği getirdi.

## Mental model
```text
metrics / backlog / busy-time
          |
       evaluator
          |
 desired parallelism
          |
 alignment policy
          |
 scaling executor
          |
      job graph
          ^
     backpressure
```

Autoscaler bir feedback control loop'tur. Amaç yalnız lag'i azaltmak değil; SLO, state-movement maliyeti, oscillation ve compute cost'u birlikte optimize etmektir.

## Mülakat derinliği
- Junior: throughput, lag, parallelism.
- Mid: backpressure ve scaling.
- Senior: checkpoint/state movement, cooldown, hysteresis, saturation.
- Staff: control-loop stability, custom policy, multi-job capacity.
- Principal/CTO: latency SLO, cloud cost ve platform standardization.

## Yüksek getirili sorular
1. Streaming autoscaling neden stateless autoscaling'den farklıdır?
2. Backpressure ile source lag nasıl ilişkilidir?
3. Parallelism alignment neyi çözmeye çalışır?
4. State repartitioning scale kararının maliyetini nasıl değiştirir?
5. Cooldown/hysteresis neden gerekir?
6. Autoscaler oscillation nasıl teşhis edilir?

## Production failure modes
CPU'yu tek sinyal sanmak; source/sink bottleneck'ini ayırmamak; cooldown olmadan oscillation; checkpoint/state movement maliyetini yok saymak; downstream kapasiteyi varsaymak.

İzlenecek sinyaller: source lag, busy/backpressured time, checkpoint duration/failure, scale frequency, restart time ve compute cost.

## Alıştırma
20k event/s alan ve task başına 2.5k event/s sürdürülebilir throughput veren pipeline için minimum parallelism'i hesapla; %30 headroom ve scale-action maliyetiyle policy tasarla.

## Proje
`flink-autoscaler-simulator`: evaluator/alignment/executor arayüzleriyle synthetic lag üret; aggressive ve conservative policy'lerde lag, oscillation, scale count ve cost'u karşılaştır.

## Kaynaklar
- https://flink.apache.org/2026/09/15/apache-flink-kubernetes-operator-1.16.0-release-announcement/
- https://nightlies.apache.org/flink/flink-kubernetes-operator-docs-main/docs/custom-resource/autoscaler/
