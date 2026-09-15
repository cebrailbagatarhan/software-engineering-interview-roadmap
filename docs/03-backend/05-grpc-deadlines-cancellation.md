# gRPC Deadlines, Cancellation & Budget Propagation

## Neden önemli?
Bir RPC deadline'ı uçtan uca latency ve resource budget'ın bir parçasıdır. gRPC varsayılan olarak deadline koymayabileceği için client'lar workload'a uygun deadline'ı açıkça belirlemelidir.

## Mental model
```text
request budget
   |
service A --spent--> remaining budget --> service B
   ^                                      |
   +----------- cancellation <------------+
```

## Temel noktalar
- Deadline client'ın artık sonucu beklemeyeceği zamanı ifade eder.
- Downstream çağrılar kalan budget'ı devralmalıdır.
- Deadline/cancellation sonrası application work kendiliğinden her durumda durmaz; handler cancellation-aware olmalıdır.
- Önceden yapılmış side effect cancellation ile rollback olmaz.
- Write RPC tasarımında idempotency, transaction boundary ve retry policy birlikte ele alınır.

## Mülakat derinliği
Senior aday tail latency, propagation ve abandoned work'ü; Staff aday retry amplification, admission control, SLO budget ve observability'yi de tartışmalıdır.

## Production failure modes
Deadline yokluğu, hop başına budget reset, cancellation sonrası CPU/DB işini sürdürme, write retry duplicate'leri ve yalnız average latency ile timeout seçimi.

## Kaynaklar
- https://grpc.io/docs/guides/deadlines/
- https://grpc.io/docs/guides/cancellation/
- https://grpc.io/docs/what-is-grpc/core-concepts/
