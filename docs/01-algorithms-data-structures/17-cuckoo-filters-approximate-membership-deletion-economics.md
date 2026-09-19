# Cuckoo Filters: Approximate Membership & Deletion Economics

**Seviye:** Junior → Staff  
**Alan:** Algorithms & Data Structures / Databases

## Konu anlatımı
Approximate membership yapıları, pahalı exact lookup öncesinde “kesin yok / muhtemelen var” kapısı sağlar. Cuckoo filter tam key yerine kısa fingerprint saklar ve her fingerprint için iki candidate bucket kullanır. Bloom filter’ın aksine entry tabanlı yapı deletion’ı doğal destekler. İki bucket doluysa fingerprint’lerden biri alternatif bucket’a taşınır; yüksek load factor relocation zincirini uzatıp insert failure doğurabilir.

## Mental model
```mermaid
flowchart LR
 K[Key] --> F[Fingerprint]
 K --> I1[Bucket i1]
 F --> I2[Bucket i2 = i1 XOR hash(f)]
 I1 --> B1[Bucket 1]
 I2 --> B2[Bucket 2]
 B1 <-->|relocation| B2
```
**Invariant:** Negative lookup güçlüdür; positive lookup fingerprint collision nedeniyle probabilistic’tir.

## İçeride ne oluyor?
- Fingerprint width false-positive rate ile memory arasında trade-off yaratır.
- Bucket size ve load factor space efficiency ile insertion tail latency’yi belirler.
- Alternative index fingerprint’ten türetildiği için relocation sonrası candidate pair korunur.
- Delete fingerprint slot’unu kaldırır; filter exact identity store değildir.
- Kick sayısı bounded tutulmalı; limit aşılırsa resize/rebuild gerekir.

## Mülakat soruları
1. Bloom filter ve Cuckoo filter farkı nedir?
2. Deletion neden Cuckoo filter’da daha kolaydır?
3. İki candidate bucket nasıl bulunur?
4. Load factor yükseldikçe ne bozulur?
5. False positive ile false negative arasındaki correctness farkı nedir?
6. Senior: concurrent resize nasıl yapılır?
7. Staff: LSM-tree/cache/dedup workload’unda hangi probabilistic structure’ı seçersin?

## Beklenen cevap seviyesi
- **Junior:** approximate membership ve false positive’i tanımlar.
- **Mid:** fingerprint, bucket ve relocation’ı açıklar.
- **Senior:** sizing, concurrency, rebuild ve adversarial input’u tartışır.
- **Staff:** FPR/memory/latency hedeflerinden veri yapısı ve rollout seçer.

## Mini alıştırma
4 slot’lu bucket’larla 12 key ekleyen küçük simülasyon yaz. Candidate bucket ve kick sayısını kaydet; üç key silip lookup sonuçlarını karşılaştır.

## Proje fikri
`cuckoo-filter-lab`: fingerprint width ve bucket size configurable olsun. Bloom filter ile memory/key, throughput, FPR ve insertion failure benchmark’ı yap.

## Failure modes / trade-off / production
Kısa fingerprint yüksek FPR; aşırı doluluk relocation storm; sınırsız kick latency spike; unsafe concurrency false negative; adversarial hashing CPU amplification yaratır. Production’da load factor, kicks/insert, insert-failure, sampled FPR, rebuild duration ve memory/key izlenir.

## Kaynaklar
- Fan et al., *Cuckoo Filter: Practically Better Than Bloom*, CoNEXT 2014: https://www.cs.cmu.edu/~dga/papers/cuckoo-conext2014-abstract.html
- CMU ISTC publication page: https://istc-cc.cmu.edu/publications/papers/2014/cuckoo-conext2014_abs.shtml
