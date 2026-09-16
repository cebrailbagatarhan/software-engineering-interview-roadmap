# S3 Conditional Writes, Optimistic Concurrency & Object-Store Coordination

## Konu anlatımı
Amazon S3 conditional writes HTTP precondition'ları ile write sırasında object state doğrulaması sağlar. `If-None-Match: *` create-if-absent, `If-Match: <ETag>` ise optimistic compare-and-swap benzeri bir primitive sağlar.

## Mental model
```text
GET object + ETag=v7
       |
     modify
       v
PUT If-Match:v7
       |
 current == v7 ?
    /       \
 write    412
            |
      reread/retry
```

## İçeride ne oluyor?
Aynı key'e yarışan `If-None-Match:*` write'larında ilk tamamlanan işlem başarılı olabilir, diğerleri 412 alır. Concurrent delete gibi yarışlarda 409 da görülebilir. `If-Match` stale writer'ı tespit eder. Bu primitive multi-object transaction değildir; ETag de her durumda business version veya content hash sayılmamalıdır. Bucket policy conditional-write kullanımını zorunlu kılabilir.

## Mülakat soruları
- `If-None-Match:*` ve `If-Match` farkı nedir?
- Lost update nasıl engellenir?
- 412 ve 409 nasıl ele alınır?
- ETag neden genel business version değildir?
- Retry'da neden reread/recompute gerekir?
- Staff: multi-object invariant için ne eklenir?

## Beklenen cevap seviyesi
Junior: overwrite/precondition. Mid: ETag ve 412. Senior: optimistic concurrency/retry. Staff: multi-writer coordination. Principal/CTO: consistency, cost ve operational complexity.

## Mini alıştırma
`catalog/current.json` için GET+ETag -> modify -> conditional PUT akışını iki concurrent writer ile yürüt.

## Proje fikri
`s3-cas-catalog-lab`: concurrent writers, 412 handling ve invariant testleri olan manifest pointer servisi.

## Production bağlantısı / failure modes
Unconditional lost update, 412'yi kör retry etmek, stale payload'u reread etmeden yeniden göndermek, ETag semantics'ini yanlış varsaymak ve multi-key transaction beklemek başlıca risklerdir. 412/409 rate, retries, hot-key contention ve invariant violations izlenir.

## Kaynaklar
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes.html
- https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes-enforce.html
