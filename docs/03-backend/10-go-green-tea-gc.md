# Go 1.26 Green Tea GC: Locality, GC CPU ve Production Rollout

## Neden önemli?
Go 1.26 ile Green Tea garbage collector varsayılan hale geldi. Interview açısından konu yalnız yeni runtime özelliğini bilmek değil; tracing GC correctness, memory locality, CPU cache, benchmark yorumlama ve production rollout reasoning'ini birleştirmektir.

## Mental model
```text
roots -> reachable objects
             |
       page-local batches
        /     |      \
     page A page B  page C
       |
seen/scanned metadata -> scan -> discover more pages

locality ↑  work-list pressure ↓  GC CPU potentially ↓
```

## Temel mekanizma
Go GC tracing mark-sweep ailesindedir. Green Tea reachable graph'ın semantics'ini değiştirmez; traversal ve marking/scanning işinin organizasyonunu page locality lehine değiştirir. Whole pages work list üzerinde taşınabilir, reachable object metadata'sı page-local takip edilir ve page queue üzerinde beklerken birden fazla object'in birikmesi daha düzenli scanning üretir.

Modern CPU'da locality önemlidir: birbirine yakın metadata/object scanning cache hit ihtimalini yükseltir. Yeni amd64 işlemcilerde vector instructions küçük-object scanning'i hızlandırabilir. Bunun getirisi heap shape ve workload'a bağlıdır; her uygulama aynı kazancı görmez.

## Interview soruları
- Tracing GC'nin correctness invariant'ı nedir?
- Page batching neden object-at-a-time traversal'dan hızlı olabilir?
- GC CPU kazancı ile total process CPU kazancı neden farklıdır?
- Allocation-heavy ve pointer-heavy workload nasıl farklı davranabilir?
- Runtime upgrade'i production'da nasıl canary edersin?

## Beklenen cevap derinliği
Mid seviyede mark/sweep, roots ve heap açıklanmalı. Senior locality, allocation rate, CPU profile ve tail latency'yi bağlamalı. Staff/Principal representative workload, architecture cohort, regression budget ve rollback stratejisini tartışmalıdır.

## Mini alıştırma
CPU'nun %15'i GC, GC overhead improvement %30 ise Amdahl-benzeri kaba total CPU kazancını hesapla. Sonra allocation rate, RSS ve p99 değişirse bu sonucun neden geçersizleşebileceğini açıkla.

## Proje
Aynı servis workload'unu Go 1.26 default Green Tea ve `GOEXPERIMENT=nogreenteagc` build'lerinde çalıştır; CPU, RSS, allocation rate, throughput ve p99 karşılaştır.

## Failure modes / trade-off / production
Microbenchmark'i production fleet'e genellemek, GC yüzdesini total CPU yüzdesi sanmak, memory/tail-latency regression'ını kaçırmak ve CPU architecture segmentasyonunu yapmamak sık hatalardır. Rollout runtime version + architecture + workload sınıfı bazında gözlemlenmelidir.

## Kaynaklar
- https://go.dev/doc/go1.26
- https://go.dev/blog/greenteagc
- https://go.dev/blog/go1.26
