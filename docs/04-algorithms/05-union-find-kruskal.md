# Union-Find, Path Compression & Kruskal

Disjoint Set Union kesişmeyen kümeleri parent-pointer forest ile tutar. `find` representative root'u bulur; `union` iki root'u birleştirir. Union-by-rank/size ve path compression birlikte ağaçları sığ tutar ve operasyonları amortized olarak pratikte sabite çok yakın hale getirir.

```text
Before: 4 -> 3 -> 2 -> 1
find(4) + compression
After:  4 -> 1, 3 -> 1, 2 -> 1
```

Kruskal edge'leri ağırlığa göre sıralar; iki endpoint farklı component'teyse edge'i MST'ye ekleyip union yapar.

## Interview depth
Junior: parent array, find, union. Mid: rank/size, path compression, amortized complexity, Kruskal. Senior: offline connectivity, rollback DSU ve deletion sınırları.

## Alıştırma / proje
Edge stream'i geldikçe component count ve largest component ölçen küçük bir araç yaz; naive DFS ile çalışma süresini karşılaştır.

## Failure modes
Root bulmadan parent mutation invariants'ı bozar; rank/size olmadan kötü şekilli ağaçlar oluşabilir; klasik DSU edge deletion'ı doğal olarak desteklemez.

## Kaynaklar
- https://algs4.cs.princeton.edu/15uf/
- https://algs4.cs.princeton.edu/code/javadoc/edu/princeton/cs/algs4/KruskalMST.html
