# Fenwick Tree, Prefix Aggregates & Update/Query Economics

## Neden var?
Dinamik bir array'de point update ve prefix aggregate query'lerini birlikte ucuz yapmak isteriz. Naive array update'i `O(1)` yapabilir ama prefix sum `O(n)` olur. Prefix-sum array query'yi `O(1)` yapar fakat tek update sonrasındaki birçok prefix değiştiği için update `O(n)` olur. Fenwick Tree (Binary Indexed Tree) ikisini tipik olarak `O(log n)`'de dengeler ve `O(n)` memory kullanır.

## Mental model
1-based indexing'de `lowbit(i) = i & -i`.

```text
index:   1 2 3 4 5 6 7 8
lowbit:  1 2 1 4 1 2 1 8

prefix(7):
  tree[7]  -> [7..7]
+ tree[6]  -> [5..6]
+ tree[4]  -> [1..4]
```

**Invariant:** Query path'indeki bloklar overlap etmeden hedef prefix'i kaplar; update path'indeki her node güncellenen index'i kapsar.

## Lowbit neden çalışır?
Two's-complement representation'da `i & -i` en düşük set bit'i izole eder. Bu bit, Fenwick slot'unun temsil ettiği block size'dır.

Prefix query:
```text
sum = 0
while i > 0:
  sum += tree[i]
  i -= i & -i
```

Point update:
```text
while i <= n:
  tree[i] += delta
  i += i & -i
```

Her adım binary representation'da anlamlı bir bit seviyesini değiştirdiği için ziyaret edilen node sayısı `O(log n)`'dir.

## Range query ve algebra
Sum için:
`range(l,r) = prefix(r) - prefix(l-1)`.

Bu difference trick aggregate operation'ın inverse'inin bulunmasına dayanır. Bu nedenle “Fenwick Tree her associative operation için aynı range-query tekniğini verir” demek doğru değildir. Segment tree arbitrary range metadata ve daha genel combine fonksiyonlarında daha esnektir.

## Fenwick vs Segment Tree
Fenwick Tree:
- compact array representation,
- küçük constant factor,
- prefix-oriented aggregates,
- basit point update/query.

Segment Tree:
- arbitrary interval query,
- richer node metadata,
- lazy propagation ile range update,
- daha fazla memory/implementation complexity.

## Coordinate compression
Key domain çok büyük/sparse ise değerleri sorted unique rank'lere map edip Fenwick Tree üzerinde frequency tutabilirsin. Inversion count bunun klasik örneğidir: soldan/sağdan ilerlerken daha küçük/büyük görülen elemanların sayısını prefix frequency query ile bulursun. Duplicate değerlerde rank ve strict/non-strict comparison semantics açık olmalıdır.

## Mülakat soruları
1. Prefix array ile Fenwick Tree trade-off'u nedir?
2. `i & -i` neyi hesaplar?
3. Query/update neden `O(log n)`?
4. Range sum nasıl çıkarılır?
5. Segment tree ne zaman daha uygundur?
6. Mid: inversion count nasıl çözülür?
7. Senior: duplicate değerli coordinate compression nasıl yapılır?
8. Staff: local mutable aggregate ile distributed durable aggregate arasındaki sınır nedir?

## Seviyeye göre cevap
- **Junior:** prefix aggregate ve update/query maliyetini açıklar.
- **Mid:** lowbit traversal, range sum ve inversion count kodlar.
- **Senior:** algebraic şartlar, compression, overflow ve cache davranışını tartışır.
- **Staff:** concurrency, persistence, partitioning ve production aggregate ihtiyacını veri yapısı seçimine bağlar.

## Mini alıştırma
`[3,1,4,1,5,9,2,6]` için tree'yi elle oluştur. `prefix(7)` path'ini yaz. Index 3'e `+5` uygulandığında hangi tree slot'larının değiştiğini göster.

## Mini proje
`fenwick-benchmark`: naive array, prefix array, Fenwick Tree ve segment tree implement et. 1M elemanda read-heavy ve write-heavy workload çalıştır. Throughput, memory footprint ve p99 operation latency ölç.

## Failure modes / production
0-based/1-based index karıştırmak, integer overflow, inverse-operation şartını unutmak, compression'da duplicate semantics'i bozmak ve concurrent update'leri synchronization olmadan yapmak tipik hatalardır. Fenwick Tree leaderboard/rank, mutable frequency table, cumulative counters ve offline analytics için faydalıdır; distributed durability/consistency gerektiğinde local data structure tek başına sistem tasarımı değildir.

## Kaynaklar
- Peter M. Fenwick, “A New Data Structure for Cumulative Frequency Tables”, Software: Practice and Experience 24(3), 1994: https://doi.org/10.1002/spe.4380240306
- CP-Algorithms — Fenwick Tree: https://cp-algorithms.com/data_structures/fenwick.html
