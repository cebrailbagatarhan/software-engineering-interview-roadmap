# HNSW, Recall–Latency Trade-off & Filtered Vector Search

## Neden önemli?
Vector retrieval, semantic search ve RAG sistemlerinde exact nearest-neighbor search veri büyüdükçe pahalılaşır. Approximate nearest-neighbor (ANN) index'leri hız için bazı gerçek komşuları kaçırmayı kabul eder. HNSW bu alanın temel graph tabanlı tasarımlarındandır.

## Mental model
```mermaid
flowchart TD
 Q[Query vector] --> U[Sparse upper layers]
 U --> B[Dense base graph]
 B --> C[Candidate set]
 C --> F[Metadata filter]
 F --> K[Top-k]
 F -->|too few survivors| X[Expand search]
 X --> B
 E[Exact ground truth sample] --> R[Recall@k evaluation]
 K --> R
```

HNSW'yi **highway + local streets** olarak düşün: üst katman doğru bölgeye hızlı yaklaşır, alt katman yakın komşuları ayrıntılı tarar.

## Temel mekanizma
HNSW çok katmanlı proximity graph kurar. Node'ların üst katmanlarda bulunma olasılığı katman yükseldikçe azalır. Query seyrek üst graph'ta navigasyonla başlar, aşağı katmanlara indikçe daha yoğun candidate search yapar. Search breadth yükseldikçe recall genellikle iyileşir; latency/CPU da yükselir.

## Dört yönlü sözleşme
HNSW tuning'i tek metrikli değildir:

`recall ↔ latency ↔ memory ↔ build/update cost`

Graph degree/build effort index memory ve build süresini; query search budget ise runtime recall/latency'yi etkiler. Kalite exact ground-truth sample'a karşı `recall@k` ile ölçülmelidir.

## Filtering problemi
Metadata predicate ANN traversal'dan sonra uygulanırsa adayların büyük bölümü elenebilir. Seçici filtrede top-k için yeterli survivor kalmayabilir. pgvector bu durumda iterative scans ile daha fazla index tarayabilir; alternatifler exact B-tree prefilter, partial HNSW index veya partitioning'dir.

Multi-tenant workload'da global graph tenant distribution/skew'dan etkilenebilir. Partitioning/separate tables isolation sağlar ama index sayısı, memory ve operasyon maliyetini büyütür.

## Mülakat derinliği
- **Mid:** exact-vs-ANN, similarity metric, recall@k, HNSW layers.
- **Senior:** search breadth, memory/build cost, filtered recall ve benchmark design.
- **Staff:** partitioning/partial-index/iterative-scan seçimi, tenant isolation, lifecycle.
- **Principal/CTO:** retrieval recall'ını end-to-end RAG quality, token/reranking cost, SLO ve ürün metriğiyle optimize etme.

## Production benchmark
Representative query set için exact top-k ground truth üret. Her config için recall@k, p50/p95/p99, QPS, CPU, memory/index size ölç. Filter selectivity ve tenant skew boyutlarını ayrı deney ekseni yap. Index/config/data-distribution değişimlerinde aynı benchmark'ı regression gate olarak çalıştır.

## Failure modes / trade-off
HTTP 200, ANN correctness kanıtı değildir. Recall sessizce düşebilir. Search budget'ını körlemesine büyütmek latency/CPU maliyeti yaratır. Partitioning isolation/filtered recall'ı iyileştirebilir fakat operasyonel parçalanma yaratır. RAG'de fazla candidate retrieval reranker ve prompt/token maliyetini artırabilir; retrieval metriği downstream answer-quality metriğiyle birlikte değerlendirilmelidir.

## Kaynaklar
- Malkov & Yashunin — HNSW: https://arxiv.org/abs/1603.09320
- IEEE TPAMI: https://doi.org/10.1109/TPAMI.2018.2889473
- pgvector — HNSW, filtering, iterative scans: https://github.com/pgvector/pgvector#hnsw
