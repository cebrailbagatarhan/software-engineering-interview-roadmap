# Apache Kafka Tiered Storage: Hot/Cold Logs & Remote Fetch Economics

## Konu anlatımı
Tiered Storage, Kafka log storage'ını local hot tier ve remote long-retention tier olarak ayırır. Active/recent segment'ler broker diskinde kalırken tamamlanmış eski segment'ler remote storage'a kopyalanabilir. Amaç broker compute lifecycle'ını uzun süreli storage kapasitesinden kısmen ayırmaktır.

```text
producer -> partition log -> local active/recent
                              |
                         segment roll
                              v
                    RemoteStorageManager
                              |
                       remote storage
                              |
                    old/backfill fetch
```

## Mental model
Local tier = hızlı tail reads ve sınırlı hot window. Remote tier = daha ucuz uzun retention, fakat daha yüksek latency/request/egress maliyeti.

## İçeride ne oluyor?
`remote.log.storage.system.enable` broker remote-log servislerini, `remote.storage.enable` topic özelliğini açar. `local.retention.*` local window'u; `retention.*` toplam retention'ı belirler. RemoteLogMetadataManager remote segment lifecycle metadata'sını yönetir. Remote reads backfill ve recovery için değerlidir fakat object-store latency ve throughput sınırlarını sisteme taşır. Güncel Kafka 4.3 dokümantasyonu compacted topic desteğini hâlâ limitation olarak listeler.

## Mülakat soruları
- Tiered storage broker disk maliyetini nasıl değiştirir?
- Local retention ile total retention farkı nedir?
- Active segment neden remote'a hemen taşınmaz?
- Remote metadata neden correctness state'idir?
- Backfill tail-read'den nasıl farklıdır?
- Senior: remote-store outage etkisi nedir?
- Staff: hot window nasıl boyutlandırılır?
- Principal/CTO: SSD/object storage/egress economics nasıl modellenir?

## Beklenen cevap seviyesi
Junior partition/segment/retention; Mid local-vs-remote; Senior metadata/fetch/failure; Staff capacity/backfill isolation; Principal/CTO economics, compliance ve provider/plugin risk.

## Mini alıştırma
5 TB/gün ingest, 7 gün local ve 90 gün total retention için yaklaşık local/remote logical storage hesapla; backfill maliyetini tartış.

## Proje fikri
Test cluster'da kısa segment roll/local retention ile tiered storage kur; eski offset'ten consume ederek remote fetch latency/throughput'u tail-read ile kıyasla.

## Failure modes / trade-off / production
Remote storage'u local disk latency'sinde varsaymak, metadata'yı kritik state saymamak, backfill ile live traffic'i boğmak, retention/delete semantics'i test etmemek ve unsupported compacted-topic varsayımı temel risklerdir. Local/remote bytes, copy lag/failure, remote-fetch latency/rate, object-store errors/egress ve consumer lag izlenir.

## Kaynaklar
- https://kafka.apache.org/43/operations/tiered-storage/
- https://kafka.apache.org/43/configuration/tiered-storage-configs/
