# Topological Sort, DAG Scheduling & Cycle Detection

## Neden önemli?
Dependency graph problemleri package manager, CI build graph, workflow engine ve data pipeline scheduler'larında tekrar eder. Topological sort, DAG düğümlerini her `u -> v` bağımlılığında `u` önce gelecek biçimde lineerleştirir; cycle varsa geçerli sıra yoktur.

## Mental model
Kahn algoritmasında `indegree=0` düğümler hazır iş kuyruğudur. Bir düğüm tamamlanınca outgoing dependency'leri kaldırılmış gibi komşuların indegree'i azalır. Queue tükenmesine rağmen tüm düğümler işlenmediyse cycle vardır.

```text
A ---> C ---> E
 \     ^
  \   /
   > B ---> D

ready = indegree 0
processed < V after ready empties => cycle
```

## Algoritma ve karmaşıklık
Adjacency list ve indegree array oluştur: `O(V+E)`. Her node ve edge en fazla bir kez işlenir: toplam `O(V+E)`. Storage da graph dahil `O(V+E)` olur. Lexicographically smallest order için FIFO queue yerine min-heap kullanılabilir; frontier operasyonları logaritmik hale gelir.

DFS alternatifi postorder kullanır; white/gray/black state içinde gray node'a edge cycle belirtir. Kahn scheduling, DFS dependency traversal sezgisine daha yakındır.

## Mülakat derinliği
- Junior: DAG, indegree, queue ve `O(V+E)`.
- Mid: cycle detection, multiple valid orders, heap varyantı, DFS alternatifi.
- Senior: parallel scheduling, critical path, incremental updates, failure propagation.
- Staff: büyük dependency graph'larında ownership, caching ve scheduler control plane.

## Production trade-off'ları
Topological validity task'ın güvenle çalışacağı anlamına gelmez. Parallelism limit, retry/idempotency, artifact caching, priority, resource constraints ve downstream failure semantics ayrıca tasarlanır. Duplicate edge, disconnected component ve deterministic-order gereksinimleri sık hata kaynaklarıdır.

## Alıştırma / proje
Bir `dag-build-runner` yaz: YAML graph oku, cycle'ı reddet, ready task'ları worker pool'a ver, failure downstream'ini skip et ve critical-path süresini raporla.

## Kaynaklar
- https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/
- https://docs.python.org/3/library/graphlib.html
