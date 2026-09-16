# Python 3.14 Free-Threading, GIL & Thread Safety

## Konu anlatımı
CPython'ın klasik build'inde GIL aynı anda yalnız bir thread'in Python object/C API üzerinde çalışmasını sınırlar. Free-threaded build GIL'i devre dışı bırakabilir ve CPU-bound Python thread'lerinin farklı çekirdeklerde paralel çalışmasına izin verir. Python 3.14'te bu build officially supported fakat optional'dır; specializing adaptive interpreter free-threaded modda da aktiftir. Resmi release notes tek-thread workload için platform/compiler'a bağlı yaklaşık %5–10 overhead bildirir.

GIL'in kaldırılması shared mutable state'i güvenli yapmaz. Application invariants lock, queue, immutable data veya ownership ile korunmalıdır. Bazı native extension'lar free-threading'e hazır değilse GIL'i yeniden etkinleştirebilir; rollout dependency compatibility, race testing ve benchmark gerektirir.

## Mental model
```text
classic: T1 -> [GIL] <- T2
free-threaded: T1 -> core1 | T2 -> core2
parallelism != shared-state safety
```

## İçeride ne oluyor?
`sys._is_gil_enabled()` runtime GIL durumunu; `sysconfig.get_config_var("Py_GIL_DISABLED")` build desteğini kontrol etmekte kullanılabilir. Built-in bir operation'ın thread-safe olması multi-step business invariant'ın atomic olduğu anlamına gelmez. Native C API kullanan extension'lar ayrıca değerlendirilmelidir.

## Mülakat soruları
- GIL neyi garanti eder, neyi etmez?
- CPU-bound ve I/O-bound thread farkı nedir?
- Free-threading multiprocessing'i tamamen kaldırır mı?
- Extension neden GIL'i yeniden etkinleştirebilir?
- Compound shared-state invariant nasıl korunur?

## Beklenen cevap seviyesi
Junior/Mid: thread, race, lock, CPU/I/O. Senior: extension compatibility ve compound invariants. Staff: rollout, capacity, observability ve fallback.

## Mini alıştırma
Shared dictionary üzerinde `read -> compute -> write` yapan dört thread için race noktalarını işaretle; lock scope veya work partitioning tasarla.

## Proje fikri
Classic/free-threaded CPython karşılaştıran benchmark: throughput/core, CPU utilization, p95 latency ve dependency compatibility.

## Production bağlantısı / failure modes
Otomatik speedup varsaymak, GIL'i application mutex sanmak, native dependency'leri atlamak ve tek-thread overhead'i ölçmemek yaygın hatalardır.

## Kaynaklar
- https://docs.python.org/3/whatsnew/3.14.html
- https://docs.python.org/3.14/howto/free-threading-python.html
- https://docs.python.org/3.14/c-api/threads.html
