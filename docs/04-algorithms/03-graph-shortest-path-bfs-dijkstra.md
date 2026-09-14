# Graph Shortest Path: BFS vs Dijkstra

## Önce problemi modelle
Shortest path seçiminde ilk soru edge cost modelidir. Unweighted veya eşit maliyetli graph için BFS; non-negative ve değişken edge weight için Dijkstra doğal başlangıç noktasıdır.

## BFS
Queue ile layer-by-layer ilerler. İlk kez ulaşılan node minimum hop distance ile bulunur.

## Dijkstra
```text
dist[source] = 0
priority queue -> en düşük tentative distance
pop u -> her (u,v,w) için relax
if dist[u] + w < dist[v]: update + push
```

Binary heap ile tipik complexity `O((V+E) log V)` seviyesindedir. Decrease-key olmayan heap implementasyonlarında yeni entry push edilip pop sırasında stale entry filtrelenebilir.

## Correctness intuition
Dijkstra'nın greedy adımı non-negative edge varsayımına dayanır. Minimum tentative distance ile seçilen node'un daha sonra daha ucuz bir yolla bulunamayacağı invariant'ı negative edge ile kırılır.

## Interview prompts
- BFS neden shortest hop path verir?
- Dijkstra negative edge ile neden güvenli değildir?
- predecessor map ile path nasıl reconstruct edilir?
- stale heap entries nasıl yönetilir?
- grid problemi hangi durumda BFS'den Dijkstra'ya dönüşür?

## Production bağlantısı
Routing, dependency graph analizi ve weighted state-space problemlerinde model seçimi implementation'dan daha önemlidir. Büyük graph'larda memory layout, graph partitioning ve heuristic search ayrıca değerlendirilir.

## Kaynaklar
- Python heapq: https://docs.python.org/3/library/heapq.html
- E. W. Dijkstra (1959), A note on two problems in connexion with graphs.
