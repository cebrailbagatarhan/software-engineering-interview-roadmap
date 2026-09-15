# Spark Shuffle, Data Skew & Adaptive Query Execution

## Mental model
```text
partitions -> wide operation -> shuffle -> new partitions
                                      -> skewed partition -> straggler
runtime statistics -> AQE -> adapt join/partition/skew decisions
```

Spark'ta join, groupBy ve repartition gibi wide operasyonlar shuffle boundary yaratır. Shuffle network I/O, serialization, disk spill ve scheduling maliyeti taşır. Data skew birkaç büyük partition'ın stage completion süresini belirlemesine yol açabilir. Mitigation workload'a göre broadcast join, key redesign, salting veya skew-aware optimization olabilir. Adaptive Query Execution runtime statistics kullanarak partition coalescing, join strategy ve skew kararlarını execution sırasında iyileştirebilir; kötü data modelinin yerine geçmez.

## Mülakat odağı
- Narrow vs wide transformation.
- Shuffle neden pahalı?
- Skew ve straggler teşhisi.
- Broadcast join ve memory trade-off'u.
- Salting ve AQE sınırları.

## Mini alıştırma
Median task 20 saniye iken tek task 14 dakika sürüyorsa Spark UI'da bakacağın sinyalleri ve üç mitigation seçeneğini yaz.

## Failure modes / production
Körlemesine partition artırmak; broadcast memory riskini hesaplamamak; spill/network'i atlamak; AQE'yi kötü partition key tasarımının yerine koymak.

## Kaynaklar
- https://spark.apache.org/docs/latest/sql-performance-tuning.html
- https://spark.apache.org/docs/latest/rdd-programming-guide.html
- https://spark.apache.org/docs/latest/
