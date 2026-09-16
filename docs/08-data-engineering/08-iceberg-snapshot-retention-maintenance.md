# Apache Iceberg Snapshot Retention, Branches & Safe Maintenance

## Konu anlatımı
Iceberg her write'ta yeni snapshot üretir. Snapshot'lar reader isolation, time travel ve rollback sağlar; retention sınırsızsa metadata/storage büyür. `expire_snapshots`, retention dışındaki eski snapshot'ları metadata'dan çıkarır ve artık geçerli snapshot'larca referans edilmeyen dosyaların temizlenmesini sağlar.

Branches ve tags snapshot'lara named reference ve bağımsız lifecycle verir. Bu yüzden audit tag'i eski bir snapshot'ı koruyabilir. `delete orphan files` farklıdır: table metadata graph'ında hiç referans edilmeyen, örneğin failed write'tan kalmış dosyaları age guard ile temizler.

## Mental model
```text
main -> S10 -> S11 -> S12
         ^             ^
       audit tag      current

expiration: retention + refs graph
orphan cleanup: no metadata reference + safe age cutoff
```

## İçeride ne oluyor?
Snapshot log, manifests ve data/delete-file referansları table state'i oluşturur. Streaming commit'leri snapshot ve manifest sayısını hızlı büyütebilir. Snapshot expiration, old metadata cleanup, data-file compaction ve manifest rewrite ayrı maintenance operasyonlarıdır; scheduler bunları catalog/object-store kapasitesine göre sınırlar.

## Mülakat soruları
- Snapshot expiration ile orphan deletion farkı?
- Tag neden snapshot expiration'ı engeller?
- Streaming table neden daha sık maintenance ister?
- Compaction ile expiration neden farklıdır?
- Orphan cutoff nasıl güvenli seçilir?

## Beklenen cevap seviyesi
Mid: snapshot/time travel. Senior: refs, orphan safety, streaming metadata. Staff: fleet scheduler, concurrency ve storage/catalog load. Principal/CTO: audit/compliance retention ile maliyet dengesi.

## Mini alıştırma
Main 7 gün, audit tag 180 gün, test branch 3 gün tutuyor. 120 günlük tagged snapshot'ın neden korunduğunu ve orphan cleanup'ın neden ayrı age guard istediğini açıkla.

## Proje fikri
`iceberg-maintenance-planner`: snapshot/ref inventory, dry-run expiration, reclaim-byte tahmini ve protected-ref raporu.

## Production bağlantısı
Snapshot expiration'ı backup sanmak, ref retention'ı unutmak veya orphan threshold'u agresif seçmek veri kaybı/operasyon riski yaratır. Snapshot count, metadata size, small-file count, maintenance duration/failure ve reclaimed bytes izlenmelidir.

## Kaynaklar
- https://iceberg.apache.org/docs/latest/maintenance/
- https://iceberg.apache.org/docs/latest/branching/
- https://iceberg.apache.org/docs/latest/spark-procedures/
- https://iceberg.apache.org/docs/latest/spark-structured-streaming/
