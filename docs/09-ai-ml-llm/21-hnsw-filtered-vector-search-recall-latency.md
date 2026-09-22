# HNSW ANN, Filtered Vector Search & Recall/Latency Tuning

## Konu anlatımı
Exact kNN tüm adaylarla distance hesaplayarak güçlü ground truth verir; ANN daha küçük aday uzayı karşılığında bazı gerçek komşuları kaçırabilir. HNSW çok katmanlı proximity graph kullanır: seyrek üst katmanlar hızlı yön bulur, dense base layer yerel aramayı tamamlar. Search breadth (`ef_search`) arttıkça genellikle recall yükselir; CPU ve latency de artar. Build tarafında `M` graph degree/memory'yi, `ef_construction` build-time candidate breadth ve graph quality'yi etkiler.

Filtered vector search ayrı bir production problemidir. ANN candidate'ları üretildikten sonra selective metadata predicate uygulanıyorsa adayların çoğu elenebilir. Sonuç `LIMIT k`'den az olabilir veya recall düşebilir. pgvector 0.8.0+ iterative scan, yeterli filtered result bulunana ya da scan budget'a ulaşana kadar index'i daha fazla tarayabilir. Alternatifler exact/B-tree prefilter, partial index, partitioning veya native pre-filter'dır.

## Mental model
```mermaid
flowchart TD
 Q[query vector] --> U[sparse upper layer]
 U --> B[dense base layer]
 B --> C[ANN candidates]
 C --> F{metadata filter}
 F -->|enough k| R[top-k]
 F -->|too few| I[expand / iterative scan]
 I --> C
 E[exact top-k sample] --> M[recall@k]
 R --> M
 M --> T[recall-latency-cost tuning]
```

HNSW = highway → neighborhood → local search. Filter, bulunan adayların bir bölümünü kapıdan geri çevirir; unfiltered recall iyi olsa bile filtered recall kötü olabilir.

## İçeride ne oluyor?
1. Vector'lar metric'e göre proximity graph'a yerleşir.
2. Query üst katmandan iyi bir bölgeye yaklaşır.
3. Alt katmanlarda candidate frontier genişletilir.
4. Base layer yaklaşık nearest candidates üretir.
5. Metadata predicate pre/post/hybrid stratejiyle uygulanır.
6. Candidate starvation varsa search breadth/iterative scan artırılabilir.
7. Exact search sample ground truth; ANN sonucu recall@k üretir.
8. p95/p99, recall slice, index bytes, build time ve QPS birlikte optimize edilir.

## Mülakat soruları
- Exact kNN ile ANN trade-off'u nedir?
- HNSW hierarchy neden faydalıdır?
- `M`, `ef_construction`, `ef_search` neyi etkiler?
- Metric seçimi embedding normalization ile nasıl ilişkilidir?
- Selective filter neden recall düşürebilir?
- Iterative scan hangi problemi çözer ve bedeli nedir?
- Senior: recall@10 evaluation'ı nasıl kurarsın?
- Staff: multi-tenant RAG partition/index topology'si nasıl tasarlanır?
- Principal: embedding migration dual-index/shadow/rollback nasıl yapılır?

## Beklenen cevap seviyesi
**Mid:** exact/ANN ve recall-latency. **Senior:** HNSW parametreleri, metric ve filtered ANN. **Staff:** skew, tenant partitioning, rebuild ve capacity. **Principal:** embedding migration, quality SLO, fleet cost ve lifecycle.

## Mini alıştırma
10k query için exact top-10 ground truth üret. Üç `ef_search` değeriyle filtersiz ve %2-selective tenant filtresi altında recall@10, p95 ve result-count distribution ölç. `LIMIT 10` olup 3 sonuç dönen vakayı ayrıca analiz et.

## Proje
`filtered-ann-lab`: PostgreSQL + pgvector, 100k–1M embedding, HNSW; `ef_search`, iterative scan, B-tree prefilter, partial index ve partitioning varyantlarını karşılaştır. Recall@k, p50/p95/p99, rows returned, CPU/buffers, index size ve build time dashboard'u üret.

## Failure modes / trade-off / production
Latency ölçüp recall ölçmemek silent quality loss'tur. Random query set gerçek tenant/filter skew'unu kaçırabilir. Çok yüksek search breadth ANN avantajını azaltır; çok düşük breadth filtered starvation yaratır. Embedding model versiyonlarını aynı vector space sanmak correctness hatasıdır. Tenant authorization vector filter'ın kendisine bırakılmamalıdır.

İzlenecek sinyaller: offline recall, undersized result rate, filter selectivity, p95/p99, CPU, memory/index bytes, rebuild süresi ve embedding-version dağılımı.

## Kaynaklar
- HNSW paper: https://arxiv.org/abs/1603.09320
- IEEE/PubMed record: https://pubmed.ncbi.nlm.nih.gov/30602420/
- pgvector README: https://github.com/pgvector/pgvector/blob/master/README.md
