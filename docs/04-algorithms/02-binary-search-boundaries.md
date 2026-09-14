# Binary Search ve Boundary Thinking

Binary search'in en güçlü genellemesi yalnız sorted array'de exact match bulmak değildir. Monoton bir predicate'in değiştiği sınırı bulma problemidir.

```text
false false false | true true true
                  ^
              boundary
```

Her iterasyonda bir invariant korunur ve arama uzayı küçülür. Bu nedenle search O(log n) olabilir. Fakat sorted array'e insertion yapmak O(n) olabilir; search complexity ile mutation complexity aynı değildir.

## Temel desenler

- exact match
- lower bound: ilk `>= target`
- upper bound: ilk `> target`
- first/last occurrence
- answer-space search: monoton feasibility predicate'i üzerinde minimum veya maximum geçerli cevap

## Mülakat beklentisi

Junior klasik binary search'i off-by-one hatası olmadan yazmalı. Mid lower/upper bound ve answer-space search'i tanımalı. Senior termination invariant, overflow-safe midpoint, random-access gereksinimi ve pahalı predicate maliyetini tartışabilmeli.

## Failure modes

`lo <= hi` ve `lo < hi` şablonlarını bilinçsiz karıştırmak, midpoint sonrası sınırı ilerletmemek, monoton olmayan predicate üzerinde binary search yapmak ve duplicate değerlerde yanlış boundary döndürmek sık hatalardır.

## Mini lab

Önce sorted array'de ilk `target` index'ini bul. Sonra aynı boundary şablonunu, işleri D gün içinde tamamlayan minimum kapasiteyi bulacak feasibility search'e dönüştür.

## Production bağlantısı

Binary search capacity planning, threshold calibration ve monoton cost/performance fonksiyonlarında kullanılabilir. Predicate'in kendisi pahalı bir distributed ölçümse O(log n) çağrının bile maliyetli olacağını hesaba kat.

## Kaynak

- Python `bisect` resmi dokümanı: https://docs.python.org/3/library/bisect.html
