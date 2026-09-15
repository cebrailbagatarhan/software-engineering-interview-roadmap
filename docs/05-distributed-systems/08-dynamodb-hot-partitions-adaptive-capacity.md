# DynamoDB Partition Keys, Hot Partitions & Adaptive Capacity

## Konu anlatımı
DynamoDB'de partition key veri ve request load dağılımının scaling primitive'idir. Düşük-cardinality veya aşırı popüler key hot partition oluşturabilir. Adaptive capacity uneven traffic'i daha iyi karşılar ancak fiziksel partition/item sınırlarını kaldırmaz. AWS'nin güncel dokümantasyonunda partition başına tasarım sınırı 3,000 read units/s ve 1,000 write units/s olarak verilir. Write sharding sıcak logical key'i dağıtabilir; read fan-out ve aggregation karmaşıklığı getirir.

## Mental model
```text
hot key -> one partition -> throttle
   |
write shard #0..#N
   |
multiple partitions -> more write spread
                      -> more read fan-out
```

## Mülakat soruları
- Partition key neden yalnız uniqueness değildir?
- Table kapasitesi varken neden throttle olabilir?
- Adaptive capacity neyi çözmez?
- Write sharding trade-off'u nedir?

## Beklenen cevap seviyesi
Mid: partition/sort key. Senior: hot key, capacity units, access patterns, sharding. Staff: skew, GSI etkisi, migration, cost ve consistency.

## Mini alıştırma
`eventType=CLICK` hot key tasarımını iki alternatif partition-key stratejisiyle yeniden modelle.

## Proje fikri
Zipf traffic ile naive/sharded key throttling ve p99 latency karşılaştırması yapan load-test harness.

## Failure modes / production
Low-cardinality key, monoton timestamp key, GSI skew, adaptive capacity'yi sınırsız sanmak ve fan-out maliyetini unutmak. Top-key distribution, throttling, consumed capacity ve p95/p99 izlenmelidir.

## Kaynaklar
- AWS partition key best practices: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html
- AWS adaptive capacity: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/burst-adaptive-capacity.html
