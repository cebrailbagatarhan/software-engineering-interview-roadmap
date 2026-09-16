# C++26 Hazard Pointers, RCU & Safe Memory Reclamation

## Neden var?
Lock-free veri yapısında atomik pointer update visibility sağlar; object lifetime'ı otomatik olarak güvenli yapmaz. Bir thread pointer'ı okuduktan sonra başka thread objeyi structure'dan çıkarıp free ederse ilk thread use-after-free yaşayabilir. C++26 `<hazard_pointer>` ve `<rcu>` ile safe reclamation primitive'lerini standard library'ye taşır.

## Mental model
```text
Hazard pointer: protect -> validate -> use -> clear
Writer: unlink -> retire -> no hazard? -> reclaim

RCU: read-side region -> writer replace/retire -> grace period -> reclaim
```

## Hazard pointer
Reader objeye erişmeden önce pointer'ı hazard slot'ta yayınlar ve source pointer'ı tekrar doğrular. Writer logical removal sonrası objeyi retire eder; aktif hazard setinde görünmüyorsa daha sonra reclaim eder. Publish + validate sırası access-deletion race'i kapatır.

## RCU
Read-mostly sistemlerde reader path'i protection region ile ucuz tutulur. Writer yeni versiyonu publish eder, eski objeyi retire eder ve eski reader'ların grace period'u tamamlandıktan sonra reclaim eder. Reader maliyeti düşerken reclamation latency ve memory backlog artabilir.

## Mülakat ayrımları
- Atomicity != lifetime safety.
- ABA != reclamation; ilişkili olabilir ama farklı problemlerdir.
- Lock-free != wait-free.
- Hazard pointer daha explicit per-object protection; RCU read-mostly workload'larda reader tarafını optimize eder.

## Production
Retired-object backlog, reclaim latency, peak memory, CAS retries ve p99 operation latency izlenir. Lock-free complexity düşük-contention workload'da mutex'ten daha kötü engineering trade-off olabilir.

## Kaynaklar
- https://en.cppreference.com/w/cpp/thread
- https://en.cppreference.com/cpp/headers
- https://wg21.link/P2530R3
- https://wg21.link/P2545R4
