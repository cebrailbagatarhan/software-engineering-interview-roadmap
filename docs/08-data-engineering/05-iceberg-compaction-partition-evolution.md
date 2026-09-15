# Apache Iceberg: Small Files, Compaction & Partition Evolution

## Small-file problemi
Çok sayıda küçük data file metadata ve file-open maliyetini büyütür. Iceberg `rewriteDataFiles` ile küçük dosyaları daha büyük dosyalara compact edebilir. Bu işlem query/read efficiency kazanımı karşılığında compute ve write amplification yaratır.

```text
small writes -> [f1][f2][f3][f4]
                    |
             rewriteDataFiles
                    v
              [ larger F ]
```

## Partition evolution
Partition spec metadata üzerinden evolve edilebilir. Eski dosyalar eski spec ile kalır, yeni dosyalar yeni spec ile yazılır; planning her layout için uygun filtre/pruning üretir. Değişiklik eager full-table rewrite gerektirmez.

## Operasyonel tasarım
Compaction trigger'ı file count/size distribution ve query SLA ile bağla. Target file size'ı engine/object-store özellikleriyle benchmark et. Streaming writer ile maintenance concurrency'sini test et. Data-file rewrite ile manifest rewrite'ın farklı maintenance işlemleri olduğunu unutma.

## Failure modes
Over-partitioning, her micro-batch sonrası compaction, yalnız ortalama file size izlemek, partition evolution'ın eski data'yı fiziksel taşıdığını varsaymak ve maintenance compute budget'ını hesaba katmamak.

## Kaynaklar
- https://iceberg.apache.org/docs/latest/maintenance/
- https://iceberg.apache.org/docs/latest/evolution/
