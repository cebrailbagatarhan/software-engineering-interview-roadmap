# Apache Flink Checkpoint Barriers & Exactly-Once

## Konu anlatımı
Flink consistent snapshots için source positions ve operator state'i checkpoint barrier'larıyla koordine eder. Multi-input operator'lerde aligned checkpoint snapshot sınırını korur; backpressure alignment latency yaratabilir. Exactly-once operator state garantisi, external sink side effect'lerinin otomatik olarak exactly-once olduğu anlamına gelmez; sink checkpoint protokolüyle işbirliği yapmalıdır.

## Mental model
```text
source A -- |B42| --\
                    +--> state --> sink
source B -- |B42| --/
checkpoint = positions + state
```

## Mülakat soruları
- Barrier alignment neyi garanti eder?
- Exactly-once state ve delivery nasıl ayrılır?
- Unaligned checkpoint hangi trade-off'u yapar?
- Sink semantics neden end-to-end guarantee'i belirler?

## Beklenen cevap seviyesi
Mid checkpoint/restore; Senior barriers, source offsets ve sink semantics; Staff recovery RTO, state backend, checkpoint SLO ve upgrade/savepoint stratejisini tartışmalıdır.

## Mini alıştırma
Yavaş bir input'un aligned checkpoint duration'a etkisini çiz.

## Proje fikri
Kafka→Flink stateful aggregation hattında failure injection ile correctness ve checkpoint duration ölç.

## Production bağlantısı
Checkpoint storage dayanıklılığı, state büyümesi, restore süresi ve sink transaction/idempotency kapasite ve reliability tasarımının parçasıdır.

## Kaynaklar
- https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/stateful-stream-processing/
- https://nightlies.apache.org/flink/flink-docs-stable/docs/ops/state/checkpoints/
- https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/datastream/guarantees/
