# Monotonic Stack, Next Greater Element & Amortized O(n)

## Konu anlatımı
Monotonic stack, elemanları artan veya azalan invariant altında tutan stack pattern'idir. Next Greater Element'te stack'te henüz cevabı bulunmamış index'ler tutulur. Yeni değer top'tan büyük olduğunda top'un cevabı bulunur ve pop edilir; sonra yeni index push edilir.

İç içe `while` görünse de toplam süre O(n)'dir: her index en fazla bir kez push ve bir kez pop edilir. Bu amortized-analysis argümanı pattern'in özüdür. Stock span, daily temperatures ve histogram boundary problemleri aynı fikrin varyantlarıdır.

## Mental model
```text
values: 2 1 5 3 4
2 -> [2]
1 -> [2,1]
5 -> pop 1, pop 2, push 5
3 -> [5,3]
4 -> pop 3, push 4

push <= 1 + pop <= 1 per index => O(n)
```

## Mülakat soruları
- Monotonic invariant nedir?
- NGE brute force karmaşıklığı?
- `while` varken neden O(n)?
- Index vs value tutmak neyi değiştirir?
- `<` ve `<=` duplicate semantics'i nasıl etkiler?
- Largest Rectangle in Histogram'da stack neyi temsil eder?

## Beklenen cevap seviyesi
Junior: stack ve brute force. Mid: invariant, index implementation ve amortized O(n). Senior varyantı: duplicates, boundaries ve histogram/range dönüşümleri.

## Mini alıştırma
`[2,1,2,4,3]` için next-greater index dizisini çıkar; sonra next-smaller'a dönüştür.

## Proje fikri
`monotonic-pattern-visualizer`: push/pop adımlarını NGE, stock span ve daily temperatures için görselleştir.

## Production / failure modes
Index gerektiği halde value tutmak; duplicate semantics'i tanımlamamak; invariant'ı ters kurmak; amortized complexity'yi açıklayamamak. Pattern sequence/range analytics'te de kullanılabilir.

## Kaynaklar
- https://algs4.cs.princeton.edu/13stacks/
