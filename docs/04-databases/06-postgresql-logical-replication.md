# PostgreSQL Logical Replication, Slots & Failover

## Konu anlatımı
PostgreSQL logical replication, fiziksel block kopyalamak yerine publication tarafından seçilen mantıksal tablo değişikliklerini subscriber'a taşır. Publication hangi tabloların ve DML türlerinin yayınlanacağını; subscription bağlantı ve apply tarafını tanımlar. Aktif subscription normalde publisher tarafında bir logical replication slot kullanır.

Slot subscriber'ın henüz tüketmediği WAL bilgisinin kaybolmasını önler; bu nedenle lag yalnız freshness problemi değildir, publisher disk kapasitesi problemine dönüşebilir. UPDATE/DELETE için satır eşleme gerektiğinden uygun `REPLICA IDENTITY` önemlidir. Initial synchronization ve steady-state apply ayrı kapasite/failure yüzeyleridir.

PostgreSQL 18 logical replication failover için subscription slot'larının physical standby'a senkronize edilmesini destekler. Slot synchronization asenkron olduğundan promotion öncesi slot readiness doğrulanmalıdır.

## Mental model
```text
Publisher table -> WAL -> logical decoding -> publication
                              |
                        replication slot
                              |
                              v
                         Subscriber
                         apply worker

subscriber lag -> retained WAL -> publisher disk pressure
```

## Mülakat soruları
- Physical ve logical replication farkı nedir?
- Publication/subscription sorumlulukları nasıl ayrılır?
- Slot hangi garantiyi ve hangi riski getirir?
- Replica identity neden önemlidir?
- Initial sync ve steady-state apply nasıl ayrılır?
- Publisher failover nasıl güvenli yapılır?

## Seviye beklentisi
**Mid:** publication/subscription ve async apply. **Senior:** slot retention, replica identity, lag ve conflicts. **Staff:** failover topology, schema compatibility, capacity ve runbook.

## Mini alıştırma
6 saat geride kalan subscriber için slot lag, retained WAL, disk headroom ve apply throughput sinyallerini kullanarak recovery planı yaz.

## Proje fikri
İki PostgreSQL instance arasında logical replication kur; subscriber'ı durdurup WAL retention büyümesini ölç ve kontrollü catch-up uygula.

## Production / failure modes
Unmonitored slots, eksik replica identity, DDL'nin otomatik replike edildiğini varsaymak, initial-copy bandwidth'ini hesaba katmamak ve failover slot readiness'i test etmemek temel risklerdir.

## Kaynaklar
- https://www.postgresql.org/docs/18/logical-replication.html
- https://www.postgresql.org/docs/18/logical-replication-publication.html
- https://www.postgresql.org/docs/18/logical-replication-subscription.html
- https://www.postgresql.org/docs/18/logical-replication-failover.html
